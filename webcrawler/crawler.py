from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


class Crawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = _init_driver()

    def crawl(self):
        self.driver.get(self.base_url)

        # Wait for button to be clickable/loaded
        wait = WebDriverWait(self.driver, 10)
        button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//button[@type="button" and @data-testid="search-submit-button"]'
            ))
        )

        button.click()

        # Wait for page to load
        wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                # This is the div that contains a real estate entry
                '//div[contains(@class, "Box-sc-*")]'
            ))
        )

        page_source = self.driver.page_source
        self.driver.quit()
        return page_source
