from bs4 import BeautifulSoup
import time
import requests
from ..config import BASE_URL, COLUMNS
from ..services.photo import get_product_photo


def scrape_page(page_number: int, session: requests.Session):
    url = f"{BASE_URL}{page_number}"
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=10)

            # Check status code first (most efficient)
            if response.status_code == 404:
                print(f"Page {page_number} not found (404). Skipping.")
                return None

            # Only parse HTML if status code is OK
            soup = BeautifulSoup(response.text, "html.parser")

            # Check for terms of use page
            if "terms-of-use" in response.url:
                print(f"Redirected to Terms of Use page at {page_number}. Need VPN rotation.")
                return "NEED_VPN_ROTATION"

            # Helper function for robust section content extraction
            def get_section_content(section_id):
                section = soup.find("div", {"id": section_id})
                if section:
                    content_div = section.find_next("div", class_="ac-body")
                    return content_div.get_text(strip=True) if content_div else None
                return None

            # Extract all data with proper error handling
            data = {
                "Brand Name": None,
                "Dosage Form": None,
                "Generic Name": None,
                "Strength": None,
                "Manufactured By": None,
                "Price": None,
                "Pack_Size_Info": None,
                "Indications": None,
                "Pharmacology": None,
                "Dosage & Administration": None,
                "Interaction": None,
                "Contraindications": None,
                "Side Effects": None,
                "Pregnancy & Lactation": None,
                "Precautions & Warnings": None,
                "Use in Special Populations": None,
                "Therapeutic Class": None,
                "Storage Conditions": None,
                "Photo": None
            }

            # Basic information
            brand_elem = soup.find("h1", class_="page-heading-1-l brand")
            data["Brand Name"] = brand_elem.text.strip() if brand_elem else None

            if not data["Brand Name"] and "Terms of Use" in soup.get_text():
                return "NEED_VPN_ROTATION"

            dosage_elem = soup.find("small", class_="h1-subtitle")
            data["Dosage Form"] = dosage_elem.text.strip() if dosage_elem else None

            generic_elem = soup.find("div", title="Generic Name")
            data["Generic Name"] = generic_elem.text.strip() if generic_elem else None

            strength_elem = soup.find("div", title="Strength")
            data["Strength"] = strength_elem.text.strip() if strength_elem else None

            manufacturer_elem = soup.find("div", title="Manufactured by")
            data["Manufactured By"] = manufacturer_elem.text.strip() if manufacturer_elem else None

            price_elem = soup.select_one('span:-soup-contains("৳")')
            data["Price"] = price_elem.text.strip() if price_elem else None

            pack_size_elem = soup.find("span", class_="pack-size-info")
            data["Pack_Size_Info"] = pack_size_elem.text.strip() if pack_size_elem else None

            # Section content
            data["Indications"] = get_section_content("indications")
            data["Pharmacology"] = get_section_content("mode_of_action")
            data["Dosage & Administration"] = get_section_content("dosage")
            data["Interaction"] = get_section_content("interaction")
            data["Contraindications"] = get_section_content("contraindications")
            data["Side Effects"] = get_section_content("side_effects")
            data["Pregnancy & Lactation"] = get_section_content("pregnancy_cat")
            data["Precautions & Warnings"] = get_section_content("precautions")
            data["Use in Special Populations"] = get_section_content("pediatric_uses")
            data["Therapeutic Class"] = get_section_content("drug_classes")
            data["Storage Conditions"] = get_section_content("storage_conditions")

            # Get photo
            data["Photo"] = get_product_photo(session, url)

            # Return data in the same order as COLUMNS
            return [data[col] for col in COLUMNS]

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for page {page_number}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Error scraping page {page_number} after {max_retries} attempts: {e}")
                return None
        except Exception as e:
            print(f"Error scraping page {page_number}: {e}")
            return None
