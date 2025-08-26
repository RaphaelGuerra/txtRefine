"""
Brazilian Portuguese Philosophical Terminology System
Comprehensive BP corrections and philosophical term handling.
"""

from typing import Dict, List, Set, Tuple, Any
import re
import unicodedata
from difflib import get_close_matches, SequenceMatcher


class BPPhilosophySystem:
    """Complete BP philosophical terminology and correction system."""
    
    def __init__(self):
        """Initialize the BP philosophy system."""
        self._setup_terms_database()
        self._setup_bp_patterns()
    
    def _setup_terms_database(self):
        """Setup the comprehensive philosophical terms database."""
        # Core philosophical terms in Portuguese (expanded with multi-word concepts)
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

            # Multi-word philosophical concepts (common in transcriptions)
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
            "pacto social": ["pacto social", "pácto social", "pacto sosial"]
        }

        # Latin terms commonly used (expanded with BP variations)
        self.latin_terms = {
            # Epistemological terms
            "a priori": ["apriori", "a priore", "a priory", "apriori"],
            "a posteriori": ["aposteriori", "a posteriore", "a posteryory", "aposteriori"],
            "ad hominem": ["ad hominen", "ad ominem", "ad homynem"],
            "ad infinitum": ["ad infinitun", "adinfinitum", "ad infinitu"],
            "cogito ergo sum": ["cogito ergosum", "cogito ergossum", "cógito ergo sum"],
            "causa sui": ["causa sui", "cauza sui", "causa súi"],
            "tabula rasa": ["tabula rasa", "tábula rasa", "tabúla rasa"],

            # Scholastic terms
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

            # Cartesian terms
            "res cogitans": ["res cogitans", "rez cogitans", "res cogytans"],
            "res extensa": ["res extensa", "rez extensa", "res extênsa"],

            # Modern philosophical terms
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

            # Logical terms
            "reductio ad absurdum": ["reductio ad absurdum", "reductyo ad absurdum", "reductio ad absurdun"],
            "argumentum ad baculum": ["argumentum ad baculum", "argumentun ad baculum", "argumentum ad baculun"],
            "argumentum ad ignorantiam": ["argumentum ad ignorantiam", "argumentun ad ignorantiam", "argumentum ad ignorantsyam"],
            "argumentum ad populum": ["argumentum ad populum", "argumentun ad populum", "argumentum ad populun"],
            "argumentum ad verecundiam": ["argumentum ad verecundiam", "argumentun ad verecundiam", "argumentum ad verecundyâm"],

            # Political terms
            "jus naturale": ["jus naturale", "jus natural", "juz naturale"],
            "jus gentium": ["jus gentium", "jus gentyum", "juz gentium"],
            "jus civile": ["jus civile", "jus cyvile", "juz civile"],
            "imperium": ["imperium", "imperiun", "imperyum"],
            "dominium": ["dominium", "domyniun", "dominium"],

            # Ethical terms
            "summum bonum": ["summum bonum", "summun bonum", "summum bonun"],
            "bona fide": ["bona fide", "bonafide", "bona fyde"],
            "mala fide": ["mala fide", "malafide", "mala fyde"],
            "in bona fide": ["in bona fide", "inbonafide", "in bona fyde"],
            "in mala fide": ["in mala fide", "inmalafide", "in mala fyde"],

            # Temporal terms
            "ante meridiem": ["ante meridiem", "antemeridiem", "ante meridyen"],
            "post meridiem": ["post meridiem", "postmeridiem", "post meridyen"],
            "ad hoc": ["ad hoc", "adhoc", "ad hoc"],
            "ad valorem": ["ad valorem", "advalorem", "ad valoren"],
            "pro tempore": ["pro tempore", "protempore", "pro tempure"],
            "pro forma": ["pro forma", "proforma", "pro fourma"],
            "pro bono": ["pro bono", "probono", "pro bonu"],
            "pro rata": ["pro rata", "prorata", "pro ráta"]
        }

        # Classical Greek philosophers and terms (with common BP variations)
        self.greek_philosophers = {
            "Sócrates": [
                "Socrates", "Socrátes", "Sokrates", "SÓCRATES",
                "Socrate", "Socra tes", "Socrats", "Socratez", "Socratis",
                "Socrates (filósofo)", "socrates",
            ],
            "Platão": [
                "Plato", "Platón", "Platon", "PLATÃO", "Platao",
                "Plàtão", "Plto", "P lato", "platao",
            ],
            "Aristóteles": [
                "Aristotle", "Aristoteles", "Aristóteles", "ARISTÓTELES",
                "Aristoteles", "Aristotles", "Aristoteles", "Aristoteles (filósofo)",
                "aristoteles",
            ],
            "Heráclito": ["Heraclitus", "Heráclito"],
            "Parmênides": ["Parmenides", "Parmênides"],
            "Demócrito": ["Democritus", "Demócrito"],
            "Pitágoras": ["Pythagoras", "Pitágoras"],
            "Tales": ["Thales", "Tales"],
            "Anaximandro": ["Anaximander", "Anaximandro"],
            "Anaxímenes": ["Anaximenes", "Anaxímenes"],
        }

        # Patristic authors (with common BP/EN variations)
        self.patristic_authors = {
            "Agostinho de Hipona": [
                "Augustine of Hippo", "Saint Augustine", "St. Augustine",
                "Santo Agostinho", "S. Agostinho", "Agostino", "Agostín",
                "Agostinho Hipona",
            ],
            "Justino Mártir": ["Justin Martyr"],
            "Ireneu de Lyon": ["Irenaeus", "Ireneu"],
            "Tertuliano": ["Tertullian", "Tertuliano"],
            "Hipólito": ["Hippolytus", "Hipólito"],
            "Cipriano": ["Cyprian", "São Cipriano"],
            "Orígenes": ["Origen", "Orígenes"],
            "Clemente de Alexandria": ["Clement", "Clemente"],
        }

        # Scholastic philosophers (with common BP/EN variations)
        self.scholastic_philosophers = {
            "Tomás de Aquino": [
                "Thomas Aquinas", "St Thomas Aquinas", "Saint Thomas Aquinas",
                "Santo Tomás", "São Tomás", "S. Tomás", "São Thomaz",
                "Tomás Aquinas", "Tomaz de Aquino", "Tomas de Aquino",
                "Tomaz Aquino", "Tomás d' Aquino", "T. de Aquino",
            ],
            "Duns Scotus": ["John Duns Scotus", "João Duns Scotus"],
            "Pedro Lombardo": ["Peter Lombard", "Pedro Lombardo"],
            "Anselmo de Cantuária": [
                "Anselm", "Anselm of Canterbury", "Anselmo", "Santo Anselmo",
                "St. Anselm", "Anselmo Cantuária",
            ],
            "Boaventura": ["Bonaventure", "São Boaventura"],
            "Alberto Magno": ["Albert the Great", "Alberto Magno", "Santo Alberto Magno"],
            "Roger Bacon": ["Roger Bacon", "Rogério Bacon", "R. Bacon"],
        }

        # Contemporary philosophers (Brazilian focus - expanded)
        self.contemporary_philosophers = {
            "Olavo de Carvalho": [
                "Olavo", "Olavo de Carvalho", "O. de Carvalho", "Olavo Carvalho",
                "Olavo d'Carvalho", "Olavo deCarvalho"
            ],
            "José Arthur Giannotti": [
                "Giannotti", "José Arthur Giannotti", "José A. Giannotti",
                "Gianotti", "J. A. Giannotti", "José Giannotti"
            ],
            "Marilena Chauí": [
                "Chauí", "Marilena Chauí", "Marilena Chaui", "M. Chauí",
                "Marilena de Souza Chauí", "Chauí Marilena"
            ],
            "Paulo Arantes": [
                "Arantes", "Paulo Arantes", "Paulo Eduardo Arantes",
                "P. Arantes", "Arantes Paulo"
            ],
            "Roberto Romano": [
                "Romano", "Roberto Romano", "R. Romano", "Roberto Mangabeira Romano"
            ],
            "Gerd Bornheim": [
                "Bornheim", "Gerd Bornheim", "G. Bornheim", "Bornhein"
            ],
            "João Cruz Costa": [
                "Cruz Costa", "João Cruz Costa", "João da Cruz Costa",
                "J. Cruz Costa", "Cruz-Costa"
            ],
            # Additional Brazilian philosophers
            "Benedito Nunes": [
                "Benedito Nunes", "B. Nunes", "Nunes", "Benedito N."
            ],
            "Newton Cunha": [
                "Newton Cunha", "N. Cunha", "Cunha", "Newton da Cunha"
            ],
            "Leandro Konder": [
                "Leandro Konder", "L. Konder", "Konder", "Leandro Karnal Konder"
            ],
            "José Maurício Domingues": [
                "José Maurício Domingues", "J. M. Domingues", "Domingues",
                "José M. Domingues", "Maurício Domingues"
            ],
            "Renato Janine Ribeiro": [
                "Renato Janine Ribeiro", "R. Janine Ribeiro", "Janine Ribeiro",
                "Renato J. Ribeiro", "Renato Ribeiro"
            ],
            "Vladimir Safatle": [
                "Vladimir Safatle", "V. Safatle", "Safatle", "Vladimir S."
            ],
            "Luiz B. L. Orlandi": [
                "Luiz B. L. Orlandi", "L. B. L. Orlandi", "Orlandi",
                "Luiz Orlando", "Luiz B. Orlandi"
            ],
            "Adolfo Sánchez Vázquez": [
                "Adolfo Sánchez Vázquez", "A. Sánchez Vázquez", "Sánchez Vázquez",
                "Adolfo Vazquez", "Sanchez Vazquez"
            ],
            "Carlos Nelson Coutinho": [
                "Carlos Nelson Coutinho", "C. N. Coutinho", "Coutinho",
                "Carlos N. Coutinho", "Nelson Coutinho"
            ],
            "José Paulo Netto": [
                "José Paulo Netto", "J. P. Netto", "Netto", "José P. Netto",
                "Paulo Netto"
            ],
            "Marco Aurélio Nogueira": [
                "Marco Aurélio Nogueira", "M. A. Nogueira", "Nogueira",
                "Marco Aurelio Nogueira", "Marco A. Nogueira"
            ],
            "Roberto Schwarz": [
                "Roberto Schwarz", "R. Schwarz", "Schwarz", "Roberto S."
            ],
            "Sérgio Paulo Rouanet": [
                "Sérgio Paulo Rouanet", "S. P. Rouanet", "Rouanet",
                "Sérgio Rouanet", "Paulo Rouanet"
            ],
            "Ivonaldo Leite": [
                "Ivonaldo Leite", "I. Leite", "Leite", "Ivonaldo L."
            ],
            "Rogério Miranda de Almeida": [
                "Rogério Miranda de Almeida", "R. M. de Almeida", "Miranda de Almeida",
                "Rogério Miranda", "R. de Almeida"
            ],
            "Ricardo Terra": [
                "Ricardo Terra", "R. Terra", "Terra", "Ricardo T."
            ],
            "José Oscar de Almeida Marques": [
                "José Oscar de Almeida Marques", "J. O. A. Marques", "Marques",
                "José Oscar Marques", "Oscar Marques"
            ],
            "Alfredo Bosi": [
                "Alfredo Bosi", "A. Bosi", "Bosi", "Alfredo B."
            ],
            "Antonio Candido": [
                "Antonio Candido", "A. Candido", "Candido", "Antônio Cândido",
                "Antonio C."
            ],
            "Roberto DaMatta": [
                "Roberto DaMatta", "R. DaMatta", "DaMatta", "Roberto Da Mata"
            ],
            "Célio da Cunha": [
                "Célio da Cunha", "C. da Cunha", "Cunha", "Célio Cunha"
            ],
            "Gisele Marchiori Busana": [
                "Gisele Marchiori Busana", "G. M. Busana", "Busana",
                "Gisele Busana", "Marchiori Busana"
            ],
            "Ricardo Vélez Rodríguez": [
                "Ricardo Vélez Rodríguez", "R. V. Rodríguez", "Vélez Rodríguez",
                "Ricardo Vélez", "R. Rodríguez"
            ]
        }
        
        self._build_corrections()
    
    def _setup_bp_patterns(self):
        """Setup comprehensive BP-specific phonetic patterns."""
        self.phonetic_patterns = {
            's/z alternation': {
                'causa': ['causa', 'cauza', 'cauça'],
                'realidade': ['realidade', 'rialidade', 'realidadi'],
                'existência': ['existência', 'ezistência', 'existensia'],
                'essência': ['essência', 'ecência', 'essensia'],
                'consciência': ['consciência', 'consciênça', 'consciencia'],
                'transcendência': ['transcendência', 'transcendênça', 'transcendencia'],
                'imanência': ['imanência', 'imanênça', 'imanencia'],
                'presença': ['presença', 'presenza', 'presensa'],
                'ausência': ['ausência', 'ausenza', 'ausensa']
            },
            'r/l alternation': {
                'filosofia': ['filosofia', 'filozofia', 'filozofia'],
                'real': ['real', 'rial', 'real'],
                'oral': ['oral', 'oural', 'oural'],
                'plural': ['plural', 'ploural', 'ploural'],
                'liberal': ['liberal', 'libral', 'libral'],
                'moral': ['moral', 'moural', 'moural'],
                'formal': ['formal', 'fourmal', 'fourmal']
            },
            't/ch alternation': {
                'argumentação': ['argumentação', 'argumetação', 'argumetaçao'],
                'demonstração': ['demonstração', 'dimonstração', 'dimonstraçao'],
                'interpretação': ['interpretação', 'intirpretação', 'intirpretaçao'],
                'representação': ['representação', 'reprisentação', 'reprisentação'],
                'compreensão': ['compreensão', 'comprensão', 'comprensao'],
                'expressão': ['expressão', 'exprissão', 'exprissao']
            },
            'c/ç alternation': {
                'processo': ['processo', 'proceço', 'procesço'],
                'conceito': ['conceito', 'concêito', 'conceito'],
                'contexto': ['contexto', 'contêxto', 'contexto'],
                'perspectiva': ['perspectiva', 'perspêtiva', 'perspectiva'],
                'especifico': ['específico', 'especifico', 'espesifico']
            },
            'ão/ao alternation': {
                'filosofia': ['filosofia', 'filosofia'],
                'ontologia': ['ontologia', 'ontolojia', 'ontologia'],
                'epistemologia': ['epistemologia', 'epistimologia', 'epistemolojia'],
                'fenomenologia': ['fenomenologia', 'fenomenolojia', 'fenomenologia'],
                'antropologia': ['antropologia', 'antropolojia', 'antropologia']
            },
            'i/y alternation': {
                'sistema': ['sistema', 'sistima', 'sistema'],
                'critério': ['critério', 'criteryo', 'criterio'],
                'história': ['história', 'hystoria', 'historia'],
                'método': ['método', 'metodo', 'metodo']
            },
            'e/i alternation': {
                'existencial': ['existencial', 'ezistêncial', 'existencial'],
                'essencial': ['essencial', 'ecêncial', 'essencial'],
                'racional': ['racional', 'rascional', 'racional'],
                'final': ['final', 'fynal', 'final']
            },
            'o/u alternation': {
                'ontológico': ['ontológico', 'ontoulógico', 'ontologico'],
                'psicológico': ['psicológico', 'psicoulógico', 'psicologico'],
                'lógico': ['lógico', 'lougico', 'logico'],
                'cosmológico': ['cosmológico', 'cosmoulógico', 'cosmologico']
            },
            'vowel nasalization': {
                'tempo': ['tempo', 'têmpo', 'tempo'],
                'mundo': ['mundo', 'mûndo', 'mundo'],
                'pensamento': ['pensamento', 'pensamênto', 'pensamento'],
                'conhecimento': ['conhecimento', 'conhecimênto', 'conhecimento']
            }
        }

        # Common BP academic expressions (expanded)
        self.academic_expressions = {
            # Basic connectors
            'quer dizer': ['quer dizer', 'que dizer', 'quedizer', 'quer dize'],
            'ou seja': ['ou seja', 'ouseja', 'ouzeja', 'ou zeja'],
            'isto é': ['isto é', 'itoé', 'iztoé', 'isto e'],
            'por exemplo': ['por exemplo', 'poexemplo', 'porexemplo', 'porezemplo'],
            'dessa forma': ['dessa forma', 'decacorma', 'decaforma', 'dessa fourma'],
            'na verdade': ['na verdade', 'naverdade', 'na verdadi', 'na verdadi'],
            'por outro lado': ['por outro lado', 'poutro lado', 'poroutrolado', 'por outro lado'],
            'em outras palavras': ['em outras palavras', 'emoutraspalavras', 'em outraz palavra'],
            'do ponto de vista': ['do ponto de vista', 'dopontodevista', 'dopontodavista'],

            # Advanced academic expressions
            'em suma': ['em suma', 'emsúma', 'em zuma'],
            'em resumo': ['em resumo', 'emrezumo', 'em resúmo'],
            'a propósito': ['a propósito', 'apróposito', 'a propouzito'],
            'a bem da verdade': ['a bem da verdade', 'abem da verdade', 'a bêm da verdade'],
            'de fato': ['de fato', 'defato', 'de factu'],
            'em princípio': ['em princípio', 'emprinsípio', 'em prinsípyo'],
            'por conseguinte': ['por conseguinte', 'porconseguinte', 'por conseguinti'],
            'consequentemente': ['consequentemente', 'consequenteminti', 'consequentemente'],
            'portanto': ['portanto', 'portantu', 'portanto'],
            'entretanto': ['entretanto', 'entretantu', 'entretanto'],
            'no entanto': ['no entanto', 'noentantu', 'no entanto'],
            'contudo': ['contudo', 'contúdo', 'contudo'],
            'todavia': ['todavia', 'todávia', 'todavia'],
            'não obstante': ['não obstante', 'nao obstante', 'não obstánti'],
            'além disso': ['além disso', 'alêmdisso', 'além dísso'],
            'ademais': ['ademais', 'adémaiz', 'ademaiz'],
            'além do mais': ['além do mais', 'alêmdomais', 'além do maiz'],
            'diante disso': ['diante disso', 'dyanti disso', 'diante dísso'],
            'perante isso': ['perante isso', 'peranti isso', 'perante isço'],
            'nesse sentido': ['nesse sentido', 'neszesentido', 'nese sentído'],
            'sob esse aspecto': ['sob esse aspecto', 'sobese aspecto', 'zob esse aspecto'],
            'sob essa ótica': ['sob essa ótica', 'sobesa ótica', 'sob esa ótica'],
            'do mesmo modo': ['do mesmo modo', 'domesmo modo', 'do mezmo modo'],
            'da mesma forma': ['da mesma forma', 'damesma forma', 'da mezma fourma'],
            'analogamente': ['analogamente', 'analógamente', 'analogamenti'],
            'similarmente': ['similarmente', 'zymilarmente', 'similarmenti'],
            'igualmente': ['igualmente', 'ygualmente', 'igualmenti'],
            'outrossim': ['outrossim', 'outrozzim', 'outrossym'],
            'mais ainda': ['mais ainda', 'maiz ainda', 'mais ayn da'],
            'ainda mais': ['ainda mais', 'ayn damais', 'ainda maiz'],

            # Temporal expressions
            'no decorrer': ['no decorrer', 'nodecorrer', 'no decórre'],
            'ao longo de': ['ao longo de', 'aolongode', 'ao longo de'],
            'através de': ['através de', 'atravéz de', 'através de'],
            'por meio de': ['por meio de', 'pormeio de', 'por meio de'],
            'por intermédio de': ['por intermédio de', 'porintermédio de', 'por intermédyo de'],

            # Philosophical discourse markers
            'vale dizer': ['vale dizer', 'valedizer', 'vale dize'],
            'vale ressaltar': ['vale ressaltar', 'valeressaltar', 'vale ressaltá'],
            'importa destacar': ['importa destacar', 'importadestacar', 'importa destácá'],
            'cumpre salientar': ['cumpre salientar', 'cumpresalientar', 'cumpre salyentá'],
            'urge ressaltar': ['urge ressaltar', 'urgeressaltar', 'urge ressaltá'],
            'não se pode deixar de notar': ['não se pode deixar de notar', 'nao se pode deixar de notar', 'não se pode deixá de notá'],
            'é importante frisar': ['é importante frisar', 'e importante frisar', 'é importanti frizá'],
            'deve-se destacar': ['deve-se destacar', 'devê-se destacar', 'deve-se destácá'],
            'convém mencionar': ['convém mencionar', 'convêm mencionar', 'convêm mensyoná'],
            'cabe mencionar': ['cabe mencionar', 'cabemencionar', 'cabe mensyoná'],
            'é preciso esclarecer': ['é preciso esclarecer', 'e preciso esclarecer', 'é prezizo esclarêsé'],
            'não se pode ignorar': ['não se pode ignorar', 'nao se pode ignorar', 'não se pode ygnorá'],
            'é forçoso reconhecer': ['é forçoso reconhecer', 'e forçoso reconhecer', 'é forsoso rekonsêsé'],
            'urge reconhecer': ['urge reconhecer', 'urgerreconhecer', 'urge rekonsêsé'],

            # Critical expressions
            'em contrapartida': ['em contrapartida', 'emcontrapartida', 'em contrapartýda'],
            'ao contrário': ['ao contrário', 'aocontrário', 'ao contráryo'],
            'pelo contrário': ['pelo contrário', 'pelocontrário', 'pelo contráryo'],
            'muito pelo contrário': ['muito pelo contrário', 'muitopelocontrário', 'muito pelo contráryo'],
            'longe disso': ['longe disso', 'longedisso', 'longe dísso'],
            'de modo algum': ['de modo algum', 'demodo algum', 'de modo algun'],
            'de forma alguma': ['de forma alguma', 'deforma alguma', 'de fourma algúma'],
            'em hipótese alguma': ['em hipótese alguma', 'emhipótese alguma', 'em hipótesi algúma'],
            'sob nenhuma hipótese': ['sob nenhuma hipótese', 'sobnenhuma hipótese', 'zob nenúma hipótesi'],

            # Conclusion expressions
            'em conclusão': ['em conclusão', 'emconclusão', 'em conclusam'],
            'para concluir': ['para concluir', 'paraconcluir', 'para conclusy'],
            'a título de conclusão': ['a título de conclusão', 'atítulodeconclusão', 'a título de conclusam'],
            'finalizando': ['finalizando', 'finalyzando', 'finalizando'],
            'encerrando': ['encerrando', 'enserrando', 'encerrando'],
            'para finalizar': ['para finalizar', 'parafinalizar', 'para finalyzá'],

            # Transition expressions
            'passando a': ['passando a', 'pazando a', 'passando a'],
            'voltando a': ['voltando a', 'voltandoa', 'voltando a'],
            'retomando': ['retomando', 'retomando', 'retomando'],
            'retornando a': ['retornando a', 'retornandoa', 'retornando a'],
            'continuando': ['continuando', 'contynuando', 'continuando'],
            'prosseguindo': ['prosseguindo', 'prozeguindo', 'prosseguindo'],
            'avançando': ['avançando', 'avansando', 'avansando'],
            'passemos a': ['passemos a', 'pazemos a', 'passe mos a'],
            'vamos a': ['vamos a', 'vamoza', 'vamos a'],
            'chegamos a': ['chegamos a', 'chegamoza', 'chegamos a']
        }
    
    def _build_corrections(self):
        """Build reverse lookup dictionary for corrections."""
        self.corrections = {}
        self._canonical_names: Set[str] = set()
        self._name_variants: Dict[str, str] = {}

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
            self._canonical_names.add(correct)
            for v in incorrects:
                self._name_variants[self._normalize(v)] = correct

        for correct, incorrects in self.patristic_authors.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
            self._canonical_names.add(correct)
            for v in incorrects:
                self._name_variants[self._normalize(v)] = correct

        for correct, incorrects in self.scholastic_philosophers.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
            self._canonical_names.add(correct)
            for v in incorrects:
                self._name_variants[self._normalize(v)] = correct

        for correct, incorrects in self.contemporary_philosophers.items():
            for incorrect in incorrects:
                self.corrections[incorrect.lower()] = correct
            self._canonical_names.add(correct)
            for v in incorrects:
                self._name_variants[self._normalize(v)] = correct

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
            # More transcription errors and philosophical terms
            'capacidadi': 'capacidade',
            'capacida di': 'capacidade',
            'sofistica da': 'sofisticada',
            'intelectu al': 'intelectual',
            # Specific corrections for the reported text
            'hamartianeamente': 'historicamente',  # corrected to proper philosophical term
            'ptechne': 'techne',
            # Additional specific corrections from user feedback
            'historicamnete': 'historicamente',
            'historicamente inute': 'historicamente ineficaz',
            'historicamente inuteis': 'historicamente ineficazes',

            'e spantoso': 'espantoso',
            'pequeníssimos': 'pequeníssimos',
            'maior': 'maior',
            'acompanhar': 'acompanhar',
            'abordar': 'abordar',
            'sofisticada': 'sofisticada',
            'intelectual': 'intelectual',
            'seguinte': 'seguinte',
            'século seguinte': 'século seguinte',
            'importante': 'importante',
            'influência': 'influência',
            'verdade': 'verdade',
            'movimento': 'movimento',
            'neotomismo': 'neotomismo',
            'neo tomismo': 'neotomismo',
            'tomismo': 'Tomismo',
            'único': 'único',
            'séculos': 'séculos',
            'intelectuais': 'intelectuais',
            'nível': 'nível',
            'quando': 'quando',
            'estava': 'estava',
            'dando': 'dando',
            'gente': 'gente',
            'filosofia': 'filosofia',
            'Tomás': 'Tomás',
            'Aquino': 'Aquino',
            'oportunidade': 'oportunidade',
            'perdida': 'perdida',
            'problema': 'problema',
            'cultura': 'cultura',
            'sacra': 'sacra',
            'profana': 'profana',
            'assim': 'assim',
            'equaciona': 'equaciona',
            'coisa': 'coisa',
            'pode': 'pode',
            'equacionar': 'equacionar',
            'fé': 'fé',
            'razão': 'razão',
            'porque': 'porque',
            'dentro': 'dentro',
            'existem': 'existem',
            'elementos': 'elementos',
            'existe': 'existe',
            'científicos': 'científicos',
            'racionais': 'racionais',
            'também': 'também',
            'colocado': 'colocado',
            'questão': 'questão',
            'dogmática': 'dogmática',
            'muito': 'muito',
            'real': 'real',
            'própria': 'própria',
            'função': 'função',
            'Igreja': 'Igreja',
            'civilização': 'civilização',
            'europeia': 'europeia',
            'assume': 'assume',
            'após': 'após',
            'dissolução': 'dissolução',
            'Império': 'Império',
            'temporariamente': 'temporariamente',
            'certas': 'certas',
            'funções': 'funções',
            'administrativas': 'administrativas',
            'torna': 'torna',
            'lugares': 'lugares',
            'fator': 'fator',
            'ordem': 'ordem',
            'social': 'social',
            'sobrecarregava': 'sobrecarrega',
            'série': 'série',
            'ofereceram': 'ofereceram',
            'ideia': 'ideia',
            'idea': 'ideia',
            'idéia': 'ideia',
            'fazer': 'fazer',
            'preciso': 'preciso',
            'pensar': 'pensar',
            'fórmula': 'fórmula',
            'política': 'política',
            'baseada': 'baseada',
            'Evangelho': 'Evangelho',
            'bocado': 'bocado',
            'difícil': 'difícil',
            'deduzir': 'deduzir',
            'menor': 'menor',
            'dica': 'dica',
            'quanto': 'quanto',
            'ponto': 'ponto',
            'estabelecer': 'estabelecer',
            'Dias': 'dai',
            'César': 'César',
            'fica': 'fica',
            'pouco': 'pouco',
            'nebuloso': 'nebuloso',
            'saber': 'saber',
            'exatamente': 'exatamente',
            'onde': 'onde',
            'começa': 'começa',
            'reino': 'reino',
            'Deus': 'Deus',
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
            # Treat dictionary entries that look like names as variants too
            if incorrect and incorrect[:1].isupper():
                self._name_variants[self._normalize(incorrect)] = correct
    
    def find_and_correct_terms(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Find and correct philosophical terms in text.
        Returns corrected text and list of corrections made.
        """
        corrections = []
        corrected_text = text

        # Apply fuzzy corrections to the original text first
        fuzzy_corrected, fuzzy_corrs = self._fuzzy_correct_names(text)
        if fuzzy_corrs:
            corrections.extend(fuzzy_corrs)
            corrected_text = fuzzy_corrected

        # Then apply exact corrections to the fuzzy-corrected text
        sorted_corrections = sorted(self.corrections.items(), key=lambda x: len(x[0]), reverse=True)

        # Keep track of already corrected positions to avoid overlaps
        corrected_positions = set()

        for incorrect, correct in sorted_corrections:
            pattern = re.compile(re.escape(incorrect), re.IGNORECASE)
            matches = list(pattern.finditer(corrected_text))

            for match in matches:
                start_pos = match.start()
                end_pos = match.end()

                # Check if this match overlaps with any already corrected position
                overlap = False
                for corr_start, corr_end in corrected_positions:
                    if (start_pos < corr_end and end_pos > corr_start):
                        overlap = True
                        break

                if overlap:
                    continue

                original = match.group()
                # Preserve case ONLY for single-word tokens; for multi-word, keep canonical form
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

                # Add this position range to the corrected positions
                corrected_positions.add((start_pos, start_pos + len(corrected)))

                corrections.append({
                    'original': original,
                    'corrected': corrected,
                    'position': start_pos
                })

        # Apply context-aware corrections
        corrected_text, context_corrs = self._apply_context_corrections(corrected_text)
        if context_corrs:
            corrections.extend(context_corrs)

        return corrected_text, corrections

    def enhance_academic_structure(self, text: str) -> str:
        """
        Apply MINIMAL corrections to preserve original speech structure and content.
        Focus on terms, words, and mis-transcriptions only - NO restructuring.
        """
        enhanced_text = text

        # Apply term corrections first - these are the core focus
        enhanced_text, corrections = self.find_and_correct_terms(enhanced_text)

        # Apply only the most critical corrections that were specifically mentioned
        critical_corrections = {
            'hamartianeamente': 'historicamente',
            'ptechne': 'techne',
            'capacidadi': 'capacidade',
            'e spantoso': 'espantoso',
            'historicamnete': 'historicamente'
        }

        for wrong, correct in critical_corrections.items():
            enhanced_text = enhanced_text.replace(wrong, correct)

        # MINIMAL improvements - only fix obvious transcription errors
        # Do NOT reorganize structure, add titles, or change the fundamental flow

        # Fix only the most obvious spacing and punctuation issues
        enhanced_text = enhanced_text.replace(' ,', ',')
        enhanced_text = enhanced_text.replace(' .', '.')
        enhanced_text = enhanced_text.replace('  ', ' ')

        return enhanced_text

    def _normalize(self, s: str) -> str:
        """Lowercase and strip accents for robust matching."""
        if not s:
            return s
        s = s.strip().lower()
        nfkd = unicodedata.normalize('NFD', s)
        return ''.join(ch for ch in nfkd if not unicodedata.combining(ch))

    def _is_name_like(self, token: str) -> bool:
        """Heuristic: looks like a proper name token (Title or ALLCAPS)."""
        return bool(re.match(r'^[A-ZÁÀÃÂÉÊÍÓÔÕÚÇ][a-záàãâéêíóôõúç]+$', token)) or token.lower() in {'de', 'da', 'do', 'dos', 'das'}

    def _extract_name_candidates(self, text: str) -> List[Tuple[int, int, str]]:
        """Extract candidate name spans (start, end, substring)."""
        candidates: List[Tuple[int, int, str]] = []
        # Tokenize with positions
        for m in re.finditer(r'\b[\wÀ-ÿ]+\b', text):
            pass
        tokens = [(m.start(), m.end(), text[m.start():m.end()]) for m in re.finditer(r'\b[\wÀ-ÿ]+\b', text)]
        n = len(tokens)
        i = 0
        while i < n:
            if self._is_name_like(tokens[i][2]):
                # try to extend window up to 5 tokens including particles
                j = i + 1
                last_valid = i
                while j < n and (self._is_name_like(tokens[j][2])) and (j - i) < 6:
                    last_valid = j
                    j += 1
                if last_valid > i:
                    start = tokens[i][0]
                    end = tokens[last_valid][1]
                    substring = text[start:end]
                    # Ensure at least two significant tokens (not only particle)
                    parts = [t[2] for t in tokens[i:last_valid+1] if t[2].lower() not in {'de','da','do','dos','das'}]
                    if len([p for p in parts if p and p[0].isupper()]) >= 2:
                        candidates.append((start, end, substring))
                    i = last_valid + 1
                    continue
            i += 1
        return candidates

    def _best_name_match(self, candidate: str) -> Tuple[str, float]:
        """Return best canonical name and score for candidate."""
        norm = self._normalize(candidate)
        best_score = 0.0
        best_canonical = ''
        # Check direct variants first
        variant_canonical = self._name_variants.get(norm)
        if variant_canonical:
            return variant_canonical, 1.0
        # Fuzzy compare against all known variants and canonical names
        for variant, canonical in self._name_variants.items():
            # Skip if this would create a duplication with exact corrections
            if norm in [self._normalize(k) for k in self.corrections.keys()]:
                continue
            score = SequenceMatcher(None, norm, variant).ratio()
            if score > best_score:
                best_score = score
                best_canonical = canonical
        return best_canonical, best_score

    def _fuzzy_correct_names(self, text: str) -> Tuple[str, List[Dict]]:
        """Conservative fuzzy correction for proper names.
        - Only applies to multi-token name-like spans
        - Uses accent-insensitive matching
        - Requires high similarity (>= 0.90)
        - Skips if identical ignoring accents
        """
        corrections: List[Dict] = []
        if not self._name_variants:
            return text, corrections

        spans = self._extract_name_candidates(text)
        # Process from left to right, updating offsets
        offset = 0
        s = text
        for start, end, substr in spans:
            start += offset
            end += offset
            canonical, score = self._best_name_match(substr)
            if not canonical or score < 0.90:
                continue
            # Skip if already same ignoring accents/case
            if self._normalize(substr) == self._normalize(canonical):
                continue
            # Preserve typical Portuguese casing: particles lower, names Title
            def title_portuguese(name: str) -> str:
                parts = name.split()
                out = []
                for p in parts:
                    pl = p.lower()
                    if pl in {'de','da','do','dos','das','e'}:
                        out.append(pl)
                    else:
                        out.append(p[:1].upper() + p[1:])
                return ' '.join(out)

            replacement = title_portuguese(canonical)
            # If replacement would duplicate adjacent particle (e.g., "de Aquino" right after), skip
            tail = s[end:end+12]
            if self._normalize(replacement.split()[-1]) in {self._normalize(w) for w in tail.split()[:2]}:
                continue
            s = s[:start] + replacement + s[end:]
            delta = len(replacement) - (end - start)
            offset += delta
            corrections.append({
                'original': substr,
                'corrected': replacement,
                'position': start,
                'type': 'name_fuzzy'
            })

        return s, corrections

    def _apply_context_corrections(self, text: str) -> Tuple[str, List[Dict]]:
        """Apply context-aware corrections for ambiguous terms."""
        corrections = []
        corrected_text = text

        # Context-aware corrections dictionary
        context_rules = {
            # 'ser' vs 'Ser' - capitalize when referring to Heidegger's Being
            r'\bser\b': {
                'contexts': [
                    (r'heidegger', 'Ser'),
                    (r'ontologia', 'Ser'),
                    (r'existência', 'Ser'),
                    (r'ente', 'Ser'),
                    (r'dasein', 'Ser'),
                    (r'próprio', 'Ser'),
                    (r'autêntico', 'Ser'),
                    (r'inautêntico', 'Ser')
                ]
            },
            # 'ser' should remain lowercase in other contexts (to be/being)
            r'\bSer\b': {
                'contexts': [
                    (r'é\s|é\s', 'ser'),  # After é/era
                    (r'foi\s|era\s', 'ser'),  # After foi/era
                    (r'não\s', 'ser'),  # After não
                    (r'poderia\s', 'ser'),  # After poderia
                    (r'deveria\s', 'ser'),  # After deveria
                    (r'como\s', 'ser'),  # After como
                    (r'que\s', 'ser')  # After que
                ]
            },
            # 'verdade' vs 'Verdade' - capitalize in absolute sense
            r'\bverdade\b': {
                'contexts': [
                    (r'absoluta', 'Verdade'),
                    (r'eterna', 'Verdade'),
                    (r'divina', 'Verdade'),
                    (r'suprema', 'Verdade'),
                    (r'ontológica', 'Verdade'),
                    (r'última', 'Verdade')
                ]
            },
            # 'bem' vs 'Bem' - capitalize when referring to the Good
            r'\bbem\b': {
                'contexts': [
                    (r'idea do', 'Bem'),
                    (r'forma do', 'Bem'),
                    (r'ontológico', 'Bem'),
                    (r'platônico', 'Bem'),
                    (r'supremo', 'Bem'),
                    (r'em si', 'Bem')
                ]
            }
        }

        for pattern, rules in context_rules.items():
            for match in re.finditer(pattern, corrected_text, re.IGNORECASE):
                original = match.group()
                start_pos = match.start()
                end_pos = match.end()

                # Get context around the match (50 chars before and after)
                context_start = max(0, start_pos - 50)
                context_end = min(len(corrected_text), end_pos + 50)
                context = corrected_text[context_start:context_end].lower()

                for context_pattern, correction in rules['contexts']:
                    if re.search(context_pattern, context):
                        # Apply the correction
                        if original.isupper():
                            corrected = correction.upper()
                        elif original.istitle():
                            corrected = correction.capitalize()
                        else:
                            corrected = correction.lower()

                        corrected_text = (corrected_text[:start_pos] + corrected +
                                        corrected_text[end_pos:])

                        corrections.append({
                            'original': original,
                            'corrected': corrected,
                            'position': start_pos,
                            'type': 'context_aware'
                        })
                        break

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
            "Work directly with BP: Process Brazilian Portuguese content natively without translation layers",
            "BP-specific vocabulary: Add Portuguese philosophical terms directly to Whisper's vocabulary",
            "Context priming in BP: Provide philosophical context in Brazilian Portuguese before transcription",
            "Multi-pass refinement: Use Whisper for initial transcription, then apply BP-specific corrections",
            "Speaker identification: Use Whisper's speaker diarization for dialogue-heavy philosophical content",
            "Custom BP vocabulary: Include terms like 'fenomenologia', 'existencialismo', 'metafísica' in vocabulary",
            "Post-processing: Apply BP-specific corrections after Whisper transcription",
            "Confidence scoring: Use Whisper's confidence scores to identify uncertain philosophical transcriptions"
        ]
