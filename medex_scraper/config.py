import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Base URL
BASE_URL = "https://medex.com.bd/brands/"

# CSV File Configuration
CSV_FILE = "medex_scraper_data.csv"
COLUMNS = [
    "Brand Name", "Dosage Form", "Generic Name", "Strength",
    "Manufactured By", "Price", "Pack_Size_Info", "Indications",
    "Pharmacology", "Dosage & Administration", "Interaction",
    "Contraindications", "Side Effects", "Pregnancy & Lactation",
    "Precautions & Warnings", "Use in Special Populations",
    "Therapeutic Class", "Storage Conditions", "Photo"
]


def create_session() -> requests.Session:
    """Create a requests session with retry strategy identical to the original script."""
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
