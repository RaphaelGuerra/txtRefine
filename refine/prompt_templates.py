"""
Advanced prompt templates for philosophical text refinement.
Provides specialized prompts for different types of philosophical content.
"""

from typing import Dict, Optional
from enum import Enum


class PhilosophyStyle(Enum):
    """Types of philosophical content."""
    SCHOLASTIC = "scholastic"
    CONTEMPORARY = "contemporary"
    LECTURE = "lecture"
    DIALOGUE = "dialogue"
    COMMENTARY = "commentary"
    TREATISE = "treatise"


class PromptTemplates:
    """Collection of specialized prompt templates for philosophical texts."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.context_templates = self._initialize_context_templates()
    
    def _initialize_templates(self) -> Dict[PhilosophyStyle, str]:
        """Initialize prompt templates for different styles."""
        return {
            PhilosophyStyle.SCHOLASTIC: """Você é um especialista em filosofia medieval e escolástica, com profundo conhecimento de latim, grego e português acadêmico.

CONTEXTO: Esta é uma transcrição de conteúdo sobre filosofia escolástica que pode incluir:
- Referências a autores medievais (Tomás de Aquino, Duns Scotus, Pedro Lombardo, etc.)
- Termos técnicos em latim (quidditas, haecceitas, esse, ens, etc.)
- Estrutura argumentativa silogística
- Citações de textos clássicos e patrísticos

SUA TAREFA: Refinar a transcrição corrigindo APENAS:
1. Erros de transcrição em termos filosóficos (ex: "Colássica" → "Escolástica")
2. Termos latinos mal transcritos (ex: "a priore" → "a priori")
3. Nomes de autores incorretos (ex: "Thomas" → "Tomás")
4. Estruturas gramaticais quebradas pela transcrição
5. Pontuação inadequada que prejudica o argumento lógico

PRESERVE ABSOLUTAMENTE:
- A estrutura argumentativa original (premissas, conclusões, objeções, respostas)
- Todas as citações e referências
- O estilo didático e explicativo
- A sequência lógica dos argumentos
- Exemplos e analogias utilizados
- Termos técnicos específicos da tradição escolástica

ATENÇÃO ESPECIAL para:
- Distinções escolásticas (distinctio formalis, distinctio realis, etc.)
- Fórmulas latinas completas (S.T. I-II, q. 90, a. 1, ad 2)
- Estrutura questio disputata (videtur quod, sed contra, respondeo)

Transcrição (parte {chunk_num} de {total_chunks}):

{chunk}

Refine mantendo TOTAL fidelidade ao conteúdo filosófico original:""",

            PhilosophyStyle.CONTEMPORARY: """Você é um especialista em filosofia contemporânea brasileira e portuguesa, familiarizado com a obra de Olavo de Carvalho e a tradição filosófica lusófona.

CONTEXTO: Esta é uma transcrição de filosofia contemporânea que pode incluir:
- Referências a filósofos modernos e contemporâneos
- Discussões sobre fenomenologia, existencialismo, hermenêutica
- Críticas culturais e políticas
- Linguagem coloquial misturada com termos técnicos

SUA TAREFA: Refinar corrigindo APENAS:
1. Erros óbvios de transcrição
2. Palavras incompletas ou mal captadas
3. Termos filosóficos incorretos
4. Problemas de pontuação que afetam a compreensão

PRESERVE COMPLETAMENTE:
- O tom e estilo pessoal do autor/professor
- Expressões idiomáticas e coloquialismos intencionais
- Críticas e posicionamentos
- Exemplos contemporâneos
- Referências culturais brasileiras

Transcrição (parte {chunk_num} de {total_chunks}):

{chunk}

Refine preservando o estilo e conteúdo original:""",

            PhilosophyStyle.LECTURE: """Você é um especialista em transcrição de aulas de filosofia, compreendendo a dinâmica oral do ensino filosófico.

CONTEXTO: Esta é a transcrição de uma AULA de filosofia que inclui:
- Explicações didáticas e repetições pedagógicas
- Interações com alunos (perguntas e respostas)
- Digressões e exemplos espontâneos
- Marcadores discursivos orais ("então", "né", "veja bem", "quer dizer")
- Pausas e reformulações típicas da fala

SUA TAREFA: Refinar corrigindo APENAS:
1. Erros claros de transcrição automática
2. Palavras cortadas ou mal captadas
3. Pontuação que prejudica a compreensão
4. Separação incorreta de turnos de fala

PRESERVE INTEGRALMENTE:
- O caráter oral e espontâneo
- Repetições didáticas intencionais
- Perguntas retóricas
- Exemplos improvisados
- Marcadores conversacionais
- Mudanças de tom (ironia, ênfase, questionamento)
- Indicações de interação ("como vocês sabem", "lembram quando")

FORMATAÇÃO:
- Use "Professor:" para falas do docente
- Use "Aluno:" para intervenções de estudantes
- Use [...] para pausas longas ou trechos inaudíveis
- Mantenha exclamações e interrogações conforme o tom original

Transcrição da aula (parte {chunk_num} de {total_chunks}):

{chunk}

Refine mantendo o caráter oral e didático:""",

            PhilosophyStyle.DIALOGUE: """Você é um especialista em diálogos filosóficos, compreendendo a estrutura dialética e maiêutica.

CONTEXTO: Este é um DIÁLOGO filosófico que apresenta:
- Múltiplos interlocutores com posições distintas
- Estrutura pergunta-resposta
- Desenvolvimento dialético de argumentos
- Possíveis referências ao método socrático

SUA TAREFA: Refinar corrigindo:
1. Atribuição incorreta de falas
2. Erros de transcrição em termos filosóficos
3. Quebras na estrutura dialógica
4. Pontuação inadequada para diálogos

PRESERVE:
- A identidade e caracterização de cada interlocutor
- O desenvolvimento lógico do diálogo
- Ironias e recursos retóricos
- A progressão argumentativa

Transcrição do diálogo (parte {chunk_num} de {total_chunks}):

{chunk}

Refine preservando a estrutura dialógica:""",

            PhilosophyStyle.COMMENTARY: """Você é um especialista em comentários filosóficos e exegese textual.

CONTEXTO: Este é um COMENTÁRIO filosófico que inclui:
- Análise linha por linha de um texto clássico
- Citações do texto original intercaladas com explicações
- Referências cruzadas a outros comentadores
- Notas interpretativas e esclarecimentos

SUA TAREFA: Refinar corrigindo:
1. Erros nas citações do texto comentado
2. Confusão entre texto original e comentário
3. Referências bibliográficas incorretas
4. Termos técnicos mal transcritos

PRESERVE:
- A distinção clara entre texto original e comentário
- Todas as referências e notas
- A estrutura analítica
- Interpretações e glosas

FORMATAÇÃO:
- Use aspas ou itálico para o texto original comentado
- Mantenha numeração de linhas ou parágrafos se houver
- Preserve indicações como "cf.", "vide", "op. cit."

Transcrição do comentário (parte {chunk_num} de {total_chunks}):

{chunk}

Refine mantendo a estrutura de comentário:""",

            PhilosophyStyle.TREATISE: """Você é um especialista em tratados filosóficos sistemáticos.

CONTEXTO: Este é um TRATADO filosófico formal com:
- Estrutura sistemática (livros, capítulos, seções, parágrafos numerados)
- Argumentação rigorosa e técnica
- Definições precisas e demonstrações
- Aparato crítico (notas, referências)

SUA TAREFA: Refinar corrigindo:
1. Erros em termos técnicos especializados
2. Quebras na numeração estrutural
3. Inconsistências nas referências internas
4. Problemas de formatação hierárquica

PRESERVE:
- Toda a estrutura formal (I.1.§2, etc.)
- Definições e axiomas exatamente como estão
- Demonstrações e corolários
- Notas de rodapé e referências
- Formalismo lógico se houver

Transcrição do tratado (parte {chunk_num} de {total_chunks}):

{chunk}

Refine preservando o rigor formal:"""
        }
    
    def _initialize_context_templates(self) -> Dict[str, str]:
        """Initialize context-aware additions to prompts."""
        return {
            "with_latin": """
ATENÇÃO ESPECIAL para termos latinos:
- Corrija grafias incorretas (ex: "caussа sui" → "causa sui")
- Preserve declinações latinas corretas
- Mantenha expressões latinas completas juntas
- Corrija apenas erros óbvios de transcrição, não "modernize" o latim
""",
            
            "with_greek": """
ATENÇÃO para termos gregos (transliterados):
- Corrija transliterações inconsistentes (ex: "lógos" e "logos" → escolha uma)
- Preserve acentos gregos quando usados (ἀλήθεια, λόγος)
- Mantenha consistência na romanização
""",
            
            "with_citations": """
FORMATAÇÃO de citações:
- Preserve referências bibliográficas exatamente
- Mantenha abreviações acadêmicas (op. cit., ibid., cf., apud)
- Corrija apenas erros óbvios em nomes de autores conhecidos
- Preserve numeração de páginas, volumes, edições
""",
            
            "with_formulas": """
NOTAÇÃO lógica e formal:
- Preserve símbolos lógicos (∀, ∃, →, ↔, ¬, ∧, ∨)
- Mantenha fórmulas e equações intactas
- Corrija apenas erros tipográficos óbvios
- Preserve numeração de proposições e teoremas
""",
            
            "with_examples": """
EXEMPLOS e analogias:
- Mantenha todos os exemplos, mesmo que pareçam estranhos
- Preserve analogias e metáforas exatamente como foram ditas
- Não "melhore" ou "esclareça" exemplos
- Corrija apenas erros gramaticais óbvios
"""
        }
    
    def get_prompt(self, 
                   style: PhilosophyStyle,
                   chunk: str,
                   chunk_num: int,
                   total_chunks: int,
                   context_additions: Optional[list] = None) -> str:
        """
        Get appropriate prompt for the philosophical content style.
        
        Args:
            style: Type of philosophical content
            chunk: Text chunk to refine
            chunk_num: Current chunk number
            total_chunks: Total number of chunks
            context_additions: List of additional context templates to include
        
        Returns:
            Formatted prompt string
        """
        base_prompt = self.templates[style]
        
        # Add context-specific additions
        if context_additions:
            additions = "\n".join([
                self.context_templates[ctx] 
                for ctx in context_additions 
                if ctx in self.context_templates
            ])
            base_prompt = base_prompt.replace(
                "Transcrição",
                additions + "\nTranscrição"
            )
        
        # Format with chunk information
        return base_prompt.format(
            chunk=chunk,
            chunk_num=chunk_num,
            total_chunks=total_chunks
        )
    
    def detect_style(self, text: str) -> PhilosophyStyle:
        """
        Attempt to detect the style of philosophical content.
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected PhilosophyStyle
        """
        text_lower = text.lower()
        
        # Check for dialogue markers
        if any(marker in text for marker in [":", "—", "Sócrates:", "Aluno:", "Professor:"]):
            if text.count(":") > 5 or "professor:" in text_lower or "aluno:" in text_lower:
                return PhilosophyStyle.LECTURE
            return PhilosophyStyle.DIALOGUE
        
        # Check for scholastic markers
        scholastic_markers = [
            "quidditas", "haecceitas", "tomás de aquino", "suma teológica",
            "pedro lombardo", "escolástica", "silogismo", "quididade"
        ]
        if sum(1 for marker in scholastic_markers if marker in text_lower) >= 2:
            return PhilosophyStyle.SCHOLASTIC
        
        # Check for formal structure
        if any(marker in text for marker in ["§", "Capítulo", "Seção", "Livro I", "Parte I"]):
            return PhilosophyStyle.TREATISE
        
        # Check for commentary markers
        if "comentário" in text_lower or "glosa" in text_lower or "cf." in text:
            return PhilosophyStyle.COMMENTARY
        
        # Check for contemporary markers
        contemporary_markers = [
            "fenomenologia", "existencialismo", "hermenêutica",
            "pós-moderno", "desconstrução", "olavo de carvalho"
        ]
        if any(marker in text_lower for marker in contemporary_markers):
            return PhilosophyStyle.CONTEMPORARY
        
        # Default to lecture style as most common
        return PhilosophyStyle.LECTURE
    
    def detect_context_needs(self, text: str) -> list:
        """
        Detect what additional context templates are needed.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of context template keys needed
        """
        needs = []
        text_lower = text.lower()
        
        # Check for Latin
        latin_indicators = [
            "a priori", "a posteriori", "per se", "qua", "ergo",
            "sine qua non", "ipso facto", "ad hominem"
        ]
        if any(indicator in text_lower for indicator in latin_indicators):
            needs.append("with_latin")
        
        # Check for Greek
        greek_indicators = ["logos", "nous", "psyche", "physis", "telos"]
        if any(indicator in text_lower for indicator in greek_indicators):
            needs.append("with_greek")
        
        # Check for citations
        if any(marker in text for marker in ["(", "cf.", "op. cit.", "apud", "p.", "pp."]):
            needs.append("with_citations")
        
        # Check for logical formulas
        if any(symbol in text for symbol in ["∀", "∃", "→", "¬", "∧", "∨"]):
            needs.append("with_formulas")
        
        # Check for examples
        if "por exemplo" in text_lower or "exemplo:" in text_lower:
            needs.append("with_examples")
        
        return needs