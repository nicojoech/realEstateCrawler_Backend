from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


def _init_driver():
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
    return driver


class Crawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = _init_driver()

    def open_page(self, url):
        self.driver.get(url)

    def click_button(self, button_selector):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        )
        button.click()

    def get_page_source(self):
        return self.driver.page_source

    def close_browser(self):
        self.driver.quit()

    def crawl(self):
        self.open_page(self.base_url)

        # Wait for cookies dialog and decline
        try:
            self.click_button('#didomi-notice-disagree-button')
        except Exception as e:
            print(f"Could not find or interact with cookies dialog: {e}")

        # Wait for search button and click
        self.click_button('//button[@type="button" and @data-testid="search-submit-button"]')

        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                # This is the div that contains a real estate entry
                '//div[contains(@class, "Box-sc-*")]'
            ))
        )

        self.close_browser()
        self.get_page_source()
