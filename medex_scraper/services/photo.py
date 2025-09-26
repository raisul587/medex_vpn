import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_product_photo(session, url: str):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)
        driver.get(url)

        try:
            image_element = driver.find_element(By.XPATH, '//*[@id="ms-block"]/section/div[5]/div[1]/div[4]/div[2]/a/img')
            image_url = image_element.get_attribute("src")
        except Exception:
            try:
                image_element = driver.find_element(By.XPATH, '//*[@id="ms-block"]/section/div[5]/div[1]/div[4]/div[2]/div[1]/a/img')
                image_url = image_element.get_attribute("src")
            except Exception:
                driver.quit()
                return None

        # Download the image data with retry
        response = session.get(image_url, timeout=10)
        driver.quit()

        if response.status_code == 200:
            image_data = response.content
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            return image_base64

    except Exception as e:
        print(f"Error getting photo: {e}")
        if 'driver' in locals():
            driver.quit()
    return None
