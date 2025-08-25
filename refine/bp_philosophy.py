"""
Brazilian Portuguese Philosophical Terminology System
Comprehensive BP corrections and philosophical term handling.
"""

from typing import Dict, List, Set, Tuple, Any
import re
from difflib import get_close_matches


class BPPhilosophySystem:
    """Complete BP philosophical terminology and correction system."""
    
    def __init__(self):
        """Initialize the BP philosophy system."""
        self._setup_terms_database()
        self._setup_bp_patterns()
    
    def _setup_terms_database(self):
        """Setup the comprehensive philosophical terms database."""
        # Core philosophical terms in Portuguese
        self.portuguese_terms = {
            # Classical Greek terms
            "logos": ["lógos", "logos"],
            "nous": ["noûs", "nous"],
            "physis": ["phýsis", "physis", "fisis"],
            "aretē": ["areté", "aretê", "virtude"],
            "eudaimonia": ["eudaimonia", "eudaimônia", "felicidade"],
            "mythos": ["mýthos", "mythos", "mito"],
            "kosmos": ["kósmos", "kosmos", "cosmos"],
            "arche": ["arché", "princípio"],
            "doxa": ["dóxa", "doxa", "opinião"],
            "episteme": ["epistéme", "episteme", "conhecimento"],
            "sophia": ["sophía", "sophia", "sabedoria"],
            "techne": ["téchne", "techne", "arte", "técnica"],
            "hamartia": ["hamartía", "hamartia", "erro"],
            "anagnorisis": ["anagnórisis", "anagnorisis", "reconhecimento"],
            "peripeteia": ["peripeteía", "peripeteia", "reviravolta"],
            "catharsis": ["kátharsis", "catharsis", "catarse"],

            # Latin/Scholastic terms
            "esse": ["essse", "esse"],
            "ens": ["enz", "ens"],
            "quidditas": ["quidditas", "quididade"],
            "haecceitas": ["haecceitas", "heceidade"],
            "substantia": ["substantia", "substância"],
            "accidens": ["accidens", "acidente"],
            "qualitas": ["qualitas", "qualidade"],
            "quantitas": ["quantitas", "quantidade"],
            "relatio": ["relatio", "relação"],
            "modus": ["modus", "modalidade"],
            "causa": ["cauza", "causa"],
            "efficientia": ["efficientia", "eficiência"],
            "finalitas": ["finalitas", "finalidade"],
            "formalitas": ["formalitas", "formalidade"],
            "materialitas": ["materialitas", "materialidade"],

            # Logic terms
            "premissa": ["premisa", "premíssa"],
            "conclusão": ["concluzão", "conclusao"],
            "inferência": ["inferencia", "enferência"],
            "dedução": ["deducção", "dedusão"],
            "indução": ["induccão", "indusão"],
            "falácia": ["falacia", "falásia"],
            "proposição": ["proposicão", "proposisão"],
            "juízo": ["juizo", "juíso"],
            "conceito": ["conseito", "concêito"],
            "categoria": ["categória", "cathegoria"],

            # Ethics terms
            "virtude": ["virtude", "virtude"],
            "dever": ["dever", "dever"],
            "obrigação": ["obrigação", "obrigação"],
            "responsabilidade": ["responsabilidade", "responsabilidade"],
            "autonomia": ["autonomia", "autonomia"],
            "heteronomia": ["heteronomia", "heteronomia"],
            "imperativo": ["imperativo", "imperativo"],
            "categórico": ["categórico", "categórico"],
        }

        # Latin terms commonly used
        self.latin_terms = {
            "a priori": ["apriori", "a priore"],
            "a posteriori": ["aposteriori", "a posteriore"],
            "ad hominem": ["ad hominen", "ad ominem"],
            "ad infinitum": ["ad infinitun", "adinfinitum"],
            "cogito ergo sum": ["cogito ergosum", "cogito ergossum"],
            "causa sui": ["causa sui", "cauza sui"],
            "ens": ["enz", "hens"],
            "esse": ["essse", "esse"],
            "quidditas": ["quidditas", "quididade"],
            "haecceitas": ["haecceitas", "heceidade"],
            "substantia": ["substantia", "substância"],
            "accidens": ["accidens", "acidente"],
            "qualitas": ["qualitas", "qualidade"],
            "quantitas": ["quantitas", "quantidade"],
            "relatio": ["relatio", "relação"],
            "modus": ["modus", "modalidade"],
            "actus": ["actus", "ato"],
            "potentia": ["potentia", "potência"],
            "forma": ["forma", "forma"],
            "materia": ["materia", "matéria"],
            "anima": ["anima", "alma"],
            "intellectus": ["intellectus", "intelecto"],
            "voluntas": ["voluntas", "vontade"],
            "bonum": ["bonum", "bem"],
            "verum": ["verum", "verdade"],
            "unum": ["unum", "uno"],
        }

        # Classical Greek philosophers and terms
        self.greek_philosophers = {
            "Sócrates": ["Socrates", "Socrátes", "Sokrates"],
            "Platão": ["Plato", "Platón", "Platon"],
            "Aristóteles": ["Aristotle", "Aristoteles", "Aristóteles"],
            "Heráclito": ["Heraclitus", "Heráclito"],
            "Parmênides": ["Parmenides", "Parmênides"],
            "Demócrito": ["Democritus", "Demócrito"],
            "Pitágoras": ["Pythagoras", "Pitágoras"],
            "Tales": ["Thales", "Tales"],
            "Anaximandro": ["Anaximander", "Anaximandro"],
            "Anaxímenes": ["Anaximenes", "Anaxímenes"],
        }

        # Patristic authors
        self.patristic_authors = {
            "Agostinho de Hipona": ["Augustine of Hippo", "Santo Agostinho"],
            "Justino Mártir": ["Justin Martyr", "Justino"],
            "Ireneu de Lyon": ["Irenaeus", "Ireneu"],
            "Tertuliano": ["Tertullian", "Tertuliano"],
            "Hipólito": ["Hippolytus", "Hipólito"],
            "Cipriano": ["Cyprian", "São Cipriano"],
            "Orígenes": ["Origen", "Orígenes"],
            "Clemente de Alexandria": ["Clement", "Clemente"],
        }

        # Scholastic philosophers
        self.scholastic_philosophers = {
            "Tomás de Aquino": ["Thomas Aquinas", "Santo Tomás", "São Tomás"],
            "Duns Scotus": ["John Duns Scotus", "João Duns Scotus"],
            "Pedro Lombardo": ["Peter Lombard", "Pedro Lombardo"],
            "Anselmo de Cantuária": ["Anselm", "Anselmo"],
            "Boaventura": ["Bonaventure", "São Boaventura"],
            "Alberto Magno": ["Albert the Great", "Alberto Magno"],
            "Roger Bacon": ["Roger Bacon", "Rogério Bacon"],
        }

        # Contemporary philosophers (Brazilian focus)
        self.contemporary_philosophers = {
            "Olavo de Carvalho": ["Olavo", "Olavo de Carvalho"],
            "José Arthur Giannotti": ["Giannotti", "José Arthur Giannotti"],
            "Marilena Chauí": ["Chauí", "Marilena Chauí"],
            "Paulo Arantes": ["Arantes", "Paulo Arantes"],
            "Roberto Romano": ["Romano", "Roberto Romano"],
            "Gerd Bornheim": ["Bornheim", "Gerd Bornheim"],
            "João Cruz Costa": ["Cruz Costa", "João Cruz Costa"],
        }
        
        self._build_corrections()
    
    def _setup_bp_patterns(self):
        """Setup BP-specific phonetic patterns."""
        self.phonetic_patterns = {
            's/z alternation': {
                'causa': ['causa', 'cauza'],
                'realidade': ['realidade', 'rialidade'],
                'existência': ['existência', 'ezistência'],
                'essência': ['essência', 'ecência'],
                'consciência': ['consciência', 'consciênça'],
                'transcendência': ['transcendência', 'transcendênça'],
                'imanência': ['imanência', 'imanênça']
            },
            'r/l alternation': {
                'filosofia': ['filosofia', 'filozofia'],
                'real': ['real', 'rial'],
                'oral': ['oral', 'oural'],
                'plural': ['plural', 'ploural']
            },
            't/ch alternation': {
                'argumentação': ['argumentação', 'argumetação'],
                'demonstração': ['demonstração', 'dimonstração'],
                'interpretação': ['interpretação', 'intirpretação']
            }
        }

        # Common BP academic expressions
        self.academic_expressions = {
            'quer dizer': ['quer dizer', 'que dizer', 'quedizer'],
            'ou seja': ['ou seja', 'ouseja', 'ouzeja'],
            'isto é': ['isto é', 'itoé', 'iztoé'],
            'por exemplo': ['por exemplo', 'poexemplo', 'porexemplo'],
            'dessa forma': ['dessa forma', 'decacorma', 'decaforma'],
            'na verdade': ['na verdade', 'naverdade', 'na verdadi'],
            'por outro lado': ['por outro lado', 'poutro lado', 'poroutrolado'],
            'em outras palavras': ['em outras palavras', 'emoutraspalavras'],
            'do ponto de vista': ['do ponto de vista', 'dopontodevista', 'dopontodavista']
        }
    
    def _build_corrections(self):
        """Build reverse lookup dictionary for corrections."""
        self.corrections = {}

        # Add all terms to corrections dictionary
        for correct, incorrects in self.portuguese_terms.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        for correct, incorrects in self.latin_terms.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        for correct, incorrects in self.greek_philosophers.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        for correct, incorrects in self.patristic_authors.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        for correct, incorrects in self.scholastic_philosophers.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        for correct, incorrects in self.contemporary_philosophers.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct

        # Add additional BP phonetic variations
        bp_additional_corrections = {
            'cauza': 'causa',
            'rial': 'real',
            'ezistêncial': 'existencial',
            'filizofica': 'filosófica',
            'dezenvolvimento': 'desenvolvimento',
            'proceço': 'processo',
            'conpreensão': 'compreensão',
            'intiretação': 'interpretação',
            # Common transcription errors in philosophical lectures
            'Né de Val': 'medieval',
            'ne de val': 'medieval',
            'Né de Vale': 'medieval',
            'ne de vale': 'medieval',
            'mediebal': 'medieval',
            # Additional corrections for reported errors
            'hamartianeamente': 'hamartiano',
            'ptechne': 'techne',
            'fTomás de Aquinode Tomás de Aquino': 'Tomás de Aquino',
            'factusr': 'actus',
            'ofereciram': 'ofereceram',
            # More common BP errors
            'filizofia': 'filosofia',
            'filozofica': 'filosófica',
            'filozofia': 'filosofia',
            'metafizica': 'metafísica',
            'ontolojia': 'ontologia',
            'epistimologia': 'epistemologia',
            'conhicimento': 'conhecimento',
            'racionalidadi': 'racionalidade',
            'argumetação': 'argumentação',
            'dimonstração': 'demonstração',
            'intirpretação': 'interpretação',
            'comprinensão': 'compreensão',
            'virdade': 'verdade',
            'rialidade': 'realidade',
            'ezistência': 'existência',
            'ecência': 'essência',
            'sustância': 'substância',
            'assidente': 'acidente',
            'qualidadi': 'qualidade',
            'quantidadi': 'quantidade',
            'relason': 'relação',
            'modalidadi': 'modalidade',
            # Scholastic and philosophical terms
            'tomás': 'Tomás de Aquino',
            'aquino': 'Aquino',
            'aristóteles': 'Aristóteles',
            'platão': 'Platão',
            'sócrates': 'Sócrates',
            'agostinho': 'Agostinho',
            'actus': 'ato',
            'potentia': 'potência',
            'essentia': 'essência',
            'existentia': 'existência',
            'substantia': 'substância',
            'accidens': 'acidente',
            'qualitas': 'qualidade',
            'quantitas': 'quantidade',
            'relatio': 'relação',
            'modus': 'modo',
            'forma': 'forma',
            'materia': 'matéria',
            'anima': 'alma',
            'intellectus': 'intelecto',
            'voluntas': 'vontade',
            'bonum': 'bem',
            'verum': 'verdade',
            'unum': 'uno'
        }

        for incorrect, correct in bp_additional_corrections.items():
            self.corrections[incorrect] = correct
    
    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Find and correct philosophical terms in text.
        Returns corrected text and list of corrections made.
        """
        corrections = []
        corrected_text = text

        # Sort corrections by length (longest first) to handle multi-word phrases
        sorted_corrections = sorted(self.corrections.items(), key=lambda x: len(x[0]), reverse=True)

        for incorrect, correct in sorted_corrections:
            # Find the original case version in the text
            pattern = re.compile(re.escape(incorrect), re.IGNORECASE)
            matches = list(pattern.finditer(corrected_text))

            for match in matches:
                original = match.group()
                # Preserve original case
                if original.isupper():
                    corrected = correct.upper()
                elif original.istitle():
                    corrected = correct.capitalize()
                else:
                    corrected = correct.lower()

                corrected_text = corrected_text[:match.start()] + corrected + corrected_text[match.end():]

                corrections.append({
                    'original': original,
                    'corrected': corrected,
                    'position': match.start()
                })

        return corrected_text, corrections
    
    def get_brazilian_context_info(self, term: str) -> Dict:
        """Get Brazilian Portuguese specific context information for a term."""
        term_lower = term.lower()

        # Check phonetic patterns
        for category, patterns in self.phonetic_patterns.items():
            for correct, variations in patterns.items():
                if term_lower == correct.lower() or term_lower in [v.lower() for v in variations]:
                    return {
                        'term': correct,
                        'language': 'Brazilian Portuguese',
                        'category': 'Phonetic variation',
                        'brazilian_characteristics': 'Common in spoken philosophical discussions',
                        'variations': variations
                    }

        return None
    
    def validate_brazilian_accentuation(self, text: str) -> List[str]:
        """Validate Brazilian Portuguese accentuation in philosophical terms."""
        suspicious_terms = []
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)

        # Common accentuation issues in BP philosophical texts
        accentuation_patterns = {
            r'ontologia': 'ontologia',
            r'metafísica': 'metafísica',
            r'filosofia': 'filosofia',
            r'conhecimento': 'conhecimento',
            r'argumentação': 'argumentação',
            r'interpretação': 'interpretação',
            r'compreensão': 'compreensão',
            r'existência': 'existência',
            r'essência': 'essência',
            r'substância': 'substância',
            r'consciência': 'consciência',
            r'transcendência': 'transcendência',
            r'imanência': 'imanência'
        }

        for word in words:
            word_lower = word.lower()
            for pattern, correct in accentuation_patterns.items():
                if re.match(pattern, word_lower) and word_lower != correct:
                    suspicious_terms.append(f"{word} → {correct}")

        return suspicious_terms
    
    def get_whisper_optimization_tips(self) -> List[str]:
        """Get tips for optimizing Whisper LLM performance with BP philosophical content."""
        return [
            "Use English translation layer: Transcribe in English first, then translate to BP",
            "Leverage philosophical vocabulary: Whisper performs better with academic English terms",
            "Context priming: Provide philosophical context before transcription",
            "Multi-pass refinement: Use Whisper for initial transcription, then BP-specific correction",
            "Speaker identification: Use Whisper's speaker diarization for dialogue-heavy content",
            "Custom vocabulary: Add BP philosophical terms to Whisper's vocabulary",
            "Post-processing: Apply BP-specific corrections after Whisper transcription",
            "Confidence scoring: Use Whisper's confidence scores to identify uncertain transcriptions"
        ]
