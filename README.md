## Overview
- Scrapes brand pages from `https://medex.com.bd`
- Extracts product details and the product photo (as Base64)
- Writes rows to a CSV file `medex_scraper_data.csv`
- Maintains a checkpoint in `scraper_checkpoint.json` to allow pause & resuming
- Handles Terms of Use redirections by rotating VPN via the hide.me application on Windows

## Structure
```
Medex_vpn_/
  README.md
  run.py                 # Entry point 
  medex_scraper/
    __init__.py
    config.py            # Constants and HTTP session with retry
    io/
      __init__.py
      csv_io.py          # init_csv() and write_to_csv()
      checkpoint.py      # save_checkpoint(), load_checkpoint()
    services/
      __init__.py
      vpn.py             # reconnect_vpn(), check_vpn_status(), wait_for_vpn()
      photo.py           # get_product_photo()
    scraping/
      __init__.py
      page.py            # scrape_page()
      runner.py          # scrape_parallel()
```

## How it works
- `run.py` imports `scrape_parallel()` and orchestrates the scraping flow
- `config.py` configures the `requests` session with retry logic and defines constants:
  - `BASE_URL`
  - `CSV_FILE`
  - `COLUMNS`
- `scraping/page.py` scrapes a single page and returns a row aligned with `COLUMNS`.
- `services/photo.py` uses Selenium (headless Chrome) to capture the product image URL and downloads it via the shared session.
- `io/csv_io.py` initializes the CSV (if missing) and appends rows safely.
- `io/checkpoint.py` reads/writes `scraper_checkpoint.json` for pause and resuming.
- `scraping/runner.py` loops through pages, buffers rows, handles Terms-of-Use redirections by calling the VPN service, writes CSV periodically, and saves checkpoints.

## Requirements
- Python 3.9+
- Packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `urllib3` (for Retry)

- ChromeDriver compatible with your installed Chrome. Place it in PATH or manage via Selenium Manager (Selenium 4.6+).

- Windows + hide.me VPN app installed at:
  - `C:\\Program Files (x86)\\hide.me VPN\\Hide.me.exe`

## Usage
1. Ensure dependencies are installed:
   ```bash
   pip install requests beautifulsoup4 selenium urllib3
   ```

2. From the project root run:
   ```bash
   python "Medex Scraper/run.py"
   ```

3. The script will:
   - Initialize or use `medex_scraper_data.csv`
   - Start scraping from `start_page` to `end_page`
   - Save progress in `scraper_checkpoint.json`
