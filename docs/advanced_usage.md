# Uso Avançado do txtRefine

Este documento cobre recursos avançados e configurações do txtRefine.

## Configuração Avançada

### Arquivo de Configuração

Crie um arquivo `config.json` na raiz do projeto:

```json
{
  "default_model": "llama3.2:latest",
  "max_words_per_chunk": 800,
  "parallel_processing": false,
  "cache_refinements": true,
  "progress_bar": true,
  "preserve_academic_terms": true
}
```

### Variáveis de Configuração

- `default_model`: Modelo padrão do Ollama
- `max_words_per_chunk`: Tamanho máximo de cada chunk
- `parallel_processing`: Processamento paralelo (experimental)
- `cache_refinements`: Cache de refinamentos para evitar reprocessamento
- `progress_bar`: Mostrar barra de progresso
- `preserve_academic_terms`: Preservar termos acadêmicos específicos

## Otimização de Performance

### Ajuste de Chunk Size

Para textos muito longos, ajuste o tamanho dos chunks:

```bash
# Para textos complexos, use chunks menores
echo '{"max_words_per_chunk": 600}' > config.json

# Para textos simples, use chunks maiores
echo '{"max_words_per_chunk": 1000}' > config.json
```

### Cache de Refinamentos

O sistema pode cachear refinamentos para evitar reprocessamento:

```json
{
  "cache_refinements": true,
  "cache_dir": "cache"
}
```

### Seleção de Modelo por Tipo de Texto

Diferentes modelos funcionam melhor para diferentes tipos de texto:

- **llama3.2:latest**: Equilíbrio geral
- **neural-chat:latest**: Melhor qualidade filosófica
- **openchat:latest**: Excelente para acadêmico
- **dolphin-phi:latest**: Mais rápido

## Solução de Problemas

### Problemas Comuns

1. **Modelo não encontrado**:
   ```bash
   ollama pull llama3.2:latest
   ```

2. **Memória insuficiente**:
   - Use modelos menores (2B em vez de 7B)
   - Feche outros programas
   - Reinicie o Ollama

3. **Chunks muito grandes**:
   - Reduza `max_words_per_chunk` no config.json
   - Use um modelo com maior contexto

### Logs e Debug

Para debugging detalhado:

```bash
# Ative logging verboso
echo '{"verbose_logging": true}' > config.json

# Verifique logs do Ollama
ollama logs
```

## Customização de Prompts

### Template Personalizado

Para especializar o prompt para seu caso de uso:

```python
# Modifique PHILOSOPHY_REFINEMENT_PROMPT em refine.py
CUSTOM_PROMPT = """Você é um especialista em [SEU_ASSUNTO].
Sua tarefa é refinar transcrições mantendo...
"""
```

### Preservação de Termos Específicos

Adicione termos que devem ser preservados exatamente:

```json
{
  "preserve_academic_terms": true,
  "custom_terms": ["escolástica", "metafísica", "ontologia"]
}
```

## Automação e Integração

### Scripts de Automação

Exemplo de script para processamento em lote:

```bash
#!/bin/bash
# process_batch.sh
for file in input/*.txt; do
    echo "Processando $file..."
    python refine.py --input "$file" --model llama3.2:latest
done
```

### Integração com Outros Sistemas

O txtRefine pode ser integrado com:

- **Sistemas de gerenciamento de documentos**
- **Plataformas de e-learning**
- **Workflows de processamento de texto**
- **APIs REST** (com modificações)

## Métricas e Análise

### Estatísticas de Processamento

O programa fornece estatísticas detalhadas:

- Tempo de processamento por arquivo
- Taxa de palavras por segundo
- Percentual de alteração
- Detecção de perda de conteúdo

### Análise de Qualidade

Para avaliar a qualidade dos refinamentos:

1. Compare amostras antes/depois
2. Verifique preservação de termos técnicos
3. Avalie fluidez e gramática
4. Teste com diferentes modelos

## Desenvolvimento

### Estrutura do Código

```
txtRefine/
├── refine.py           # Programa principal
├── config.py           # Configuração
├── tests/              # Testes
├── docs/               # Documentação
└── input/output/       # Dados
```

### Contribuição

Para contribuir:

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Testes

Execute os testes:

```bash
# Todos os testes
make test

# Com cobertura
make test-cov

# Testes específicos
pytest tests/test_refine.py::TestTextProcessing::test_clean_text
```
