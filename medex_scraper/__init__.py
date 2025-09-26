# Expose key functions for convenience
from .scraping.runner import scrape_parallel
from .scraping.page import scrape_page
from .services.photo import get_product_photo
from .services.vpn import reconnect_vpn, check_vpn_status, wait_for_vpn
from .io.csv_io import init_csv, write_to_csv
from .io.checkpoint import save_checkpoint, load_checkpoint
from .config import BASE_URL, CSV_FILE, COLUMNS, create_session
