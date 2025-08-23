#!/usr/bin/env python3
"""
Interactive Text Refinement Program for txtRefine

This program provides an interactive menu system where you can choose
models, files, and options without using command-line arguments.
"""

import os
import sys
from pathlib import Path
import time

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def show_header():
    """Display the program header."""
    print("=" * 60)
    print("🎯 txtRefine - Refinamento Interativo de Transcrições")
    print("=" * 60)
    print("📚 Especializado em filosofia e conteúdo acadêmico")
    print()

def list_available_models():
    """List all available Ollama models and return them."""
    try:
        import ollama
        response = ollama.list()
        models = response.models if hasattr(response, 'models') else []
        
        model_info = []
        if models:
            for model in models:
                model_name = getattr(model, 'model', 'Unknown')
                model_size = getattr(model, 'size', 'Unknown size')
                # Convert size to GB for readability
                if isinstance(model_size, int):
                    size_gb = f"{model_size / (1024**3):.1f} GB"
                else:
                    size_gb = str(model_size)
                model_info.append({
                    'name': model_name,
                    'size': size_gb,
                    'size_bytes': model_size if isinstance(model_size, int) else 0
                })
        
        return model_info
            
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        return []

def show_models_menu(models):
    """Display the models menu and return selected model."""
    print("🤖 Modelos Disponíveis:")
    print("-" * 40)
    
    # Sort models by recommended order for philosophy
    recommended_order = [
        'llama3.2:latest',  # Default - good balance
        'neural-chat:latest',  # Highest quality
        'openchat:latest',  # High quality
        'dolphin-phi:latest',  # Good balance
        'gemma:2b'  # Fastest
    ]
    
    # Sort models by recommendation, then alphabetically
    def sort_key(model):
        name = model['name']
        if name in recommended_order:
            return (recommended_order.index(name), name)
        else:
            return (len(recommended_order), name)
    
    sorted_models = sorted(models, key=sort_key)
    
    for i, model in enumerate(sorted_models, 1):
        marker = "⭐" if model['name'] == 'llama3.2:latest' else "  "
        print(f"{marker} {i}. {model['name']} ({model['size']})")
    
    print()
    print("⭐ = Modelo padrão recomendado")
    print()
    
    while True:
        try:
            choice = input("Escolha um modelo (número) ou Enter para padrão [1]: ").strip()
            
            if not choice:  # Default to llama3.2:latest
                default_model = next((m for m in sorted_models if m['name'] == 'llama3.2:latest'), sorted_models[0])
                return default_model['name']
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(sorted_models):
                return sorted_models[choice_num - 1]['name']
            else:
                print(f"❌ Escolha um número entre 1 e {len(sorted_models)}")
        except ValueError:
            print("❌ Digite um número válido")

def list_input_files():
    """List all .txt files in the input folder."""
    input_folder = Path("input")
    
    if not input_folder.exists():
        print("❌ Pasta 'input' não encontrada")
        return []
    
    txt_files = list(input_folder.glob("*.txt"))
    return [f.name for f in txt_files]

def show_files_menu(files):
    """Display the files menu and return selected files."""
    if not files:
        print("❌ Nenhum arquivo .txt encontrado na pasta 'input'")
        print("💡 Coloque seus arquivos .txt na pasta 'input' e tente novamente")
        return []
    
    print("📁 Arquivos Disponíveis:")
    print("-" * 40)
    
    for i, file in enumerate(files, 1):
        file_path = Path("input") / file
        try:
            size = file_path.stat().st_size
            size_kb = f"{size / 1024:.1f} KB"
        except:
            size_kb = "? KB"
        
        print(f"   {i}. {file} ({size_kb})")
    
    print(f"   {len(files) + 1}. Todos os arquivos")
    print()
    
    while True:
        try:
            choice = input("Escolha arquivo(s) (número, lista ou 'todos'): ").strip().lower()
            
            if choice in ['todos', 'all', str(len(files) + 1)]:
                return files
            
            if ',' in choice:
                # Multiple files
                choices = [int(x.strip()) for x in choice.split(',')]
                selected_files = []
                for c in choices:
                    if 1 <= c <= len(files):
                        selected_files.append(files[c - 1])
                if selected_files:
                    return selected_files
                else:
                    print("❌ Números inválidos")
            else:
                # Single file
                choice_num = int(choice)
                if 1 <= choice_num <= len(files):
                    return [files[choice_num - 1]]
                else:
                    print(f"❌ Escolha um número entre 1 e {len(files) + 1}")
        except ValueError:
            print("❌ Digite um número válido ou 'todos'")

def show_options_menu():
    """Display processing options menu."""
    print("⚙️  Opções de Processamento:")
    print("-" * 40)
    print("   1. Processar agora")
    print("   2. Comparar com múltiplos modelos")
    print("   3. Ver estatísticas dos arquivos")
    print("   4. Configurações avançadas")
    print()
    
    while True:
        try:
            choice = input("Escolha uma opção [1]: ").strip()
            
            if not choice:
                return 1
            
            choice_num = int(choice)
            if 1 <= choice_num <= 4:
                return choice_num
            else:
                print("❌ Escolha um número entre 1 e 4")
        except ValueError:
            print("❌ Digite um número válido")

def show_file_stats(files):
    """Show statistics about the selected files."""
    print("📊 Estatísticas dos Arquivos:")
    print("-" * 40)
    
    total_size = 0
    total_words = 0
    
    for file in files:
        file_path = Path("input") / file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            size = len(content)
            words = len(content.split())
            total_size += size
            total_words += words
            
            print(f"📄 {file}:")
            print(f"   📏 {size:,} caracteres")
            print(f"   📝 {words:,} palavras")
            print(f"   ⏱️  Tempo estimado: {words // 100:.1f}-{words // 50:.1f} segundos")
            print()
            
        except Exception as e:
            print(f"❌ Erro ao ler {file}: {e}")
    
    if len(files) > 1:
        print("📊 Total:")
        print(f"   📏 {total_size:,} caracteres")
        print(f"   📝 {total_words:,} palavras")
        print(f"   ⏱️  Tempo estimado total: {total_words // 100:.1f}-{total_words // 50:.1f} segundos")
    
    print()
    input("Pressione Enter para continuar...")

def process_files(files, model_name):
    """Process the selected files with the selected model."""
    print(f"🚀 Iniciando processamento com {model_name}")
    print("=" * 60)
    
    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)
    
    results = []
    
    for i, file in enumerate(files, 1):
        print(f"\n📦 Processando arquivo {i}/{len(files)}: {file}")
        print("-" * 40)
        
        input_path = Path("input") / file
        output_filename = f"refined_{file}"
        output_path = Path("output") / output_filename
        
        try:
            from refine import refine_transcription
            success = refine_transcription(input_path, output_path, model_name)
            
            if success:
                print(f"✅ {file} processado com sucesso!")
                results.append({"file": file, "success": True})
            else:
                print(f"❌ Falha ao processar {file}")
                results.append({"file": file, "success": False})
                
        except Exception as e:
            print(f"❌ Erro ao processar {file}: {e}")
            results.append({"file": file, "success": False, "error": str(e)})
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 RESUMO DO PROCESSAMENTO")
    print("=" * 60)
    
    successful = sum(1 for r in results if r.get('success'))
    failed = len(results) - successful
    
    print(f"📁 Total de arquivos: {len(files)}")
    print(f"✅ Processados com sucesso: {successful}")
    print(f"❌ Falhas: {failed}")
    
    if successful > 0:
        print(f"\n✅ Arquivos refinados salvos na pasta 'output/':")
        for result in results:
            if result.get('success'):
                print(f"   📄 refined_{result['file']}")
    
    return results

def compare_models(files, models):
    """Compare multiple models on the same files."""
    print("🔍 Comparação de Modelos")
    print("=" * 60)
    
    # Select models to compare
    print("Escolha modelos para comparar:")
    recommended_models = ['neural-chat:latest', 'openchat:latest', 'llama3.2:latest']
    available_recommended = [m for m in recommended_models if any(model['name'] == m for model in models)]
    
    if len(available_recommended) >= 2:
        print(f"Usar modelos recomendados? ({', '.join(available_recommended)}) [s/n]: ", end="")
        choice = input().strip().lower()
        
        if choice in ['s', 'sim', 'y', 'yes', '']:
            selected_models = available_recommended[:3]  # Max 3 models
        else:
            selected_models = [show_models_menu(models)]
    else:
        selected_models = [show_models_menu(models)]
    
    print(f"\n🤖 Comparando {len(selected_models)} modelo(s) em {len(files)} arquivo(s)")
    print("⚠️  Isso pode demorar um pouco...")
    
    # This would integrate with the compare_models.py functionality
    print("💡 Para comparação detalhada, use: python3 compare_models.py")
    input("Pressione Enter para continuar...")

def main():
    """Main interactive function."""
    while True:
        show_header()
        
        # Check if Ollama is available
        try:
            import ollama
        except ImportError:
            print("❌ Ollama não encontrado. Instale com: pip install ollama")
            return
        
        # Get available models
        models = list_available_models()
        if not models:
            print("❌ Nenhum modelo encontrado. Instale modelos com: ollama pull llama3.2:latest")
            return
        
        # Select model
        print("🎯 Passo 1: Escolha o modelo")
        selected_model = show_models_menu(models)
        print(f"✅ Modelo selecionado: {selected_model}\n")
        
        # Select files
        print("🎯 Passo 2: Escolha os arquivos")
        available_files = list_input_files()
        selected_files = show_files_menu(available_files)
        
        if not selected_files:
            print("\n❌ Nenhum arquivo selecionado")
            input("Pressione Enter para sair...")
            return
        
        print(f"✅ Arquivo(s) selecionado(s): {', '.join(selected_files)}\n")
        
        # Select processing option
        print("🎯 Passo 3: Escolha a ação")
        option = show_options_menu()
        
        if option == 1:
            # Process files
            process_files(selected_files, selected_model)
            
        elif option == 2:
            # Compare models
            compare_models(selected_files, models)
            
        elif option == 3:
            # Show file statistics
            show_file_stats(selected_files)
            continue
            
        elif option == 4:
            # Advanced settings (placeholder)
            print("⚙️  Configurações avançadas (em desenvolvimento)")
            input("Pressione Enter para continuar...")
            continue
        
        # Ask if user wants to process more files
        print(f"\n{'='*60}")
        print("✨ Processar mais arquivos? [s/n]: ", end="")
        continue_choice = input().strip().lower()
        
        if continue_choice not in ['s', 'sim', 'y', 'yes']:
            print("\n🎉 Obrigado por usar o txtRefine!")
            break
        
        print()  # Add some space before next iteration

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Tente novamente ou reporte o problema")
