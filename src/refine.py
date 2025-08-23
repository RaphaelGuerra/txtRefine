#!/usr/bin/env python3
"""
Text Refinement Program for Portuguese Philosophy Class Transcriptions

This program refines transcriptions of philosophy classes in Brazilian Portuguese,
specifically designed for classes by Olavo de Carvalho and similar philosophical content.
It maintains fidelity to the original while improving clarity and correcting obvious errors.
"""

import ollama
import os
import argparse
import re
from pathlib import Path
from tqdm import tqdm
import time
from config import *

def check_ollama_installation():
    """Check if Ollama is installed and accessible."""
    try:
        import ollama
        return True
    except ImportError:
        return False

def check_model_availability(model_name):
    """Check if the specified Ollama model is available."""
    try:
        ollama.show(model_name)
        return True
    except Exception:
        return False

def detect_content_type(text):
    """Detect the type of content to choose appropriate prompt."""
    text_lower = text.lower()
    
    # Check for philosophy keywords
    philosophy_score = sum(1 for keyword in CONTENT_TYPE_KEYWORDS["philosophy"] 
                          if keyword in text_lower)
    
    if philosophy_score >= 2:  # If 2 or more philosophy keywords found
        return "philosophy"
    else:
        return "general"

def clean_text(text):
    """Clean and preprocess the text for better processing."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove line breaks that break sentences
    text = re.sub(r'([.!?])\s*\n', r'\1 ', text)
    # Clean up common transcription artifacts
    text = re.sub(r'([a-z])\s*-\s*([a-z])', r'\1\2', text)  # Fix broken words
    return text.strip()

def split_into_chunks(text, max_words=MAX_WORDS_PER_CHUNK):
    """Split text into chunks while preserving sentence boundaries."""
    sentences = re.split(r'([.!?]+)', text)
    chunks = []
    current_chunk = ""
    current_word_count = 0
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
        full_sentence = sentence + punctuation
        
        sentence_words = len(sentence.split())
        
        if current_word_count + sentence_words > max_words and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = full_sentence
            current_word_count = sentence_words
        else:
            current_chunk += full_sentence
            current_word_count += sentence_words
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def create_refinement_prompt(chunk, chunk_num, total_chunks, content_type="philosophy"):
    """Create a specialized prompt for refining transcriptions."""
    if content_type == "philosophy":
        prompt_template = PHILOSOPHY_REFINEMENT_PROMPT
    else:
        prompt_template = GENERAL_REFINEMENT_PROMPT
    
    return prompt_template.format(
        chunk_num=chunk_num,
        total_chunks=total_chunks,
        chunk=chunk
    )

def refine_chunk(chunk, chunk_num, total_chunks, model_name, content_type="philosophy", max_retries=MAX_RETRIES):
    """Refine a single chunk of text using the specified Ollama model."""
    prompt = create_refinement_prompt(chunk, chunk_num, total_chunks, content_type)
    
    for attempt in range(max_retries):
        try:
            response = ollama.chat(model=model_name, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            
            refined_text = response['message']['content']
            
            # Verify the response is not too short (indicating potential loss of content)
            if len(refined_text) < len(chunk) * CONTENT_LOSS_THRESHOLD:
                print(ERROR_MESSAGES["content_loss_warning"].format(
                    chunk_num=chunk_num, 
                    attempt=attempt + 1
                ))
                if attempt < max_retries - 1:
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
            
            return refined_text
            
        except Exception as e:
            if "Failed to connect" in str(e):
                print(ERROR_MESSAGES["connection_error"])
                return None
            elif "context length" in str(e).lower():
                print(ERROR_MESSAGES["context_length_error"].format(chunk_num=chunk_num))
                # Try with smaller chunk
                smaller_chunks = split_into_chunks(chunk, max_words=MIN_WORDS_PER_CHUNK)
                refined_parts = []
                for i, small_chunk in enumerate(smaller_chunks):
                    refined_part = refine_chunk(small_chunk, f"{chunk_num}.{i+1}", len(smaller_chunks), model_name, content_type, 1)
                    if refined_part:
                        refined_parts.append(refined_part)
                    else:
                        refined_parts.append(small_chunk)  # Fallback to original
                return " ".join(refined_parts)
            else:
                print(ERROR_MESSAGES["unexpected_error"].format(chunk_num=chunk_num, error=e))
                if attempt < max_retries - 1:
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
                return chunk  # Fallback to original text
    
    return chunk  # Fallback to original if all retries failed

def refine_transcription(input_path, output_path, model_name):
    """Refine the complete transcription file."""
    print(SUCCESS_MESSAGES["processing_file"].format(filename=os.path.basename(input_path)))
    
    # Read and clean input file
    with open(input_path, 'r', encoding=DEFAULT_ENCODING) as f:
        transcription = f.read()
    
    if not transcription.strip():
        print(ERROR_MESSAGES["empty_file"])
        return False
    
    # Clean the text
    cleaned_text = clean_text(transcription)
    
    # Detect content type for appropriate prompt selection
    content_type = detect_content_type(cleaned_text)
    print(f"📚 Tipo de conteúdo detectado: {content_type}")
    
    # Split into manageable chunks
    chunks = split_into_chunks(cleaned_text, max_words=MAX_WORDS_PER_CHUNK)
    print(SUCCESS_MESSAGES["chunks_created"].format(count=len(chunks)))
    
    refined_chunks = []
    
    # Process each chunk with progress bar
    for i, chunk in enumerate(tqdm(chunks, desc=PROGRESS_BAR_DESC, unit=PROGRESS_BAR_UNIT)):
        if not chunk.strip():
            continue
            
        refined_chunk = refine_chunk(chunk, i + 1, len(chunks), model_name, content_type)
        
        if refined_chunk:
            refined_chunks.append(refined_chunk)
        else:
            print(ERROR_MESSAGES["using_original"].format(chunk_num=i + 1))
            refined_chunks.append(chunk)
    
    # Combine refined chunks
    refined_text = OUTPUT_SEPARATOR.join(refined_chunks)
    
    # Write output file
    with open(output_path, 'w', encoding=DEFAULT_ENCODING) as f:
        f.write(refined_text)
    
    print(SUCCESS_MESSAGES["refinement_complete"].format(filename=os.path.basename(output_path)))
    print(SUCCESS_MESSAGES["statistics"])
    print(SUCCESS_MESSAGES["original_chars"].format(count=len(transcription)))
    print(SUCCESS_MESSAGES["refined_chars"].format(count=len(refined_text)))
    print(SUCCESS_MESSAGES["chunks_processed"].format(count=len(chunks)))
    
    return True

def show_model_recommendations():
    """Show model recommendations for different use cases."""
    print("\n🔧 Recomendações de Modelos:")
    print("=" * 60)
    
    for content_type, recommendations in MODEL_RECOMMENDATIONS.items():
        print(f"\n📚 {content_type.title()}:")
        print(f"   🏆 Melhor qualidade: {', '.join(recommendations['best'])}")
        print(f"   ⚡ Mais rápido: {', '.join(recommendations['fast'])}")
        print(f"   ⚖️  Equilibrado: {', '.join(recommendations['balanced'])}")
    
    print(f"\n📊 Detalhes dos Modelos Disponíveis:")
    print("=" * 60)
    
    # Check which models are actually available
    available_models = []
    for model_name in MODEL_DESCRIPTIONS.keys():
        try:
            ollama.show(model_name)
            available_models.append(model_name)
        except:
            pass
    
    if available_models:
        for model_name in available_models:
            if model_name in MODEL_DESCRIPTIONS:
                desc = MODEL_DESCRIPTIONS[model_name]
                print(f"\n🤖 {desc['name']} ({model_name})")
                print(f"   📝 {desc['description']}")
                print(f"   💾 Tamanho: {desc['size']}")
                print(f"   ⭐ Qualidade: {desc['quality']}")
                print(f"   ⚡ Velocidade: {desc['speed']}")
                print(f"   🎯 Melhor para: {desc['best_for']}")
    else:
        print("\n⚠️  Nenhum modelo encontrado. Execute 'ollama list' para ver modelos disponíveis.")
    
    print(f"\n💡 Para baixar novos modelos:")
    print("   ollama pull openchat:latest")
    print("   ollama pull neural-chat:latest")
    print("   ollama pull llama3.2:latest")
    print("   ollama pull dolphin-phi:latest")

def main():
    """Main function to handle command line arguments and process files."""
    parser = argparse.ArgumentParser(
        description="Refine Portuguese philosophy class transcriptions using Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 src/refine.py                                    # Process all .txt files in input folder
  python3 src/refine.py --model llama2:7b                  # Use llama2:7b model for all files
  python3 src/refine.py --files aula1.txt                  # Process specific file
  python3 src/refine.py --model gemma:7b --files aula1.txt aula2.txt  # Process specific files with specific model
  python3 src/refine.py --show-models                      # Show model recommendations
        """
    )
    
    parser.add_argument(
        '--model',
        default=DEFAULT_MODEL,
        help=f'Ollama model to use (default: {DEFAULT_MODEL})'
    )
    
    parser.add_argument(
        '--files',
        nargs='+',
        help='Specific .txt files to process (if not specified, processes all .txt files in input folder)'
    )
    
    parser.add_argument(
        '--show-models',
        action='store_true',
        help='Show model recommendations for different use cases'
    )
    
    args = parser.parse_args()
    
    # Show model recommendations if requested
    if args.show_models:
        show_model_recommendations()
        return
    
    # Check Ollama installation
    if not check_ollama_installation():
        print(ERROR_MESSAGES["ollama_not_found"])
        print(ERROR_MESSAGES["ollama_install_url"])
        return
    
    # Check model availability
    if not check_model_availability(args.model):
        print(ERROR_MESSAGES["model_not_found"].format(model=args.model))
        print(ERROR_MESSAGES["model_pull_command"].format(model=args.model))
        return
    
    print(SUCCESS_MESSAGES["using_model"].format(model=args.model))
    
    # Setup folders
    input_folder = Path('input')
    output_folder = Path('output')
    
    if not input_folder.exists():
        print(ERROR_MESSAGES["input_folder_not_found"])
        return
    
    output_folder.mkdir(exist_ok=True)
    
    # Determine files to process
    if args.files:
        # Process specific files
        files_to_process = []
        for filename in args.files:
            input_path = input_folder / filename
            if input_path.exists() and filename.endswith('.txt'):
                files_to_process.append(input_path)
            else:
                print(ERROR_MESSAGES["file_not_found"].format(filename=filename))
    else:
        # Process all .txt files in input folder
        files_to_process = list(input_folder.glob(TEXT_FILE_PATTERN))
    
    if not files_to_process:
        print(ERROR_MESSAGES["no_files_to_process"])
        return
    
    print(SUCCESS_MESSAGES["files_processing"].format(count=len(files_to_process)))
    
    # Process each file
    for input_path in files_to_process:
        output_filename = f"{OUTPUT_PREFIX}{input_path.name}"
        output_path = output_folder / output_filename
        
        print(f"\n{'='*60}")
        success = refine_transcription(input_path, output_path, args.model)
        
        if not success:
            print(ERROR_MESSAGES["processing_failed"].format(filename=input_path.name))
    
    print(f"\n{'='*60}")
    print(SUCCESS_MESSAGES["processing_complete"])

if __name__ == '__main__':
    main()
