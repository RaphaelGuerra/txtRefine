# Text Refinement Program for Portuguese Philosophy Classes

Este programa refina transcrições de aulas de filosofia em Português Brasileiro usando um modelo Ollama local. Foi especificamente desenvolvido para transcrições de aulas de filosofia, como as de Olavo de Carvalho, mantendo a fidelidade absoluta ao conteúdo original enquanto corrige erros de transcrição e melhora a clareza.

## ✨ Características

- **Fidelidade ao Original**: Mantém todas as ideias filosóficas e o estilo do professor
- **Correção Inteligente**: Corrige erros gramaticais, palavras mal transcritas e frases quebradas
- **Processamento em Chunks**: Divide textos longos em partes gerenciáveis para melhor qualidade
- **Especialização Filosófica**: Prompt otimizado para conteúdo filosófico e escolástico
- **Interface Amigável**: Barra de progresso e estatísticas detalhadas
- **Fallback Seguro**: Em caso de erro, mantém o texto original

## 🚀 Como Executar

### 1. Instalar Ollama
Baixe e instale o Ollama de [https://ollama.com/download](https://ollama.com/download)

### 2. Baixar o Modelo
Execute no terminal para o modelo padrão:
```bash
ollama pull gemma:2b
```

Para outros modelos (recomendado para filosofia):
```bash
ollama pull llama2:7b
ollama pull gemma:7b
ollama pull mistral:7b
```

### 3. Instalar Dependências Python
Navegue até a pasta raiz do projeto e execute:
```bash
pip3 install -r requirements.txt
```

### 4. Colocar Arquivos de Transcrição
Coloque seus arquivos `.txt` de transcrição na pasta `input/`

### 5. Executar o Refinamento
```bash
# Processar todos os arquivos com modelo padrão
python3 src/refine.py

# Usar modelo específico
python3 src/refine.py --model llama2:7b

# Processar arquivo específico
python3 src/refine.py --files minha_aula.txt

# Processar múltiplos arquivos com modelo específico
python3 src/refine.py --model gemma:7b --files aula1.txt aula2.txt
```

## 📁 Estrutura do Projeto

```
txtRefine/
├── input/                    # Arquivos de transcrição originais
├── output/                   # Arquivos refinados (prefixo "refined_")
├── src/
│   └── refine.py            # Script principal de refinamento
├── requirements.txt          # Dependências Python
└── README.md                # Este arquivo
```

## 🎯 Casos de Uso

### Transcrições de Aulas de Filosofia
- **Escolástica Medieval**: Santo Tomás de Aquino, São Boaventura, Pedro Abelardo
- **Filosofia Contemporânea**: Olavo de Carvalho, cursos e seminários
- **Conteúdo Acadêmico**: Palestras, conferências, debates filosóficos

### O que o Programa Corrige
- ✅ Erros gramaticais do português
- ✅ Palavras mal transcritas ou incompletas
- ✅ Frases quebradas ou mal estruturadas
- ✅ Termos filosóficos incorretos
- ✅ Quebras de linha inadequadas

### O que o Programa NÃO Altera
- ❌ Conteúdo filosófico original
- ❌ Estrutura da argumentação
- ❌ Estilo e tom do professor
- ❌ Exemplos e citações
- ❌ Comprimento do texto

## 🔧 Modelos Recomendados

| Modelo | Tamanho | Qualidade | Velocidade | Recomendação |
|--------|---------|-----------|------------|--------------|
| `neural-chat:latest` | 4.1 GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | **Melhor qualidade** para filosofia |
| `openchat:latest` | 4.1 GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | **Excelente** para conteúdo acadêmico |
| `llama3.2:latest` | 2.0 GB | ⭐⭐⭐⭐ | ⚡⚡⚡ | **Equilibrado** - boa qualidade e velocidade |
| `dolphin-phi:latest` | 1.6 GB | ⭐⭐⭐⭐ | ⚡⚡⚡ | **Rápido** com boa qualidade |
| `gemma:2b` | 1.7 GB | ⭐⭐⭐ | ⚡⚡⚡⚡ | **Mais rápido** para tarefas básicas |

### 🆕 **Modelos Open Source de Alta Qualidade**

O programa agora inclui suporte para modelos open source de última geração:

- **Neural Chat**: Modelo de alta qualidade otimizado para chat e instruções
- **OpenChat**: Excelente modelo open source com capacidades de raciocínio
- **Llama 3.2**: Último modelo open source da Meta com forte performance
- **Dolphin Phi**: Modelo Phi da Microsoft otimizado para seguir instruções

### 🔍 **Comparação de Modelos**

Use o script de comparação para testar diferentes modelos no mesmo arquivo:

```bash
# Comparar todos os modelos disponíveis
python3 compare_models.py

# Comparar usando arquivo específico
python3 compare_models.py input/minha_aula.txt
```

O script fornece métricas detalhadas sobre:
- **Preservação de conteúdo** (diferença de caracteres)
- **Velocidade de processamento**
- **Qualidade da saída**
- **Recomendação balanceada**

## 📊 Exemplo de Saída

**Antes (transcrição original):**
```
O pressuposto da existência da Colássica são dois. Primeiro, a existência dessas vastas compilações de textos que acabaram tomando o título de livros de sentenças, dos quais o mais famoso foi de um sujeito chamado Pedro Lombardo...
```

**Depois (refinado):**
```
O pressuposto da existência da Escolástica são dois. Primeiro, a existência dessas vastas compilações de textos que acabaram tomando o título de livros de sentenças, dos quais o mais famoso foi de um sujeito chamado Pedro Lombardo...
```

## 🚨 Solução de Problemas

### Ollama não está rodando
```bash
# Iniciar Ollama
ollama serve

# Em outro terminal, verificar modelos disponíveis
ollama list
```

### Modelo não encontrado
```bash
# Baixar modelo específico
ollama pull nome_do_modelo

# Ver modelos disponíveis
ollama list
```

### Erro de memória
- Use modelos menores (2B em vez de 7B)
- Feche outros programas que consumam RAM
- Reinicie o Ollama

## 🤝 Contribuições

Este projeto está aberto a contribuições! Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para:

1. Abrir uma issue no GitHub
2. Fazer um fork e submeter um pull request
3. Sugerir melhorias no prompt de refinamento

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🙏 Agradecimentos

- Ollama por fornecer a infraestrutura de modelos locais
- Comunidade de filosofia brasileira por inspirar este projeto
- Todos os contribuidores que ajudaram a melhorar o programa

---

**Nota**: Este programa foi desenvolvido especificamente para transcrições de filosofia em português, mas pode ser adaptado para outros idiomas e tipos de conteúdo modificando o prompt de refinamento.