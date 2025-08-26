"""
Optimized Brazilian Portuguese Philosophical Terminology System
Efficient unified dictionary approach for maximum performance.
"""

from typing import Dict, List, Set, Tuple, Any
import re
import unicodedata
from difflib import get_close_matches, SequenceMatcher


class OptimizedBPPhilosophySystem:
    """Optimized BP philosophical terminology and correction system."""

    def __init__(self):
        """Initialize the optimized BP philosophy system."""
        self._build_efficient_corrections_dict()
        self._precompile_patterns()

    def _build_efficient_corrections_dict(self):
        """Build efficient unified corrections dictionary."""
        # Unified corrections dictionary for maximum efficiency
        self.corrections = {}
        self._canonical_names = set()
        self._name_variants = {}

        # All correction data in one place for efficiency
        raw_corrections = {
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

            # Multi-word concepts
            "pensamento crítico": ["pensamento critico", "pensameto critico", "pensamento crítco"],
            "razão prática": ["razão pratica", "razam pratica", "razão prátca"],
            "razão pura": ["razão pura", "razam pura", "razão púra"],
            "coisa em si": ["coisa em si", "coiza em si", "coisa emsy"],
            "mundo dos fenômenos": ["mundo dos fenomenos", "mundo do fenômenos", "mundo dos fenomemos"],
            "ser e tempo": ["ser e tempo", "zer e tempo", "ser e têmpo"],
            "ser-aí": ["ser-ai", "ser a i", "zer ai"],
            "estado de natureza": ["estado da natureza", "estado de naturaza", "estado da naturaza"],
            "contrato social": ["contrato social", "contráto social", "contrato sosial"],
            "vontade geral": ["vontade geral", "vontadi geral", "vontade jeral"],
            "alienação do trabalho": ["alienação do trabalho", "alienação do trabaio", "alienasão do trabalho"],
            "luta de classes": ["luta de classes", "luta de clasez", "lúta de classes"],
            "superestrutura": ["superestrutura", "superestrútura", "superesstrutura"],
            "infrastructure": ["infrastructure", "infraestrutura", "infraestrútura"],
            "mais valia": ["mais valia", "mais-valia", "maisvalia", "maiz valia"],
            "dialética materialista": ["dialética materialista", "dialética materializta", "dialética mateiralista"],
            "materialismo histórico": ["materialismo histórico", "materializmo histórico", "materialismo hystorico"],
            "teoria do conhecimento": ["teoria do conhecimento", "teoria do conhecimeto", "teoria do conhecimento"],
            "problema do mal": ["problema do mal", "problema do mau", "próblema do mal"],
            "prova ontológica": ["prova ontológica", "prova ontolojica", "prova ontoulógica"],
            "argumento ontológico": ["argumento ontológico", "argumento ontolojico", "argumento ontoulógico"],
            "linguagem ideal": ["linguagem ideal", "linguajem ideal", "linguagem ydeal"],
            "jogos de linguagem": ["jogos de linguagem", "jógos de linguagem", "jogos de linguajem"],
            "forma de vida": ["forma de vida", "fórma de vida", "forma de vyda"],
            "discurso do método": ["discurso do método", "discúrso do método", "discurso do metódo"],
            "cogito ergo sum": ["cogito ergo sum", "cógito ergo sum", "cogito ergossum"],
            "tabula rasa": ["tabula rasa", "tábula rasa", "tabúla rasa"],
            "res cogitans": ["res cogitans", "rez cogitans", "res cogytans"],
            "res extensa": ["res extensa", "rez extensa", "res extênsa"],
            "estado de direito": ["estado de direito", "estado de direyto", "estado de dreyto"],
            "poder constituinte": ["poder constituinte", "póder constituinte", "poder constytuinte"],
            "direitos humanos": ["direitos humanos", "direytos humanos", "direitos hûmanos"],
            "justiça distributiva": ["justiça distributiva", "justyça distributiva", "justiça distribútiva"],
            "bem comum": ["bem comum", "bêm comum", "bem cômun"],
            "lei natural": ["lei natural", "leí natural", "lei nátural"],
            "pacto social": ["pacto social", "pácto social", "pacto sosial"],

            # Latin terms
            "a priori": ["apriori", "a priore", "a priory", "apriori"],
            "a posteriori": ["aposteriori", "a posteriore", "a posteryory", "aposteriori"],
            "ad hominem": ["ad hominen", "ad ominem", "ad homynem"],
            "ad infinitum": ["ad infinitun", "adinfinitum", "ad infinitu"],
            "cogito ergo sum": ["cogito ergosum", "cogito ergossum", "cógito ergo sum"],
            "causa sui": ["causa sui", "cauza sui", "causa súi"],
            "tabula rasa": ["tabula rasa", "tábula rasa", "tabúla rasa"],
            "ens": ["enz", "hens", "enss"],
            "esse": ["essse", "esse", "esze"],
            "quidditas": ["quidditas", "quididade", "quyditas", "quiddytas"],
            "haecceitas": ["haecceitas", "heceidade", "haeceytas", "haecceytas"],
            "substantia": ["substantia", "substância", "substancia", "substantya"],
            "accidens": ["accidens", "acidente", "accydens", "acidens"],
            "qualitas": ["qualitas", "qualidade", "qualytas", "qualitas"],
            "quantitas": ["quantitas", "quantidade", "quantytas", "quantitas"],
            "relatio": ["relatio", "relação", "relasão", "relatyo"],
            "modus": ["modus", "modalidade", "moduz", "modus"],
            "actus": ["actus", "ato", "actuz", "actus"],
            "potentia": ["potentia", "potência", "potensia", "potentya"],
            "forma": ["forma", "forma", "fourma", "forma"],
            "materia": ["materia", "matéria", "matiria", "materya"],
            "anima": ["anima", "alma", "anyma", "anima"],
            "intellectus": ["intellectus", "intelecto", "intelectuz", "intellectus"],
            "voluntas": ["voluntas", "vontade", "voluntaz", "voluntas"],
            "bonum": ["bonum", "bem", "bonun", "bonum"],
            "verum": ["verum", "verdade", "verun", "verum"],
            "unum": ["unum", "uno", "unun", "unum"],
            "res cogitans": ["res cogitans", "rez cogitans", "res cogytans"],
            "res extensa": ["res extensa", "rez extensa", "res extênsa"],
            "status quo": ["status quo", "statusquo", "statuz quo"],
            "modus operandi": ["modus operandi", "moduz operandi", "modus operandy"],
            "modus vivendi": ["modus vivendi", "moduz vivendi", "modus vivendy"],
            "in situ": ["in situ", "insitu", "in zitu"],
            "in vitro": ["in vitro", "invitro", "in vytru"],
            "in vivo": ["in vivo", "invivo", "in vyvu"],
            "persona non grata": ["persona non grata", "persona nongrata", "persona non gráta"],
            "de facto": ["de facto", "defacto", "de factu"],
            "de jure": ["de jure", "dejure", "de júre"],
            "ipso facto": ["ipso facto", "ipsofácto", "ipso factu"],
            "sine qua non": ["sine qua non", "sinequanon", "sine qua non"],
            "sui generis": ["sui generis", "suigeneris", "sui generys"],
            "per se": ["per se", "perse", "per ze"],
            "in esse": ["in esse", "inesse", "in esze"],
            "in posse": ["in posse", "inposse", "in pozze"],
            "reductio ad absurdum": ["reductio ad absurdum", "reductyo ad absurdum", "reductio ad absurdun"],
            "argumentum ad baculum": ["argumentum ad baculum", "argumentun ad baculum", "argumentum ad baculun"],
            "argumentum ad ignorantiam": ["argumentum ad ignorantiam", "argumentun ad ignorantiam", "argumentum ad ignorantsyam"],
            "argumentum ad populum": ["argumentum ad populum", "argumentun ad populum", "argumentum ad populun"],
            "argumentum ad verecundiam": ["argumentum ad verecundiam", "argumentun ad verecundiam", "argumentum ad verecundyâm"],
            "jus naturale": ["jus naturale", "jus natural", "juz naturale"],
            "jus gentium": ["jus gentium", "jus gentyum", "juz gentium"],
            "jus civile": ["jus civile", "jus cyvile", "juz civile"],
            "imperium": ["imperium", "imperiun", "imperyum"],
            "dominium": ["dominium", "domyniun", "dominium"],
            "summum bonum": ["summum bonum", "summun bonum", "summum bonun"],
            "bona fide": ["bona fide", "bonafide", "bona fyde"],
            "mala fide": ["mala fide", "malafide", "mala fyde"],
            "in bona fide": ["in bona fide", "inbonafide", "in bona fyde"],
            "in mala fide": ["in mala fide", "inmalafide", "in mala fyde"],
            "ante meridiem": ["ante meridiem", "antemeridiem", "ante meridyen"],
            "post meridiem": ["post meridiem", "postmeridiem", "post meridyen"],
            "ad hoc": ["ad hoc", "adhoc", "ad hoc"],
            "ad valorem": ["ad valorem", "advalorem", "ad valoren"],
            "pro tempore": ["pro tempore", "protempore", "pro tempure"],
            "pro forma": ["pro forma", "proforma", "pro fourma"],
            "pro bono": ["pro bono", "probono", "pro bonu"],
            "pro rata": ["pro rata", "prorata", "pro ráta"],

            # Names and philosophers
            "Sócrates": ["Socrates", "Socrátes", "Sokrates", "SÓCRATES", "Socrate", "Socra tes", "Socrats", "Socratez", "Socratis", "Socrates (filósofo)", "socrates"],
            "Platão": ["Plato", "Platón", "Platon", "PLATÃO", "Platao", "Plàtão", "Plto", "P lato", "platao"],
            "Aristóteles": ["Aristotle", "Aristoteles", "Aristóteles", "ARISTÓTELES", "Aristoteles", "Aristotles", "Aristoteles", "Aristoteles (filósofo)", "aristoteles"],
            "Heráclito": ["Heraclitus", "Heráclito"],
            "Parmênides": ["Parmenides", "Parmênides"],
            "Demócrito": ["Democritus", "Demócrito"],
            "Pitágoras": ["Pythagoras", "Pitágoras"],
            "Tales": ["Thales", "Tales"],
            "Anaximandro": ["Anaximander", "Anaximandro"],
            "Anaxímenes": ["Anaximenes", "Anaxímenes"],
            "Agostinho de Hipona": ["Augustine of Hippo", "Saint Augustine", "St. Augustine", "Santo Agostinho", "S. Agostinho", "Agostino", "Agostín", "Agostinho Hipona"],
            "Justino Mártir": ["Justin Martyr"],
            "Ireneu de Lyon": ["Irenaeus", "Ireneu"],
            "Tertuliano": ["Tertullian", "Tertuliano"],
            "Hipólito": ["Hippolytus", "Hipólito"],
            "Cipriano": ["Cyprian", "São Cipriano"],
            "Orígenes": ["Origen", "Orígenes"],
            "Clemente de Alexandria": ["Clement", "Clemente"],
            "Tomás de Aquino": ["Thomas Aquinas", "St Thomas Aquinas", "Saint Thomas Aquinas", "Santo Tomás", "São Tomás", "S. Tomás", "São Thomaz", "Tomás Aquinas", "Tomaz de Aquino", "Tomas de Aquino", "Tomaz Aquino", "Tomás d' Aquino", "T. de Aquino"],
            "Duns Scotus": ["John Duns Scotus", "João Duns Scotus"],
            "Pedro Lombardo": ["Peter Lombard", "Pedro Lombardo"],
            "Anselmo de Cantuária": ["Anselm", "Anselm of Canterbury", "Anselmo", "Santo Anselmo", "St. Anselm", "Anselmo Cantuária"],
            "Boaventura": ["Bonaventure", "São Boaventura"],
            "Alberto Magno": ["Albert the Great", "Alberto Magno", "Santo Alberto Magno"],
            "Roger Bacon": ["Roger Bacon", "Rogério Bacon", "R. Bacon"],
            "Olavo de Carvalho": ["Olavo", "Olavo de Carvalho", "O. de Carvalho", "Olavo Carvalho", "Olavo d'Carvalho", "Olavo deCarvalho"],
            "José Arthur Giannotti": ["Giannotti", "José Arthur Giannotti", "José A. Giannotti", "Gianotti", "J. A. Giannotti", "José Giannotti"],
            "Marilena Chauí": ["Chauí", "Marilena Chauí", "Marilena Chaui", "M. Chauí", "Marilena de Souza Chauí", "Chauí Marilena"],
            "Paulo Arantes": ["Arantes", "Paulo Arantes", "Paulo Eduardo Arantes", "P. Arantes", "Arantes Paulo"],
            "Roberto Romano": ["Romano", "Roberto Romano", "R. Romano", "Roberto Mangabeira Romano"],
            "Gerd Bornheim": ["Bornheim", "Gerd Bornheim", "G. Bornheim", "Bornhein"],
            "João Cruz Costa": ["Cruz Costa", "João Cruz Costa", "João da Cruz Costa", "J. Cruz Costa", "Cruz-Costa"],
            "Benedito Nunes": ["Benedito Nunes", "B. Nunes", "Nunes", "Benedito N."],
            "Newton Cunha": ["Newton Cunha", "N. Cunha", "Cunha", "Newton da Cunha"],
            "Leandro Konder": ["Leandro Konder", "L. Konder", "Konder", "Leandro Karnal Konder"],
            "José Maurício Domingues": ["José Maurício Domingues", "J. M. Domingues", "Domingues", "José M. Domingues", "Maurício Domingues"],
            "Renato Janine Ribeiro": ["Renato Janine Ribeiro", "R. Janine Ribeiro", "Janine Ribeiro", "Renato J. Ribeiro", "Renato Ribeiro"],
            "Vladimir Safatle": ["Vladimir Safatle", "V. Safatle", "Safatle", "Vladimir S."],
            "Luiz B. L. Orlandi": ["Luiz B. L. Orlandi", "L. B. L. Orlandi", "Orlandi", "Luiz Orlando", "Luiz B. Orlandi"],
            "Adolfo Sánchez Vázquez": ["Adolfo Sánchez Vázquez", "A. Sánchez Vázquez", "Sánchez Vázquez", "Adolfo Vazquez", "Sanchez Vazquez"],
            "Carlos Nelson Coutinho": ["Carlos Nelson Coutinho", "C. N. Coutinho", "Coutinho", "Carlos N. Coutinho", "Nelson Coutinho"],
            "José Paulo Netto": ["José Paulo Netto", "J. P. Netto", "Netto", "José P. Netto", "Paulo Netto"],
            "Marco Aurélio Nogueira": ["Marco Aurélio Nogueira", "M. A. Nogueira", "Nogueira", "Marco Aurelio Nogueira", "Marco A. Nogueira"],
            "Roberto Schwarz": ["Roberto Schwarz", "R. Schwarz", "Schwarz", "Roberto S."],
            "Sérgio Paulo Rouanet": ["Sérgio Paulo Rouanet", "S. P. Rouanet", "Rouanet", "Sérgio Rouanet", "Paulo Rouanet"],
            "Ivonaldo Leite": ["Ivonaldo Leite", "I. Leite", "Leite", "Ivonaldo L."],
            "Rogério Miranda de Almeida": ["Rogério Miranda de Almeida", "R. M. de Almeida", "Miranda de Almeida", "Rogério Miranda", "R. de Almeida"],
            "Ricardo Terra": ["Ricardo Terra", "R. Terra", "Terra", "Ricardo T."],
            "José Oscar de Almeida Marques": ["José Oscar de Almeida Marques", "J. O. A. Marques", "Marques", "José Oscar Marques", "Oscar Marques"],
            "Alfredo Bosi": ["Alfredo Bosi", "A. Bosi", "Bosi", "Alfredo B."],
            "Antonio Candido": ["Antonio Candido", "A. Candido", "Candido", "Antônio Cândido", "Antonio C."],
            "Roberto DaMatta": ["Roberto DaMatta", "R. DaMatta", "DaMatta", "Roberto Da Mata"],
            "Célio da Cunha": ["Célio da Cunha", "C. da Cunha", "Cunha", "Célio Cunha"],
            "Gisele Marchiori Busana": ["Gisele Marchiori Busana", "G. M. Busana", "Busana", "Gisele Busana", "Marchiori Busana"],
            "Ricardo Vélez Rodríguez": ["Ricardo Vélez Rodríguez", "R. V. Rodríguez", "Vélez Rodríguez", "Ricardo Vélez", "R. Rodríguez"]
        }

        # Build unified corrections dictionary efficiently
        for correct_term, incorrect_variants in raw_corrections.items():
            for incorrect in incorrect_variants:
                key = incorrect.lower()
                if key not in self.corrections:  # Avoid overwrites
                    self.corrections[key] = correct_term

            # Handle canonical names for philosophers/authors
            if any(source in str(correct_term) for source in ['Sócrates', 'Platão', 'Aristóteles', 'Agostinho', 'Tomás', 'Olavo', 'Marilena']):
                self._canonical_names.add(correct_term)
                for variant in incorrect_variants:
                    self._name_variants[self._normalize(variant)] = correct_term

        # Additional BP corrections (unified)
        bp_corrections = {
            'cauza': 'causa', 'rial': 'real', 'ezistêncial': 'existencial',
            'filizofica': 'filosófica', 'dezenvolvimento': 'desenvolvimento',
            'proceço': 'processo', 'conpreensão': 'compreensão',
            'intiretação': 'interpretação', 'comprensão': 'compreensão',
            'virdade': 'verdade', 'rialidade': 'realidade',
            'ezistência': 'existência', 'ecência': 'essência',
            'sustância': 'substância', 'assidente': 'acidente',
            'qualidadi': 'qualidade', 'quantidadi': 'quantidade',
            'relason': 'relação', 'modalidadi': 'modalidade',
            'Né de Val': 'medieval', 'ne de val': 'medieval',
            'Né de Vale': 'medieval', 'ne de vale': 'medieval',
            'mediebal': 'medieval', 'hamartianeamente': 'historicamente',
            'ptechne': 'techne', 'capacidadi': 'capacidade',
            'capacida di': 'capacidade', 'sofistica da': 'sofisticada',
            'intelectu al': 'intelectual', 'e spantoso': 'espantoso',
            'neotomismo': 'neotomismo', 'neo tomismo': 'neotomismo',
            'tomismo': 'Tomismo', 'ideia': 'ideia', 'idea': 'ideia',
            'idéia': 'ideia', 'fTomás de Aquinode Tomás de Aquino': 'Tomás de Aquino',
            'factusr': 'actus', 'ofereciram': 'ofereceram',
            'filizofia': 'filosofia', 'filozofica': 'filosófica',
            'filozofia': 'filosofia', 'metafizica': 'metafísica',
            'ontolojia': 'ontologia', 'epistimologia': 'epistemologia',
            'conhicimento': 'conhecimento', 'racionalidadi': 'racionalidade',
            'argumetação': 'argumentação', 'dimonstração': 'demonstração',
            'intirpretação': 'interpretação', 'virdade': 'verdade',
            'rialidade': 'realidade', 'ezistência': 'existência',
            'ecência': 'essência', 'sustância': 'substância',
            'assidente': 'acidente', 'qualidadi': 'qualidade',
            'quantidadi': 'quantidade', 'relason': 'relação',
            'modalidadi': 'modalidade', 'tomás': 'Tomás de Aquino',
            'aquino': 'Aquino', 'aristóteles': 'Aristóteles',
            'platão': 'Platão', 'sócrates': 'Sócrates',
            'agostinho': 'Agostinho', 'actus': 'ato',
            'potentia': 'potência', 'essentia': 'essência',
            'existentia': 'existência', 'substantia': 'substância',
            'accidens': 'acidente', 'qualitas': 'qualidade',
            'quantitas': 'quantidade', 'relatio': 'relação',
            'modus': 'modo', 'forma': 'forma', 'materia': 'matéria',
            'anima': 'alma', 'intellectus': 'intelecto',
            'voluntas': 'vontade', 'bonum': 'bem', 'verum': 'verdade',
            'unum': 'uno', 'seguinte': 'seguinte', 'século seguinte': 'século seguinte',
            'importante': 'importante', 'influência': 'influência',
            'verdade': 'verdade', 'movimento': 'movimento',
            'único': 'único', 'séculos': 'séculos',
            'intelectuais': 'intelectuais', 'maior': 'maior',
            'acompanhar': 'acompanhar', 'nível': 'nível',
            'abordar': 'abordar', 'quando': 'quando',
            'estava': 'estava', 'dando': 'dando', 'gente': 'gente',
            'filosofia': 'filosofia', 'Tomás': 'Tomás',
            'Aquino': 'Aquino', 'oportunidade': 'oportunidade',
            'perdida': 'perdida', 'problema': 'problema',
            'cultura': 'cultura', 'sacra': 'sacra', 'profana': 'profana',
            'assim': 'assim', 'equaciona': 'equaciona', 'coisa': 'coisa',
            'pode': 'pode', 'equacionar': 'equacionar', 'fé': 'fé',
            'razão': 'razão', 'porque': 'porque', 'dentro': 'dentro',
            'existem': 'existem', 'elementos': 'elementos', 'existe': 'existe',
            'científicos': 'científicos', 'racionais': 'racionais',
            'também': 'também', 'colocado': 'colocado', 'questão': 'questão',
            'dogmática': 'dogmática', 'muito': 'muito', 'real': 'real',
            'própria': 'própria', 'função': 'função', 'Igreja': 'Igreja',
            'civilização': 'civilização', 'europeia': 'europeia',
            'assume': 'assume', 'após': 'após', 'dissolução': 'dissolução',
            'Império': 'Império', 'temporariamente': 'temporariamente',
            'certas': 'certas', 'funções': 'funções', 'administrativas': 'administrativas',
            'torna': 'torna', 'lugares': 'lugares', 'fator': 'fator',
            'ordem': 'ordem', 'social': 'social', 'sobrecarregava': 'sobrecarrega',
            'série': 'série', 'ofereceram': 'ofereceram', 'fazer': 'fazer',
            'preciso': 'preciso', 'pensar': 'pensar', 'fórmula': 'fórmula',
            'política': 'política', 'baseada': 'baseada', 'Evangelho': 'Evangelho',
            'bocado': 'bocado', 'difícil': 'difícil', 'deduzir': 'deduzir',
            'menor': 'menor', 'dica': 'dica', 'quanto': 'quanto',
            'ponto': 'ponto', 'estabelecer': 'estabelecer', 'Dias': 'dai',
            'César': 'César', 'fica': 'fica', 'pouco': 'pouco',
            'nebuloso': 'nebuloso', 'saber': 'saber', 'exatamente': 'exatamente',
            'onde': 'onde', 'começa': 'começa', 'reino': 'reino', 'Deus': 'Deus'
        }

        for incorrect, correct in bp_corrections.items():
            self.corrections[incorrect] = correct
            if incorrect and incorrect[:1].isupper():
                self._name_variants[self._normalize(incorrect)] = correct

        # Pre-sort corrections by length for efficiency
        self._sorted_corrections = sorted(self.corrections.items(), key=lambda x: len(x[0]), reverse=True)
    def _precompile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self._compiled_patterns = {}
        for incorrect in self.corrections:
            self._compiled_patterns[incorrect] = re.compile(re.escape(incorrect), re.IGNORECASE)



    
    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Find and correct philosophical terms in text with optimized performance.
        """
        corrections = []
        corrected_text = text

        # Use pre-sorted corrections for efficiency
        for incorrect, correct in self._sorted_corrections:
            pattern = self._compiled_patterns.get(incorrect)
            if not pattern:
                continue

            matches = list(pattern.finditer(corrected_text))

            for match in matches:
                start_pos = match.start()
                end_pos = match.end()

                # Check if this match overlaps with any already corrected position
                overlap = False
                for corr_start, corr_end in [(c['position'], c['position'] + len(c['original'])) for c in corrections]:
                    if (start_pos < corr_end and end_pos > corr_start):
                        overlap = True
                        break

                if overlap:
                    continue

                original = match.group()

                # Preserve case for single-word tokens
                if ' ' not in correct:
                    if original.isupper():
                        corrected = correct.upper()
                    elif original.istitle():
                        corrected = correct.capitalize()
                    else:
                        corrected = correct.lower()
                else:
                    corrected = correct

                corrected_text = corrected_text[:start_pos] + corrected + corrected_text[end_pos:]

                corrections.append({
                    'original': original,
                    'corrected': corrected,
                    'position': start_pos
                })

        return corrected_text, corrections

    def _normalize(self, s: str) -> str:
        """Lowercase and strip accents for robust matching."""
        if not s:
            return s
        s = s.strip().lower()
        nfkd = unicodedata.normalize('NFD', s)
        return ''.join(ch for ch in nfkd if not unicodedata.combining(ch))

    def __len__(self):
        return len(self.corrections)

# End of OptimizedBPPhilosophySystem class


    def _normalize(self, s: str) -> str:
        """Lowercase and strip accents for robust matching."""
        if not s:
            return s
        s = s.strip().lower()
        nfkd = unicodedata.normalize('NFD', s)
        return ''.join(ch for ch in nfkd if not unicodedata.combining(ch))

    def __len__(self):
        return len(self.corrections)


# End of OptimizedBPPhilosophySystem class
