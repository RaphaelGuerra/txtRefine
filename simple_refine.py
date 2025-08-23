#!/usr/bin/env python3
"""
Simple Refinement Script for txtRefine

This script allows you to process transcription files with a single selected model,
giving you full control over the refinement process.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def list_available_models():
    """List all available Ollama models."""
    try:
        import ollama
        response = ollama.list()
        print("🤖 Modelos Disponíveis:")
        print("=" * 40)
        
        # Access the models list from the response object
        models = response.models if hasattr(response, 'models') else []
        
        if models:
            for model in models:
                model_name = getattr(model, 'model', 'Unknown')
                model_size = getattr(model, 'size', 'Unknown size')
                # Convert size to GB for readability
                if isinstance(model_size, int):
                    size_gb = f"{model_size / (1024**3):.1f} GB"
                else:
                    size_gb = str(model_size)
                print(f"   📦 {model_name} ({size_gb})")
            return [getattr(model, 'model', '') for model in models]
        else:
            print("   ⚠️  Nenhum modelo encontrado")
            return []
            
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        return []

def process_single_file(input_file, model_name, output_prefix="refined_"):
    """Process a single file with the specified model."""
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        return False
    
    # Create output filename
    input_path = Path(input_file)
    output_filename = f"{output_prefix}{input_path.name}"
    output_path = Path("output") / output_filename
    
    # Ensure output directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    print(f"📖 Processando: {input_file}")
    print(f"🤖 Modelo: {model_name}")
    print(f"📁 Saída: {output_path}")
    
    try:
        from refine import refine_transcription
        success = refine_transcription(input_file, output_path, model_name)
        
        if success:
            print(f"✅ Processamento concluído com sucesso!")
            print(f"📁 Arquivo salvo em: {output_path}")
            return True
        else:
            print(f"❌ Falha no processamento")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")
        return False

def process_multiple_files(files, model_name, output_prefix="refined_"):
    """Process multiple files with the specified model."""
    print(f"🚀 Processando {len(files)} arquivo(s) com modelo: {model_name}")
    print("=" * 60)
    
    results = []
    
    for i, file_path in enumerate(files, 1):
        print(f"\n📦 Arquivo {i}/{len(files)}")
        print("-" * 40)
        
        success = process_single_file(file_path, model_name, output_prefix)
        results.append({
            "file": file_path,
            "success": success
        })
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 RESUMO DO PROCESSAMENTO")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"📁 Total de arquivos: {len(files)}")
    print(f"✅ Processados com sucesso: {successful}")
    print(f"❌ Falhas: {failed}")
    
    if failed > 0:
        print(f"\n❌ Arquivos com falha:")
        for result in results:
            if not result['success']:
                print(f"   - {result['file']}")
    
    return results

def main():
    """Main function for simple refinement."""
    parser = argparse.ArgumentParser(
        description="Processamento simples de transcrições com modelo selecionado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 simple_refine.py --model neural-chat:latest --files arquivo.txt
  python3 simple_refine.py --model openchat:latest --files aula1.txt aula2.txt
  python3 simple_refine.py --list-models
  python3 simple_refine.py --model gemma:2b --files *.txt
        """
    )
    
    parser.add_argument(
        '--model',
        help='Modelo Ollama a usar (ex: neural-chat:latest, openchat:latest)'
    )
    
    parser.add_argument(
        '--files',
        nargs='+',
        help='Arquivo(s) a processar'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='Listar modelos disponíveis'
    )
    
    parser.add_argument(
        '--output-prefix',
        default='refined_',
        help='Prefixo para arquivos de saída (padrão: refined_)'
    )
    
    args = parser.parse_args()
    
    # List available models if requested
    if args.list_models:
        list_available_models()
        return
    
    # Check if model is specified
    if not args.model:
        print("❌ Erro: Especifique um modelo usando --model")
        print("💡 Use --list-models para ver modelos disponíveis")
        print("💡 Exemplo: python3 simple_refine.py --model neural-chat:latest --files arquivo.txt")
        return
    
    # Check if files are specified
    if not args.files:
        print("❌ Erro: Especifique arquivo(s) usando --files")
        print("💡 Exemplo: python3 simple_refine.py --model neural-chat:latest --files arquivo.txt")
        return
    
    # Check if model is available
    available_models = list_available_models()
    if args.model not in available_models:
        print(f"❌ Erro: Modelo '{args.model}' não encontrado")
        print("💡 Use --list-models para ver modelos disponíveis")
        print("💡 Baixe o modelo com: ollama pull {args.model}")
        return
    
    # Process files
    if len(args.files) == 1:
        # Single file
        success = process_single_file(args.files[0], args.model, args.output_prefix)
        if success:
            print("\n🎉 Processamento concluído!")
        else:
            print("\n❌ Processamento falhou!")
    else:
        # Multiple files
        process_multiple_files(args.files, args.model, args.output_prefix)
        print("\n🎉 Processamento em lote concluído!")

if __name__ == '__main__':
    main()
