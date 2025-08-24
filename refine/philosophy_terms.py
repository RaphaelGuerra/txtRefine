"""
Philosophical terminology database for Portuguese texts.
Includes common terms, their variations, and typical transcription errors.
"""

from typing import Dict, List, Set, Tuple
import re
from difflib import get_close_matches


class PhilosophyTermsDatabase:
    """Database of philosophical terms and common transcription errors."""
    
    def __init__(self):
        # Core philosophical terms in Portuguese
        self.portuguese_terms = {
            # Medieval philosophy
            "escolástica": ["colássica", "escholástica", "escolastica"],
            "metafísica": ["metafisica", "meta física"],
            "ontologia": ["hontologia", "antologia"],
            "epistemologia": ["epistemologia", "epístemologia"],
            "teodiceia": ["teodicéia", "teodisseia"],
            "silogismo": ["silogísmo", "cilogismo"],
            "predicamento": ["predicamênto", "predicamiento"],
            "substância": ["substancia", "sustância"],
            "acidente": ["accidente", "assidente"],
            "essência": ["essencia", "escência"],
            "existência": ["existencia", "ezistência"],
            "potência": ["potencia", "potênsia"],
            "ato": ["acto", "atto"],
            
            # Scholastic authors
            "Tomás de Aquino": ["Thomas de Aquino", "Tomas de Aquino"],
            "Aristóteles": ["Aristoteles", "Aristóteles"],
            "Agostinho": ["Augustinho", "Agostino"],
            "Boécio": ["Boecio", "Boésio"],
            "Anselmo": ["Ancelmo", "Anzelmo"],
            "Pedro Lombardo": ["Pedro Lombardó", "Petrus Lombardus"],
            "Duns Scotus": ["Duns Escoto", "Duns Scoto"],
            "Guilherme de Ockham": ["Guilherme de Occam", "William de Ockham"],
            
            # Contemporary Brazilian philosophy
            "fenomenologia": ["fenomenológia", "fenomenologia"],
            "hermenêutica": ["hermeneutica", "ermenêutica"],
            "dialética": ["dialetica", "dialéctica"],
            "práxis": ["praxis", "práxes"],
            "consciência": ["consciencia", "conciência"],
            "transcendência": ["transcendencia", "trancendência"],
            "imanência": ["imanencia", "himanência"],
            
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
            "esse": ["ese", "essi"],
            "qua": ["quá", "cua"],
            "quidditas": ["quiditas", "quiddidade"],
            "haecceitas": ["haecceidade", "hecceitas"],
            "actus": ["actos", "actuz"],
            "potentia": ["potencia", "potêntia"],
            "materia prima": ["materia príma", "matéria prima"],
            "forma substantialis": ["forma substancialis", "forma sustancialis"],
            "intellectus agens": ["intelectus agens", "intellectus agente"],
            "species": ["spécies", "espécies"],
            "genus": ["gênus", "jenus"],
            "differentia specifica": ["diferentia specifica", "differencia específica"],
            "per se": ["perse", "per sé"],
            "per accidens": ["per acidens", "per accidentes"],
            "in actu": ["in ato", "in actú"],
            "in potentia": ["in potencia", "in potêntia"],
            "ex nihilo": ["ex níhilo", "ex-nihilo"],
            "creatio ex nihilo": ["criação ex nihilo", "creatio ex níhilo"],
            "sine qua non": ["sine quanon", "sine qua nom"],
            "ipso facto": ["ipso fato", "ipsofacto"],
            "modus ponens": ["modus ponems", "modus ponnens"],
            "modus tollens": ["modus tolens", "modus tollems"],
            "reductio ad absurdum": ["redução ao absurdo", "reductio ad absurdum"],
        }
        
        # Greek terms (transliterated)
        self.greek_terms = {
            "logos": ["lógos", "logus"],
            "nous": ["nus", "noûs"],
            "physis": ["fisis", "phísis"],
            "psyche": ["psique", "psiqué"],
            "telos": ["télos", "telus"],
            "arche": ["arqué", "archê"],
            "ousia": ["ousía", "usía"],
            "eidos": ["eídos", "eidus"],
            "hyle": ["hílé", "hile"],
            "morphe": ["morfé", "morphê"],
            "energeia": ["enérgeia", "energia"],
            "entelechia": ["enteléquia", "entelekia"],
            "arete": ["areté", "aretê"],
            "episteme": ["epistéme", "epistemê"],
            "doxa": ["dóxa", "doksa"],
            "aletheia": ["alétheia", "alethéia"],
            "phronesis": ["frônesis", "fronesis"],
            "sophia": ["sofía", "sophía"],
            "techne": ["técne", "teknê"],
        }
        
        # Common philosophical expressions
        self.expressions = {
            "em si": ["em sí", "em-si"],
            "para si": ["para sí", "para-si"],
            "em si e para si": ["em si e para sí", "em-si e para-si"],
            "ser em ato": ["ser em acto", "ser-em-ato"],
            "ser em potência": ["ser em potencia", "ser-em-potência"],
            "causa primeira": ["cauza primeira", "causa 1ª"],
            "causa eficiente": ["cauza eficiente", "causa efficiente"],
            "causa final": ["cauza final", "causa finál"],
            "causa formal": ["cauza formal", "causa formál"],
            "causa material": ["cauza material", "causa materiál"],
            "primeiro motor": ["primeiro mótor", "1º motor"],
            "motor imóvel": ["motor imovel", "motor imóbil"],
            "ato puro": ["acto puro", "ato púro"],
            "bem comum": ["bem comun", "bem-comum"],
            "lei natural": ["lei naturál", "ley natural"],
            "lei eterna": ["lei etherna", "ley eterna"],
            "livre arbítrio": ["livre arbitrio", "livre-arbítrio"],
            "graça divina": ["graca divina", "graça divína"],
        }
        
        # Build reverse lookup dictionary
        self._build_reverse_lookup()
    
    def _build_reverse_lookup(self):
        """Build reverse lookup from incorrect to correct terms."""
        self.corrections = {}
        
        for correct, incorrects in self.portuguese_terms.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
        
        for correct, incorrects in self.latin_terms.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
        
        for correct, incorrects in self.greek_terms.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
        
        for correct, incorrects in self.expressions.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
    
    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Find and correct philosophical terms in text.
        Returns corrected text and list of corrections made.
        """
        corrections_made = []
        corrected_text = text
        
        # Sort corrections by length (longest first) to avoid partial replacements
        sorted_corrections = sorted(self.corrections.items(), 
                                   key=lambda x: len(x[0]), reverse=True)
        
        for incorrect, correct in sorted_corrections:
            # Case-insensitive search but preserve original case in replacement
            pattern = re.compile(re.escape(incorrect), re.IGNORECASE)
            matches = pattern.finditer(corrected_text)
            
            for match in matches:
                original = match.group()
                # Preserve capitalization pattern
                if original[0].isupper():
                    replacement = correct[0].upper() + correct[1:]
                else:
                    replacement = correct
                
                # Make replacement
                corrected_text = corrected_text[:match.start()] + replacement + corrected_text[match.end():]
                
                corrections_made.append({
                    'original': original,
                    'corrected': replacement,
                    'position': match.start(),
                    'type': self._get_term_type(correct)
                })
        
        return corrected_text, corrections_made
    
    def _get_term_type(self, term: str) -> str:
        """Identify the type of philosophical term."""
        if term in self.portuguese_terms:
            return "portuguese"
        elif term in self.latin_terms:
            return "latin"
        elif term in self.greek_terms:
            return "greek"
        elif term in self.expressions:
            return "expression"
        return "unknown"
    
    def validate_terms(self, text: str) -> List[str]:
        """
        Validate philosophical terms in text.
        Returns list of potentially incorrect terms.
        """
        suspicious_terms = []
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text)
        
        all_correct_terms = set()
        all_correct_terms.update(self.portuguese_terms.keys())
        all_correct_terms.update(self.latin_terms.keys())
        all_correct_terms.update(self.greek_terms.keys())
        
        for word in words:
            # Check if word might be a philosophical term
            if len(word) > 5:  # Skip short common words
                # Find close matches to known terms
                close_matches = get_close_matches(word.lower(), 
                                                 [t.lower() for t in all_correct_terms],
                                                 n=1, cutoff=0.8)
                if close_matches and close_matches[0] != word.lower():
                    suspicious_terms.append(f"{word} → {close_matches[0]}")
        
        return suspicious_terms
    
    def get_term_info(self, term: str) -> Dict:
        """Get information about a philosophical term."""
        term_lower = term.lower()
        
        # Check each category
        for correct, variations in self.portuguese_terms.items():
            if term_lower == correct.lower() or term_lower in [v.lower() for v in variations]:
                return {
                    'term': correct,
                    'language': 'Portuguese',
                    'category': 'Philosophical term',
                    'variations': variations
                }
        
        for correct, variations in self.latin_terms.items():
            if term_lower == correct.lower() or term_lower in [v.lower() for v in variations]:
                return {
                    'term': correct,
                    'language': 'Latin',
                    'category': 'Classical term',
                    'variations': variations
                }
        
        for correct, variations in self.greek_terms.items():
            if term_lower == correct.lower() or term_lower in [v.lower() for v in variations]:
                return {
                    'term': correct,
                    'language': 'Greek (transliterated)',
                    'category': 'Classical term',
                    'variations': variations
                }
        
        return None
    
    def export_corrections_report(self, corrections: List[Dict]) -> str:
        """Generate a report of corrections made."""
        if not corrections:
            return "No corrections were made."
        
        report = "## Philosophical Terms Corrections Report\n\n"
        report += f"Total corrections: {len(corrections)}\n\n"
        
        # Group by type
        by_type = {}
        for corr in corrections:
            term_type = corr.get('type', 'unknown')
            if term_type not in by_type:
                by_type[term_type] = []
            by_type[term_type].append(corr)
        
        for term_type, items in by_type.items():
            report += f"### {term_type.capitalize()} Terms ({len(items)})\n"
            for item in items:
                report += f"- '{item['original']}' → '{item['corrected']}'\n"
            report += "\n"
        
        return report