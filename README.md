# txtRefine - Refinamento Inteligente de Transcrições

Programa interativo para refinar transcrições de aulas de filosofia e conteúdo acadêmico em Português Brasileiro. Mantém fidelidade absoluta ao original enquanto corrige erros de transcrição.

## ✨ Características

- **Fidelidade ao Original**: Mantém todas as ideias filosóficas e o estilo do professor
- **Correção Inteligente**: Corrige erros gramaticais, palavras mal transcritas e frases quebradas
- **Processamento em Chunks**: Divide textos longos em partes gerenciáveis para melhor qualidade
- **Especialização Filosófica**: Prompt otimizado para conteúdo filosófico e escolástico
- **Interface Amigável**: Barra de progresso e estatísticas detalhadas
- **Fallback Seguro**: Em caso de erro, mantém o texto original

## 🚀 Como Usar

### 1. Instalar Ollama
Baixe e instale o Ollama de [https://ollama.com/download](https://ollama.com/download)

### 2. Baixar o Modelo
Execute no terminal para o modelo padrão:
```bash
ollama pull llama3.2:latest
```

### 3. Instalar Dependências Python
```bash
pip3 install -r requirements.txt
```

### 4. Colocar Arquivos de Transcrição
Coloque seus arquivos `.txt` de transcrição na pasta `input/`

### 5. Executar o Refinamento
```bash
# Execute o programa principal
python3 refine.py
```

Siga os menus interativos para escolher modelo, arquivos e opções.

## 📁 Estrutura do Projeto

```
txtRefine/
├── input/                    # Arquivos de transcrição originais
├── output/                   # Arquivos refinados (prefixo "refined_")
├── refine.py                 # Programa principal (tudo-em-um)
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

O programa suporta todos os modelos Ollama disponíveis. Recomendamos:

- **`llama3.2:latest`** (padrão) - Equilibrado entre qualidade e velocidade
- **`neural-chat:latest`** - Melhor qualidade para filosofia
- **`openchat:latest`** - Excelente para conteúdo acadêmico
- **`dolphin-phi:latest`** - Rápido com boa qualidade

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