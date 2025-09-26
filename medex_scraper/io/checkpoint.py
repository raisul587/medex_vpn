import json


def save_checkpoint(page_number: int):
    checkpoint_data = {"last_page": page_number}
    with open("scraper_checkpoint.json", "w") as f:
        json.dump(checkpoint_data, f)


def load_checkpoint():
    try:
        with open("scraper_checkpoint.json", "r") as f:
            checkpoint_data = json.load(f)
            return checkpoint_data.get("last_page", None)
    except FileNotFoundError:
        return None
