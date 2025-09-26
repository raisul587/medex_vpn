from medex_scraper.scraping.runner import scrape_parallel
from medex_scraper.io.csv_io import init_csv
from medex_scraper.config import CSV_FILE
import os

if __name__ == "__main__":
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print("Initializing new CSV file...")
        init_csv()
    else:
        print(f"Using existing CSV file: {CSV_FILE}")

    start_page = 1
    end_page = 25000

    try:
        print(f"Starting scraper from page {start_page} to {end_page}")
        scrape_parallel(start_page, end_page)
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except Exception as e:
        print(f"\nScript stopped due to error: {e}")
