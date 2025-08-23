#!/usr/bin/env python3
"""
Model Comparison Script for txtRefine

This script compares the output quality of different Ollama models
on the same input text to help you choose the best model for your needs.
"""

import os
import sys
from pathlib import Path
import time

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def compare_models(input_file, models_to_test):
    """Compare different models on the same input file."""
    print("🔍 Comparando Modelos de Refinamento")
    print("=" * 60)
    
    if not os.path.exists(input_file):
        print(f"❌ Arquivo de entrada não encontrado: {input_file}")
        return
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    print(f"📖 Arquivo de entrada: {input_file}")
    print(f"📝 Tamanho original: {len(original_text)} caracteres")
    print(f"🔢 Palavras originais: {len(original_text.split())}")
    print()
    
    results = {}
    
    for model_name in models_to_test:
        print(f"🤖 Testando modelo: {model_name}")
        print("-" * 40)
        
        try:
            # Import refinement function
            from refine import refine_transcription
            
            # Create output filename
            output_filename = f"refined_{model_name.replace(':', '_')}_{Path(input_file).name}"
            output_path = Path("output") / output_filename
            
            # Time the refinement
            start_time = time.time()
            success = refine_transcription(input_file, output_path, model_name)
            end_time = time.time()
            
            if success:
                # Read refined output
                with open(output_path, 'r', encoding='utf-8') as f:
                    refined_text = f.read()
                
                # Calculate metrics
                char_count = len(refined_text)
                word_count = len(refined_text.split())
                processing_time = end_time - start_time
                char_diff = char_count - len(original_text)
                word_diff = word_count - len(original_text.split())
                
                results[model_name] = {
                    "success": True,
                    "char_count": char_count,
                    "word_count": word_count,
                    "processing_time": processing_time,
                    "char_diff": char_diff,
                    "word_diff": word_diff,
                    "output_file": output_filename
                }
                
                print(f"✅ Sucesso!")
                print(f"   📊 Caracteres: {char_count} ({char_diff:+.0f})")
                print(f"   📊 Palavras: {word_count} ({word_diff:+.0f})")
                print(f"   ⏱️  Tempo: {processing_time:.1f}s")
                print(f"   📁 Arquivo: {output_filename}")
                
            else:
                results[model_name] = {"success": False}
                print("❌ Falha no processamento")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            results[model_name] = {"success": False, "error": str(e)}
        
        print()
    
    # Summary comparison
    print("📊 RESUMO DA COMPARAÇÃO")
    print("=" * 60)
    
    successful_models = [m for m, r in results.items() if r.get("success")]
    
    if not successful_models:
        print("❌ Nenhum modelo foi processado com sucesso")
        return
    
    print(f"🏆 Modelos testados com sucesso: {len(successful_models)}")
    print()
    
    # Sort by processing time
    sorted_models = sorted(
        [(m, r) for m, r in results.items() if r.get("success")],
        key=lambda x: x[1]["processing_time"]
    )
    
    print("⚡ Ranking por Velocidade:")
    for i, (model, result) in enumerate(sorted_models, 1):
        print(f"   {i}. {model}: {result['processing_time']:.1f}s")
    
    print()
    
    # Sort by content preservation (closest to original length)
    sorted_by_preservation = sorted(
        [(m, r) for m, r in results.items() if r.get("success")],
        key=lambda x: abs(x[1]["char_diff"])
    )
    
    print("🎯 Ranking por Preservação de Conteúdo:")
    for i, (model, result) in enumerate(sorted_by_preservation, 1):
        diff = result["char_diff"]
        print(f"   {i}. {model}: {diff:+.0f} caracteres")
    
    print()
    
    # Best overall model (balanced approach)
    print("⚖️  Recomendação Balanceada:")
    best_balanced = None
    best_score = float('inf')
    
    for model, result in results.items():
        if result.get("success"):
            # Score based on content preservation and speed
            preservation_score = abs(result["char_diff"]) / len(original_text)
            speed_score = result["processing_time"] / 60  # Normalize to minutes
            total_score = preservation_score + speed_score
            
            if total_score < best_score:
                best_score = total_score
                best_balanced = model
    
    if best_balanced:
        print(f"   🎯 {best_balanced} - Melhor equilíbrio entre qualidade e velocidade")
    
    print()
    print("💡 Dica: Para filosofia, priorize modelos com menor diferença de caracteres")
    print("💡 Dica: Para processamento rápido, priorize modelos com menor tempo")

def main():
    """Main function for model comparison."""
    # Models to test (in order of expected quality)
    models_to_test = [
        "neural-chat:latest",    # Highest quality
        "openchat:latest",       # High quality
        "llama3.2:latest",       # Good balance
        "dolphin-phi:latest",    # Fast
        "gemma:2b"               # Fastest
    ]
    
    # Default input file
    input_file = "input/test_sample.txt"
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    print("🚀 Comparador de Modelos txtRefine")
    print("=" * 60)
    print(f"📁 Arquivo de entrada: {input_file}")
    print(f"🤖 Modelos a testar: {len(models_to_test)}")
    print()
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Arquivo de entrada não encontrado: {input_file}")
        print("💡 Use: python3 compare_models.py [arquivo_entrada]")
        print("💡 Exemplo: python3 compare_models.py input/minha_aula.txt")
        return
    
    # Run comparison
    compare_models(input_file, models_to_test)
    
    print("🎉 Comparação concluída!")
    print("📁 Verifique os arquivos na pasta 'output/' para análise detalhada")

if __name__ == '__main__':
    main()
