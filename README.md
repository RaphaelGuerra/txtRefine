# txtRefine - BP Philosophical Text Refinement

Simple and focused tool for refining Brazilian Portuguese philosophical transcription files. Specializes in correcting common transcription errors while maintaining the original philosophical content and academic style.

## ✨ Core Features

- **BP Phonetic Corrections**: Automatic correction of Brazilian Portuguese phonetic variations (s/z, r/l, t/ch alternations)
- **Philosophical Term Database**: 386+ corrections for philosophical terms in Portuguese
- **Academic Expression Preservation**: Maintains Brazilian academic expressions ("quer dizer", "ou seja", etc.)
- **Ollama Integration**: Uses local LLMs for intelligent refinement
- **Simple Interface**: Clean command-line interface focused on the essentials

## 🚀 Quick Start

### 1. Install Ollama & Model
```bash
# Install Ollama from https://ollama.com/download
# Pull the default model
ollama pull llama3.2:latest
```

### 2. Install Dependencies
```bash
pip install ollama
```

### 3. Add Your Files
Place your `.txt` transcription files in the `input/` folder.

### 4. Run the Refinement
```bash
python txtrefine.py
```

Follow the interactive menus to choose your model and files.

## 📁 Project Structure

```
txtRefine/
├── input/                    # Your .txt transcription files
├── output/                   # Refined files (with "refined_" prefix)
├── txtrefine.py             # Main program
└── refine/                  # Core modules
    ├── philosophy_terms_database.py  # BP corrections database
    ├── model_manager.py      # Ollama integration
    ├── text_processing.py    # Text utilities
    ├── file_manager.py       # File operations
    └── ui.py                 # Simple interface
```

## 🎯 What It Does

### Corrections Applied
- ✅ **Phonetic variations**: `cauza` → `causa`, `rialidade` → `realidade`
- ✅ **Philosophical terms**: `hamartianeamente` → `hamartiano`, `ptechne` → `techne`
- ✅ **Academic expressions**: Maintains "quer dizer", "ou seja", "do ponto de vista"
- ✅ **Grammar and style**: Improves clarity while preserving original meaning

### Content Preserved
- ❌ **Philosophical arguments**: Original ideas and logical structure maintained
- ❌ **Academic style**: Brazilian philosophical discourse preserved
- ❌ **Cultural context**: Regional expressions and nuances kept intact

## 🤖 Supported Philosophical Traditions

- **Greek Classical**: Socrates, Plato, Aristotle, pre-Socratics
- **Patristic**: Augustine, Justin Martyr, Origen, Church Fathers
- **Scholastic**: Thomas Aquinas, Duns Scotus, medieval tradition
- **Brazilian Contemporary**: Olavo de Carvalho, phenomenology, existentialism

## 📊 Example

**Before (transcription with BP errors):**
```
O hamartianeamente ptechne factusr ofereciram uma filizofia metafizica ontolojia.
```

**After (refined with BP corrections):**
```
O hamartiano techne actus ofereceram uma filosofia metafísica ontologia.
```

## �� Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
ollama list

# Pull the model if needed
ollama pull llama3.2:latest

# Start Ollama service if needed
ollama serve
```

### File Issues
- Ensure your `.txt` files are UTF-8 encoded
- Place files in the `input/` folder
- Output files will appear in `output/` with "refined_" prefix

## 📄 License

This project is open source and available under the MIT license.

---

🇧🇷 **Sistema brasileiro para filosofia brasileira!** ✨
