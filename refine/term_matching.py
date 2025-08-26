"""Normalization and term matching utilities for philosophical terms.

This module provides:
- normalize_text: lowercases and strips accents/diacritics
- REFINED_DICT: compact canonical dictionary of categories to normalized entries
- CORRECTIONS_MAP: targeted corrections for hallucinations and common OCR/ASR errors
- find_best_match: applies corrections, then exact/fuzzy matching within a category
"""

from typing import List, Optional
import unicodedata
from difflib import get_close_matches


def normalize_text(text: str) -> str:
    """Lowercase, trim, and strip accents/diacritics for robust matching."""
    if not text:
        return ""
    text = text.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )


# Cleaned canonical dictionary (normalized values)
REFINED_DICT = {
    "philosophers_ancient_medieval": [
        "socrates", "platao", "aristoteles", "heraclito", "parmenides", "democrito",
        "pitagoras", "tales", "anaximandro", "anaximenes", "protagoras", "gorgias",
        "zenao de eleia", "empedocles", "anaxagoras", "leucipo", "melisso",
        "agostinho de hipona", "justino martir", "ireneu de lyon", "tertuliano",
        "hipolito", "cipriano", "origines", "clemente de alexandria",
        "atanasio de alexandria", "basilio de cesareia", "gregorio nazianzeno",
        "gregorio de nissa", "joao crisostomo", "jeronimo", "tomas de aquino",
        "duns scotus", "boecio", "pedro lombardo", "anselmo de cantuaria",
        "boaventura", "alberto magno", "roger bacon", "guilherme de ockham",
        "joao buridano", "mestre eckhart", "tomas bradwardine", "roberto grosseteste",
        "averrois", "avicena", "algazel", "maimonides", "francisco suarez",
        "tomas caetano", "joao de sao tomas", "bernardo de claraval",
        "pedro abelardo", "joao escoto erigena", "alcuino de iorque", "carlos magno"
    ],
    "philosophers_modern_contemporary": [
        "rene descartes", "baruch spinoza", "gottfried wilhelm leibniz", "john locke",
        "george berkeley", "david hume", "thomas hobbes", "blaise pascal",
        "nicolas malebranche", "immanuel kant", "johann gottlieb fichte",
        "friedrich wilhelm joseph schelling", "georg wilhelm friedrich hegel",
        "soren kierkegaard", "arthur schopenhauer", "karl marx", "friedrich engels",
        "friedrich nietzsche", "wilhelm dilthey", "edmund husserl",
        "martin heidegger", "jean-paul sartre", "simone de beauvoir", "albert camus",
        "maurice merleau-ponty", "emmanuel levinas", "hannah arendt",
        "gottlob frege", "bertrand russell", "ludwig wittgenstein",
        "michel foucault", "jacques derrida", "gilles deleuze", "felix guattari",
        "judith butler", "byung-chul han", "slavoj zizek", "jurgen habermas",
        "theodor adorno", "walter benjamin", "jacques lacan", "giorgio agamben",
        "max horkheimer", "herbert marcuse", "georges bataille", "maurice blanchot",
        "jean baudrillard", "paul virilio", "saul kripke", "thomas kuhn",
        "paul feyerabend", "karl popper", "john searle", "daniel dennett",
        "richard rorty", "martha nussbaum", "peter singer", "marshall mcluhan",
        "donna haraway", "nick bostrom", "luciano floridi", "ray kurzweil"
    ],
    "philosophers_brazilian": [
        "olavo de carvalho", "vicente ferreira da silva", "mario ferreira dos santos",
        "miguel reale", "tobias barreto", "silvio romero", "farias brito",
        "vilem flusser", "gerd bornheim", "newton da costa", "ubiratan dambrosio",
        "jose arthur giannotti", "marilena chaui", "paulo arantes", "roberto romano",
        "vladimir safatle", "leandro konder", "benedito nunes", "paulo freire",
        "sueli carneiro", "djamila ribeiro", "silvio almeida", "olgaria matos",
        "oswaldo giacoia junior", "benedito prado junior"
    ],
    "concepts_ancient_latin": [
        "logos", "nous", "physis", "arete", "eudaimonia", "mythos", "kosmos", "arche",
        "doxa", "episteme", "sophia", "techne", "hamartia", "anagnorisis", "catharsis",
        "suma teologica", "hilemorfismo", "tomismo", "nominalismo", "analogia entis",
        "actus purus", "forma substancial", "materia prima", "quinque viae",
        "transcendentais", "voluntarismo", "iluminacao divina", "prova ontologica",
        "livro das sentencas", "esse", "ens", "quidditas", "haecceitas", "substantia",
        "potentia", "a priori", "a posteriori", "cogito ergo sum", "tabula rasa",
        "res cogitans", "res extensa", "causa sui", "per se"
    ],
    "concepts_modern_contemporary": [
        "ser-ai", "ser e tempo", "alem-do-homem", "vontade de potencia", "eterno retorno",
        "desconstrucao", "mais-valia", "jogos de linguagem", "fenomenologia",
        "pos-estruturalismo", "industria cultural", "biopolitica", "rizoma",
        "corpo sem orgaos", "desterritorializacao", "simulacro", "agir comunicativo",
        "esfera publica", "banalidade do mal", "arqueologia do saber",
        "genealogia do poder", "microfisica do poder", "panoptico", "differance",
        "logocentrismo", "falseabilidade", "incomensurabilidade", "transumanismo",
        "singularidade tecnologica", "argumento da sala chinesa", "problema do bonde",
        "qualia", "teoria da simulacao", "pos-humanismo", "filosofia da mente",
        "filosofia da ciencia", "sociedade do espetaculo", "o meio e a mensagem",
        "aldeia global", "risco existencial", "infosfera", "etica da informacao",
        "antropofagia cultural", "homem cordial"
    ]
}


# Targeted corrections for AI hallucinations and common OCR/ASR errors
CORRECTIONS_MAP = {
    # AI hallucination endings
    "justanous": "justamente",
    "evidentenous": "evidentemente",
    "precisanous": "precisamente",
    "historicanous": "historicamente",
    "hamartianeanous": "erroneamente",
    "temporarianous": "temporariamente",
    "exatanous": "exatamente",
    # Common OCR/ASR misreads
    "neo tomismo": "neotomismo",
    "dialetica": "dialética",
    "epistimologia": "epistemologia",
    "ontolojia": "ontologia",
    "metafizica": "metafísica",
}


def find_best_match(term: str, category: str, cutoff: float = 0.8) -> Optional[str]:
    """Return best normalized match from a category, or None.

    Steps:
    1) Normalize input
    2) Apply targeted corrections if available
    3) Exact match in category
    4) Fuzzy match using difflib
    """
    norm_term = normalize_text(term)

    if not norm_term or category not in REFINED_DICT:
        return None

    # Step 1: Apply corrections
    if norm_term in CORRECTIONS_MAP:
        norm_term = normalize_text(CORRECTIONS_MAP[norm_term])

    # Step 2: Exact match
    if norm_term in REFINED_DICT[category]:
        return norm_term

    # Step 3: Fuzzy match
    matches: List[str] = get_close_matches(norm_term, REFINED_DICT[category], n=1, cutoff=cutoff)
    return matches[0] if matches else None


