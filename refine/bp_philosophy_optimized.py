"""
Optimized Brazilian Portuguese Philosophical Terminology System
Efficient unified dictionary approach for maximum performance.
"""

from typing import Dict, List, Tuple, Optional
import re
import unicodedata
import ahocorasick
from .utils import get_global_cache
from .term_matching import CORRECTIONS_MAP, find_best_match as _tm_find_best_match


class OptimizedBPPhilosophySystem:
    """Optimized BP philosophical terminology and correction system."""

    def __init__(self):
        """Initialize the optimized BP philosophy system."""
        self._build_efficient_corrections_dict()
        self._precompile_patterns()

    def _build_efficient_corrections_dict(self) -> None:
        """Build efficient unified corrections dictionary."""
        # Unified corrections dictionary for maximum efficiency
        self.corrections: Dict[str, str] = {}
        self._canonical_names: set = set()
        self._name_variants: Dict[str, str] = {}

        # Single categorized source dictionary for all corrections
        PHILOSOPHY_TERMS = {
            # --- Philosophers ---
            "philosophers_ancient_medieval": {
                "Sócrates": ["Socrates", "Socrátes", "Sokrates", "Socrate", "Socra tes", "Socrats", "Socratez", "Socratis"],
                "Platão": ["Plato", "Platón", "Platon", "Platao", "Plàtão", "Plto", "P lato"],
                "Aristóteles": ["Aristotle", "Aristoteles", "Aristotles"],
                "Heráclito": ["Heraclitus"],
                "Parmênides": ["Parmenides"],
                "Demócrito": ["Democritus"],
                "Pitágoras": ["Pythagoras"],
                "Tales": ["Thales"],
                "Anaximandro": ["Anaximander"],
                "Anaxímenes": ["Anaximenes"],
                "Protágoras": ["Protagoras"],
                "Górgias": ["Gorgias"],
                "Zenão de Eleia": ["Zeno of Elea", "Zenão", "Zeno"],
                "Empédocles": ["Empedocles"],
                "Anaxágoras": ["Anaxagoras"],
                "Leucipo": ["Leucippus"],
                "Melisso": ["Melissus"],
                "Agostinho de Hipona": ["Augustine of Hippo", "Santo Agostinho", "S. Agostinho", "Agostino"],
                "Justino Mártir": ["Justin Martyr"],
                "Ireneu de Lyon": ["Irenaeus", "Ireneu"],
                "Tertuliano": ["Tertullian"],
                "Hipólito": ["Hippolytus"],
                "Cipriano": ["Cyprian", "São Cipriano"],
                "Orígenes": ["Origen"],
                "Clemente de Alexandria": ["Clement", "Clemente"],
                "Atanásio de Alexandria": ["Athanasius", "Atanásio"],
                "Basílio de Cesareia": ["Basil of Caesarea", "Basílio"],
                "Gregório Nazianzeno": ["Gregory Nazianzus", "Gregório Nazianzeno"],
                "Gregório de Nissa": ["Gregory of Nyssa", "Gregório de Nissa"],
                "João Crisóstomo": ["John Chrysostom", "João Crisóstomo"],
                "Jerônimo": ["Jerome", "São Jerônimo"],
                "Tomás de Aquino": ["Thomas Aquinas", "Santo Tomás", "São Tomás", "S. Tomás", "São Thomaz", "Tomás Aquinas", "Tomaz de Aquino", "Tomas de Aquino"],
                "Duns Scotus": ["John Duns Scotus", "João Duns Scotus", "Duns Escoto", "Scotus"],
                "Boécio": ["Boethius", "Boecio"],
                "Pedro Lombardo": ["Peter Lombard"],
                "Anselmo de Cantuária": ["Anselm of Canterbury", "Anselmo", "Santo Anselmo"],
                "Boaventura": ["Bonaventure", "São Boaventura"],
                "Alberto Magno": ["Albert the Great", "Santo Alberto Magno"],
                "Roger Bacon": ["Rogério Bacon", "R. Bacon"],
                "Guilherme de Ockham": ["William of Ockham", "Ockham", "Guilherme Ockham"],
                "João Buridano": ["John Buridan", "Buridan"],
                "Mestre Eckhart": ["Meister Eckhart", "Eckhart"],
                "Tomás Bradwardine": ["Thomas Bradwardine"],
                "Roberto Grosseteste": ["Robert Grosseteste"],
                "Averróis": ["Averroes", "Ibn Rushd"],
                "Avicena": ["Avicenna", "Ibn Sina"],
                "Algazel": ["Al-Ghazali"],
                "Maimônides": ["Maimonides", "Rambam"],
                "Francisco Suárez": ["Suarez", "Francisco Suarez"],
                "Tomás Caetano": ["Thomas Cajetan", "Caetano", "Cajetan"],
                "João de São Tomás": ["John of Saint Thomas", "João de S. Tomás"],
                "Bernardo de Claraval": ["Bernard of Clairvaux", "Bernardo de Claraval"],
                "Pedro Abelardo": ["Peter Abelard", "Abelardo"],
                "João Escoto Erígena": ["John Scotus Eriugena", "Eriugena", "Escoto Erígena"],
                "Alcuíno de Iorque": ["Alcuin of York", "Alcuino", "Alcuin", "Alcuíno de Iorqueo"],
                "Carlos Magno": ["Carlos o Grande", "Charlemagne", "Carlos Maio", "Carlos Mário"],
            },
            "philosophers_modern_contemporary": {
                "René Descartes": ["Descartes", "Decartes", "René Decartes"],
                "Baruch Spinoza": ["Spinoza", "Baruch de Spinoza", "Espinosa"],
                "Gottfried Wilhelm Leibniz": ["Leibniz", "Leibinitz", "G. W. Leibniz"],
                "John Locke": ["Locke", "J. Locke"],
                "George Berkeley": ["Berkeley", "G. Berkeley"],
                "David Hume": ["Hume", "D. Hume"],
                "Thomas Hobbes": ["Hobbes", "T. Hobbes"],
                "Blaise Pascal": ["Pascal", "B. Pascal"],
                "Nicolas Malebranche": ["Malebranche", "N. Malebranche"],
                "Immanuel Kant": ["Kant", "Emanuel Kant"],
                "Johann Gottlieb Fichte": ["Fichte", "J. G. Fichte"],
                "Friedrich Wilhelm Joseph Schelling": ["Schelling", "F. W. J. Schelling"],
                "Georg Wilhelm Friedrich Hegel": ["Hegel", "G. W. F. Hegel"],
                "Søren Kierkegaard": ["Kierkegaard", "S. Kierkegaard"],
                "Arthur Schopenhauer": ["Schopenhauer", "A. Schopenhauer"],
                "Karl Marx": ["Marx", "K. Marx"],
                "Friedrich Engels": ["Engels", "F. Engels"],
                "Friedrich Nietzsche": ["Nietzsche", "Nitsche", "Nietzche", "Nitche"],
                "Wilhelm Dilthey": ["Dilthey", "W. Dilthey"],
                "Edmund Husserl": ["Husserl", "E. Husserl"],
                "Martin Heidegger": ["Heidegger", "M. Heidegger"],
                "Jean-Paul Sartre": ["Sartre", "J.-P. Sartre"],
                "Simone de Beauvoir": ["Beauvoir", "S. de Beauvoir"],
                "Albert Camus": ["Camus", "A. Camus"],
                "Maurice Merleau-Ponty": ["Merleau-Ponty", "M. Merleau-Ponty"],
                "Emmanuel Levinas": ["Levinas", "E. Levinas"],
                "Hannah Arendt": ["Arendt", "H. Arendt"],
                "Gottlob Frege": ["Frege", "G. Frege"],
                "Bertrand Russell": ["Russell", "B. Russell"],
                "Ludwig Wittgenstein": ["Wittgenstein", "L. Wittgenstein"],
                "Michel Foucault": ["Foucault", "M. Foucault"],
                "Jacques Derrida": ["Derrida", "J. Derrida"],
                "Gilles Deleuze": ["Deleuze", "G. Deleuze"],
                "Félix Guattari": ["Guattari", "F. Guattari", "Felix Guattari"],
                "Judith Butler": ["Butler", "J. Butler"],
                "Byung-Chul Han": ["Han", "B-C. Han"],
                "Slavoj Žižek": ["Žižek", "Zizek"],
                "Jürgen Habermas": ["Habermas", "J. Habermas"],
                "Theodor Adorno": ["Adorno", "T. Adorno", "Teodor Adorno"],
                "Walter Benjamin": ["Benjamin", "W. Benjamin", "Valter Benjamin"],
                "Jacques Lacan": ["Lacan", "J. Lacan", "Jacque Lacan"],
                "Giorgio Agamben": ["Agamben", "G. Agamben"],
                "Max Horkheimer": ["Horkheimer", "M. Horkheimer"],
                "Herbert Marcuse": ["Marcuse", "H. Marcuse"],
                "Georges Bataille": ["Bataille", "G. Bataille"],
                "Maurice Blanchot": ["Blanchot", "M. Blanchot"],
                "Jean Baudrillard": ["Baudrillard", "J. Baudrillard"],
                "Paul Virilio": ["Virilio", "P. Virilio"],
                "Saul Kripke": ["Kripke", "S. Kripke"],
                "Thomas Kuhn": ["Kuhn", "T. Kuhn"],
                "Paul Feyerabend": ["Feyerabend", "P. Feyerabend"],
                "Karl Popper": ["Popper", "K. Popper"],
                "John Searle": ["Searle", "J. Searle"],
                "Daniel Dennett": ["Dennett", "D. Dennett"],
                "Richard Rorty": ["Rorty", "R. Rorty"],
                "Martha Nussbaum": ["Nussbaum", "M. Nussbaum"],
                "Peter Singer": ["Singer", "P. Singer"],
                "Marshall McLuhan": ["McLuhan", "M. McLuhan"],
                "Donna Haraway": ["Haraway", "D. Haraway"],
                "Nick Bostrom": ["Bostrom", "N. Bostrom"],
                "Luciano Floridi": ["Floridi", "L. Floridi"],
                "Ray Kurzweil": ["Kurzweil", "R. Kurzweil"],
            },
            "philosophers_brazilian": {
                "Olavo de Carvalho": ["Olavo", "O. de Carvalho"],
                "Vicente Ferreira da Silva": ["Vicente Ferreira", "V. F. da Silva"],
                "Mário Ferreira dos Santos": ["Mario Ferreira dos Santos", "M. F. dos Santos"],
                "Miguel Reale": ["Reale", "M. Reale"],
                "Tobias Barreto": ["Tobias Barreto", "T. Barreto"],
                "Sílvio Romero": ["Silvio Romero", "S. Romero"],
                "Farias Brito": ["Farias Brito", "F. Brito"],
                "Vilém Flusser": ["Vilem Flusser", "Flusser"],
                "Gerd Bornheim": ["Bornheim", "G. Bornheim"],
                "Newton da Costa": ["Newton da Costa", "N. da Costa"],
                "Ubiratan D'Ambrosio": ["Ubiratan D'Ambrosio", "D'Ambrosio"],
                "José Arthur Giannotti": ["Giannotti", "Gianotti"],
                "Marilena Chauí": ["Chauí", "Chaui", "M. Chauí"],
                "Paulo Arantes": ["Arantes", "P. Arantes"],
                "Roberto Romano": ["Romano", "R. Romano"],
                "Vladimir Safatle": ["Safatle", "V. Safatle"],
                "Leandro Konder": ["Konder", "L. Konder"],
                "Benedito Nunes": ["Nunes", "B. Nunes"],
                "Paulo Freire": ["Paulo Freire", "P. Freire"],
                "Sueli Carneiro": ["Sueli Carneiro", "S. Carneiro"],
                "Djamila Ribeiro": ["Djamila Ribeiro", "D. Ribeiro"],
                "Silvio Almeida": ["Silvio Almeida", "S. Almeida"],
                "Olgária Matos": ["Olgária Matos", "O. Matos"],
                "Oswaldo Giacoia Junior": ["Giacoia Junior", "O. Giacoia"],
                "Benedito Prado Júnior": ["Bento Prado Jr.", "Prado Junior"],
            },

            # --- Concepts ---
            "concepts_ancient_latin": {
                # Greek Concepts
                "logos": ["lógos"],
                "nous": ["noûs", "intelecto", "mente"],
                "physis": ["phýsis", "fisis", "natureza"],
                "aretē": ["areté", "aretê", "excelência"],
                "eudaimonia": ["eudaimônia", "felicidade"],
                "mythos": ["mýthos", "mito"],
                "kosmos": ["kósmos", "cosmos"],
                "arche": ["arché", "princípio"],
                "doxa": ["dóxa", "opinião"],
                "episteme": ["epistéme", "conhecimento"],
                "sophia": ["sophía", "sabedoria"],
                "techne": ["téchne", "técnica"],
                "hamartia": ["hamartía", "erro", "pecado"],
                "anagnorisis": ["anagnórisis", "reconhecimento"],
                "catharsis": ["kátharsis", "catarse"],
                # Latin Concepts
                "Suma Teológica": ["Summa Theologiae", "Suma Teologica", "Suma teológica"],
                "Hilemorfismo": ["hylomorphism", "ilemorfismo"],
                "Tomismo": ["thomism", "tomismu"],
                "Nominalismo": ["nominalism"],
                "Analogia entis": ["analogia do ser", "analogia entis"],
                "Actus purus": ["ato puro", "actus purus"],
                "Forma substancial": ["forma substantialis"],
                "Materia prima": ["matéria prima", "materia prima"],
                "Quinque viae": ["cinco vias", "quinque viae"],
                "Transcendentais": ["transcendentals", "trascendentais"],
                "Voluntarismo": ["voluntarism"],
                "Iluminação divina": ["iluminacao divina"],
                "Prova ontológica": ["argumento ontológico", "prova ontologica"],
                "Livro das Sentenças": ["livros de sentenças", "Livro das Sentencas"],
                "esse": ["essse"],
                "ens": ["enz"],
                "quidditas": ["quididade"],
                "haecceitas": ["heceidade"],
                "substantia": ["substância"],
                "potentia": ["potência", "potensia"],
                "a priori": ["apriori", "a priore", "a priory"],
                "a posteriori": ["aposteriori", "a posteriore"],
                "cogito ergo sum": ["cógito ergo sum"],
                "tabula rasa": ["tábula rasa"],
                "res cogitans": ["rez cogitans"],
                "res extensa": ["rez extensa"],
                "causa sui": ["cauza sui"],
                "per se": ["perse", "per ze"],
            },
            "concepts_modern_contemporary": {
                "ser-aí": ["dasein", "zer-ai"],
                "ser e tempo": ["zer e tempo"],
                "além-do-homem": ["übermensch", "super-homem"],
                "vontade de potência": ["vontade de poder", "wille zur macht"],
                "eterno retorno": ["eterna recorrência"],
                "desconstrução": ["deconstruction"],
                "mais-valia": ["mais valia"],
                "jogos de linguagem": ["jógos de linguagem"],
                "fenomenologia": ["fenomenolojia"],
                "Pós-estruturalismo": ["pós estruturalismo", "post-structuralism", "pos-estruturalismo"],
                "Indústria Cultural": ["industria cultural", "kulturindustrie"],
                "Biopolítica": ["biopolitics", "bio politica"],
                "Rizoma": ["rhizome", "risoma"],
                "Corpo sem órgãos": ["corpo sem orgaos", "CSO"],
                "Desterritorialização": ["deterritorialization", "desterritorializacao"],
                "Simulacro": ["simulacrum", "simulacra"],
                "Agir comunicativo": ["communicative action", "agir comunicativo"],
                "Esfera pública": ["public sphere", "esfera publica"],
                "Banalidade do mal": ["banality of evil", "banalidade do mau"],
                "Arqueologia do saber": ["archeology of knowledge", "arqueologia do saber"],
                "Genealogia do poder": ["genealogy of power", "genealogia do poder"],
                "Microfísica do poder": ["microphysics of power", "microfisica do poder"],
                "Panóptico": ["panopticon", "panoptico"],
                "Différance": ["differance", "diferance"],
                "Logocentrismo": ["logocentrism", "logocentrismo"],
                "Falseabilidade": ["falsifiability", "falseabilidade"],
                "Incomensurabilidade": ["incommensurability", "incomensurabilidade"],
                "transumanismo": ["trans-humanismo"],
                "singularidade tecnológica": ["singularidade tecnologica"],
                "argumento da sala chinesa": ["sala chinesa"],
                "problema do bonde": ["dilema do bonde", "trolley problem"],
                "qualia": ["qualia"],
                "teoria da simulação": ["hipótese da simulação"],
                "pós-humanismo": ["post-humanism"],
                "filosofia da mente": ["filosofia da mente", "philosophy of mind"],
                "filosofia da ciência": ["filosofia da ciência", "philosophy of science"],
                "Sociedade do Espetáculo": ["society of the spectacle", "sociedade do espetaculo"],
                "O meio é a mensagem": ["the medium is the message", "o meio e a mensagem"],
                "Aldeia global": ["global village", "aldeia global"],
                "Risco existencial": ["existential risk", "risco existencial"],
                "Infosfera": ["infosphere", "infosfera"],
                "Ética da informação": ["information ethics", "etica da informacao"],
                "Antropofagia cultural": ["antropofagia", "cultural anthropophagy"],
                "Homem cordial": ["homem cordial", "cordial man"],
            },

            # --- Common Portuguese errors not specific to a single concept ---
            "common_misspellings": {
                "filosofia": ["filizofia", "filozofia"],
                "filosófica": ["filizofica", "filozofica"],
                "neotomismo": ["neo tomismo"],
                "dialética": ["dialetica", "dialética"],
                "epistemologia": ["epistimologia"],
                "ontologia": ["ontolojia"],
                "metafísica": ["metafizica"],
                "lógica": ["logica"],
                "existência": ["existencia"],
                "escolástica": ["colássica", "escolastica"],
                "Medieval": ["Né de Val", "Medival"],
            },
        }

        # Build unified corrections dictionary from the categorized structure
        for _category, terms in PHILOSOPHY_TERMS.items():
            for correct_term, incorrect_variants in terms.items():
                for incorrect in incorrect_variants:
                    key = incorrect.lower()
                    if key not in self.corrections:  # Avoid overwrites
                        self.corrections[key] = correct_term

                # Handle canonical names for philosophers/authors
                if any(source in str(correct_term) for source in [
                    'Sócrates', 'Platão', 'Aristóteles', 'Agostinho', 'Tomás', 'Olavo',
                    'Marilena', 'Descartes', 'Spinoza', 'Leibniz', 'Locke', 'Hume', 'Kant',
                    'Hegel', 'Kierkegaard', 'Schopenhauer', 'Marx', 'Nietzsche', 'Husserl',
                    'Heidegger', 'Wittgenstein', 'Sartre', 'Foucault', 'Derrida']):
                    self._canonical_names.add(correct_term)
                    for variant in incorrect_variants:
                        self._name_variants[self._normalize(variant)] = correct_term

        # Pre-sort corrections by length for efficiency
        self._sorted_corrections = sorted(self.corrections.items(), key=lambda x: len(x[0]), reverse=True)

    def _precompile_patterns(self) -> None:
        """Pre-compile regex patterns and build Aho-Corasick automaton for efficiency."""
        self._compiled_patterns: Dict[str, re.Pattern] = {}
        for incorrect in self.corrections:
            self._compiled_patterns[incorrect] = re.compile(re.escape(incorrect), re.IGNORECASE)

        # Build Aho-Corasick automaton for O(n+m) multi-pattern matching
        self._aho_automaton = ahocorasick.Automaton()
        for incorrect, correct in self.corrections.items():
            # Add both lowercase and case-preserved versions
            self._aho_automaton.add_word(incorrect.lower(), (incorrect, correct))
            if incorrect != incorrect.lower():
                self._aho_automaton.add_word(incorrect, (incorrect, correct))

        self._aho_automaton.make_automaton()



    
    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Find and correct philosophical terms in text using Aho-Corasick automaton.
        Time complexity: O(n + m) where n is text length, m is number of corrections.
        Includes caching for improved performance on repeated texts.
        """
        cache = get_global_cache()

        # Check cache first
        cached_result = cache.get_bp_corrections(text)
        if cached_result:
            return cached_result['corrected_text'], cached_result['corrections']

        corrections: List[Dict] = []
        corrected_text = text
        lower_text = text.lower()

        # Step 0: Apply targeted corrections map first (simple and small set)
        # Do case-insensitive, word-boundary replacements
        for incorrect, correct in CORRECTIONS_MAP.items():
            pattern = re.compile(r"\b" + re.escape(incorrect) + r"\b", re.IGNORECASE)
            def _repl(match: re.Match) -> str:
                original = match.group(0)
                if ' ' not in correct:
                    if original.isupper():
                        replacement = correct.upper()
                    elif original.istitle():
                        replacement = correct.capitalize()
                    else:
                        replacement = correct
                else:
                    replacement = correct
                corrections.append({
                    'original': original,
                    'corrected': replacement,
                    'position': match.start()
                })
                return replacement

            corrected_text_new, num_subs = pattern.subn(_repl, corrected_text)
            if num_subs > 0:
                corrected_text = corrected_text_new
                lower_text = corrected_text.lower()

        # Find all matches using Aho-Corasick automaton
        matches = []
        for end_index, (original_pattern, correct_term) in self._aho_automaton.iter(lower_text):
            start_index = end_index - len(original_pattern) + 1
            original_text = corrected_text[start_index:end_index + 1]

            matches.append({
                'start': start_index,
                'end': end_index + 1,
                'original': original_text,
                'pattern': original_pattern,
                'correct': correct_term
            })

        # Sort matches by start position (reverse order to avoid position shifts)
        matches.sort(key=lambda x: x['start'], reverse=True)

        # Apply corrections without overlap conflicts
        applied_positions = set()

        for match in matches:
            start_pos = match['start']
            end_pos = match['end']
            original = match['original']
            correct = match['correct']

            # Check for overlaps with already applied corrections
            overlap = False
            for applied_start, applied_end in applied_positions:
                if (start_pos < applied_end and end_pos > applied_start):
                    overlap = True
                    break

            if overlap:
                continue

            # Apply case preservation for single-word tokens
            if ' ' not in correct:
                if original.isupper():
                    corrected = correct.upper()
                elif original.istitle():
                    corrected = correct.capitalize()
                else:
                    corrected = correct
            else:
                corrected = correct

            # Apply the correction
            corrected_text = corrected_text[:start_pos] + corrected + corrected_text[end_pos:]
            applied_positions.add((start_pos, start_pos + len(corrected)))

            corrections.append({
                'original': original,
                'corrected': corrected,
                'position': start_pos
            })

        # Cache the results
        cache.set_bp_corrections(text, corrected_text, corrections)

        # Record performance metrics
        from .utils import get_performance_monitor
        monitor = get_performance_monitor()
        monitor.record_bp_corrections(len(corrections))

        return corrected_text, corrections

    # Helper to expose best-match functionality from compact dictionary
    def find_best_match(self, term: str, category: str, cutoff: float = 0.8) -> Optional[str]:
        return _tm_find_best_match(term, category, cutoff)

    def _normalize(self, s: str) -> str:
        """Lowercase and strip accents for robust matching."""
        if not s:
            return s
        s = s.strip().lower()
        nfkd = unicodedata.normalize('NFD', s)
        return ''.join(ch for ch in nfkd if not unicodedata.combining(ch))

    def __len__(self) -> int:
        return len(self.corrections)

# End of OptimizedBPPhilosophySystem class
