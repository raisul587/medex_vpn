from concurrent.futures import ThreadPoolExecutor
from .page import scrape_page
from ..io.csv_io import write_to_csv
from ..io.checkpoint import save_checkpoint, load_checkpoint
from ..services.vpn import reconnect_vpn, wait_for_vpn
from ..config import COLUMNS, create_session


def scrape_parallel(start_page: int, end_page: int, max_workers: int = 10):
    # Load checkpoint if exists
    checkpoint = load_checkpoint()
    if checkpoint is not None:
        current_page = checkpoint
        print(f"Resuming from checkpoint at page {current_page}")
    else:
        current_page = start_page

    # Buffer to store results before writing to CSV
    results_buffer = []

    session = create_session()

    try:
        while current_page < end_page:
            print(f"\nProcessing page {current_page}")

            # We keep max_workers=1 to preserve original behavior
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(scrape_page, current_page, session)

                try:
                    result = future.result()
                    if result == "NEED_VPN_ROTATION":
                        print("\nHit Terms of Use page. Saving current data...")
                        # Always save data before VPN rotation
                        if results_buffer:
                            write_to_csv(results_buffer)
                            print(f"Saved {len(results_buffer)} records to CSV")
                            results_buffer = []

                        print("Rotating VPN...")
                        if reconnect_vpn() and wait_for_vpn():
                            print("VPN rotated successfully. Continuing...")
                            continue  # Retry the same page
                        else:
                            print("Failed to rotate VPN. Saving progress and exiting...")
                            save_checkpoint(current_page - 1)
                            return
                    elif result:
                        print(f"Successfully scraped page {current_page}")
                        results_buffer.append(result)
                        save_checkpoint(current_page)

                        # Write to CSV every 10 successful scrapes to avoid data loss
                        if len(results_buffer) >= 10:
                            write_to_csv(results_buffer)
                            print(f"Saved {len(results_buffer)} records to CSV")
                            results_buffer = []
                    else:
                        print(f"No data found for page {current_page}")

                except Exception as e:
                    print(f"Error processing page {current_page}: {e}")
                    # Save any data we have if there's an error
                    if results_buffer:
                        write_to_csv(results_buffer)
                        print(f"Saved {len(results_buffer)} records to CSV after error")
                        results_buffer = []

            current_page += 1

    except KeyboardInterrupt:
        print("\nScraping interrupted. Saving current data...")
        if results_buffer:
            write_to_csv(results_buffer)
            print(f"Saved {len(results_buffer)} records to CSV before exit")
        save_checkpoint(current_page - 1)
        print("Data saved successfully. Run again to continue from the last checkpoint.")
        return
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Saving current data...")
        if results_buffer:
            write_to_csv(results_buffer)
            print(f"Saved {len(results_buffer)} records to CSV after error")
        save_checkpoint(current_page - 1)
        raise

    # Save any remaining data in the buffer
    if results_buffer:
        write_to_csv(results_buffer)
        print(f"Saved final {len(results_buffer)} records to CSV")
