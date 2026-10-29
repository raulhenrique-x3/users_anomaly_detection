"""Config central do projeto: caminhos e parâmetros editáveis em um lugar só."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
FEATURES_DIR = DATA_DIR / "features"
MODELS_DIR = DATA_DIR / "models"
OUTPUT_DIR = DATA_DIR / "output"

# Fontes de log do CERT r4.2 (um CSV por fonte em data/raw/r4.2/)
DATA_SOURCES = ["logon", "device", "http", "email", "file"]
RAW_DIR_CERT = RAW_DIR / "r4.2"

# Ground truth (answers/insiders.csv): coluna dataset == GROUND_TRUTH_RELEASE
ANSWERS_DIR = RAW_DIR / "answers"
GROUND_TRUTH_RELEASE = "4.2"

# Formato de data nos CSVs do CERT
DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

# Definição de "noite" para features de fora do expediente (Spec 05)
NIGHT_START = 0   # 00:00 inclusivo
NIGHT_END = 6     # até 06:00 exclusivo

# Domínio da organização fictícia (emails internos = @dtaa.com)
ORG_DOMAIN = "@dtaa.com"

# Sites de busca de emprego: padrão de URL clássico usado pela literatura
# sobre o CERT r4.2 (proxy de insider prestes a sair)
JOB_SITE_PATTERNS = ["jobsearch", "careerbuilder", "simplyhired", "jobs.org",
                     "job-hunt", "cvtips", "salary.com"]

RANDOM_SEED = 42
