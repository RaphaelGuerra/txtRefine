#!/usr/bin/env python3
"""
Test script for the improved text refinement program
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_content_detection():
    """Test the content type detection functionality."""
    print("🧪 Testando detecção de tipo de conteúdo...")
    
    # Test philosophy content
    philosophy_text = """
    A escolástica medieval foi um período importante na história da filosofia.
    Santo Tomás de Aquino e São Boaventura foram grandes pensadores.
    O problema dos universais foi muito debatido na época.
    """
    
    # Test general content
    general_text = """
    Hoje vamos falar sobre o tempo e como ele afeta nossa vida.
    O clima está muito agradável para um passeio no parque.
    """
    
    # Import and test the detection function
    try:
        from refine import detect_content_type
        
        philosophy_type = detect_content_type(philosophy_text)
        general_type = detect_content_type(general_text)
        
        print(f"✅ Texto filosófico detectado como: {philosophy_type}")
        print(f"✅ Texto geral detectado como: {general_type}")
        
        if philosophy_type == "philosophy" and general_type == "general":
            print("🎉 Detecção de conteúdo funcionando corretamente!")
        else:
            print("❌ Detecção de conteúdo com problemas")
            
    except ImportError as e:
        print(f"⚠️  Não foi possível importar o módulo de refinamento: {e}")

def test_text_cleaning():
    """Test the text cleaning functionality."""
    print("\n🧪 Testando limpeza de texto...")
    
    dirty_text = """
    O pressuposto da existência da Colássica são dois. Primeiro, a existência dessas vastas compilações de textos que acabaram tomando o título de livros de sentenças, dos quais o mais famoso foi de um sujeito chamado Pedro Lombardo.
    
    A escolástica era uma filosofia de escola que se desenvolvia dentro de uma coletividade intelectual organizada.
    """
    
    try:
        from refine import clean_text
        
        cleaned = clean_text(dirty_text)
        
        print("✅ Texto original:")
        print(dirty_text[:100] + "...")
        print("\n✅ Texto limpo:")
        print(cleaned[:100] + "...")
        
        # Check if cleaning worked
        if len(cleaned.split()) < len(dirty_text.split()):
            print("🎉 Limpeza de texto funcionando!")
        else:
            print("⚠️  Limpeza pode não estar funcionando como esperado")
            
    except ImportError as e:
        print(f"⚠️  Não foi possível importar o módulo de refinamento: {e}")

def test_chunk_splitting():
    """Test the text chunking functionality."""
    print("\n🧪 Testando divisão em chunks...")
    
    long_text = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    
    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.
    
    Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
    """
    
    try:
        from refine import split_into_chunks
        
        chunks = split_into_chunks(long_text, max_words=50)
        
        print(f"✅ Texto dividido em {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            word_count = len(chunk.split())
            print(f"   Chunk {i+1}: {word_count} palavras")
        
        if len(chunks) > 1:
            print("🎉 Divisão em chunks funcionando!")
        else:
            print("⚠️  Divisão em chunks pode não estar funcionando como esperado")
            
    except ImportError as e:
        print(f"⚠️  Não foi possível importar o módulo de refinamento: {e}")

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Verificando dependências...")
    
    required_packages = ['ollama', 'tqdm', 'pathlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'pathlib':
                from pathlib import Path
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip3 install -r requirements.txt")
    else:
        print("\n🎉 Todas as dependências estão disponíveis!")

def main():
    """Run all tests."""
    print("🚀 Iniciando testes do programa de refinamento...")
    print("=" * 60)
    
    check_dependencies()
    test_content_detection()
    test_text_cleaning()
    test_chunk_splitting()
    
    print("\n" + "=" * 60)
    print("🏁 Testes concluídos!")
    
    print("\n💡 Para testar o refinamento completo:")
    print("1. Coloque um arquivo .txt na pasta 'input/'")
    print("2. Execute: python3 src/refine.py")
    print("3. Verifique o resultado na pasta 'output/'")

if __name__ == '__main__':
    main()
