import ollama
import os
import shutil
import argparse
from tqdm import tqdm

def check_ollama_installation():
    return shutil.which('ollama') is not None

def check_model_availability(model_name):
    try:
        ollama.show(model_name)
        return True
    except Exception:
        return False

def refine_transcription(input_path, output_path, model_name):
    with open(input_path, 'r') as f:
        transcription = f.read()

    # Split the transcription into chunks of 500 words
    words = transcription.split()
    chunks = [" ".join(words[i:i+500]) for i in range(0, len(words), 500)]
    
    refined_chunks = []

    with tqdm(total=len(chunks), desc=f"Refining {os.path.basename(input_path)}", unit="chunk") as pbar:
        for chunk in chunks:
            try:
                response = ollama.chat(model=model_name, messages=[
                    {
                        'role': 'user',
                        'content': f'Refine the following transcription of a class in Brazilian Portuguese. Make it clear and correct, but keep it as close to the original as possible:\n\n{chunk}',
                    },
                ])
                
                refined_chunks.append(response['message']['content'])
                pbar.update(1)

            except Exception as e:
                if "Failed to connect" in str(e):
                    tqdm.write("Error: Could not connect to Ollama. Please make sure Ollama is running and accessible.")
                    tqdm.write("You can download Ollama from https://ollama.com/download")
                else:
                    tqdm.write(f"An unexpected error occurred: {e}")
                return

    refined_text = "\n".join(refined_chunks)

    with open(output_path, 'w') as f:
        f.write(refined_text)
    
    tqdm.write(f'Refined {os.path.basename(input_path)} and saved to {output_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Refine transcriptions using Ollama.')
    parser.add_argument('--model', type=str, default='gemma:2b', help='Ollama model to use for refinement (e.g., gemma:2b, llama2).')
    parser.add_argument('--files', nargs='*', help='Specific input files to process (e.g., file1.txt file2.txt). If not provided, all .txt files in the input folder will be processed.')
    args = parser.parse_args()

    if not check_ollama_installation():
        print("Error: ollama command not found. Please install Ollama from https://ollama.com/download")
    else:
        model_name = args.model
        if not check_model_availability(model_name):
            print(f"Error: Model '{model_name}' not found.")
            print(f"Please pull the model by running: ollama pull {model_name}")
        else:
            # Get the absolute path of the script's directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the absolute paths for the input and output folders
            input_folder_abs = os.path.join(script_dir, '..', 'input')
            output_folder_abs = os.path.join(script_dir, '..', 'output')

            # Create the output folder if it doesn't exist
            os.makedirs(output_folder_abs, exist_ok=True)

            files_to_process = []
            if args.files:
                for f in args.files:
                    full_path = os.path.join(input_folder_abs, f)
                    if os.path.exists(full_path) and f.endswith('.txt'):
                        files_to_process.append(full_path)
                    else:
                        tqdm.write(f"Warning: File '{f}' not found or is not a .txt file in the input folder. Skipping.")
            else:
                # Process all .txt files in the input folder if no specific files are provided
                for filename in os.listdir(input_folder_abs):
                    if filename.endswith('.txt'):
                        files_to_process.append(os.path.join(input_folder_abs, filename))

            if not files_to_process:
                tqdm.write("No .txt files found to process.")
                return

            for input_path in files_to_process:
                filename = os.path.basename(input_path)
                output_path = os.path.join(output_folder_abs, f'refined_{filename}')
                refine_transcription(input_path, output_path, model_name)
