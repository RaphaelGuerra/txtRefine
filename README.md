# Text Refinement Program

This program refines transcriptions of long classes in Brazilian Portuguese using a local Ollama model.

## How to Run

1.  **Install Ollama:** Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).
2.  **Pull the model:** Run the following command in your terminal for the default model:
    ```
    ollama pull gemma:2b
    ```
    If you plan to use a different model (e.g., `llama2`, `gemma:7b`), pull it as well:
    ```
    ollama pull <model_name>
    ```
3.  **Install Python dependencies:** Navigate to the project's root directory (`/Users/raphaelguerra/dev/txtRefine/`) and run:
    ```
    pip3 install -r requirements.txt
    ```
4.  **Place your transcription files:** Put your `.txt` transcription files into the `input` folder (e.g., `/Users/raphaelguerra/dev/txtRefine/input/`).
5.  **Run the refinement script:** Navigate to the project's root directory (`/Users/raphaelguerra/dev/txtRefine/`) and execute the following command:
    ```
    python3 src/refine.py [--model <model_name>] [--files <file1.txt> <file2.txt> ...]
    ```
    -   `--model <model_name>`: Specify the Ollama model to use (e.g., `gemma:7b`, `llama2`). If not specified, `gemma:2b` will be used by default.
    -   `--files <file1.txt> <file2.txt> ...`: Specify one or more specific `.txt` files from the `input` folder to process. If this argument is not provided, all `.txt` files in the `input` folder will be processed.
    -   A progress bar will be displayed in the terminal showing the refinement progress for each file.

**Examples:**

*   Process all files in the `input` folder using the default model:
    ```bash
    python3 src/refine.py
    ```
*   Process a specific file using the `llama2` model:
    ```bash
    python3 src/refine.py --model llama2 --files my_transcription.txt
    ```
*   Process multiple specific files using the default model:
    ```bash
    python3 src/refine.py --files file1.txt file2.txt
    ```

The refined files will be saved in the `output` folder with the prefix `refined_`.