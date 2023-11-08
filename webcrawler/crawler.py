from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import Edge, EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def _init_driver():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = Edge(options=options, executable_path=EdgeChromiumDriverManager().install())
    return driver


class Crawler:

    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = _init_driver()

    def open_page(self, url):
        self.driver.get(url)

    def click_button(self, button_selector):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_selector))
        )
        button.click()

    def get_page_source(self):
        return self.driver.page_source

    def close_browser(self):
        self.driver.quit()

    def crawl(self):
        try:
            self.open_page(self.base_url)

            # Wait for cookies dialog and decline
            try:
                self.click_button('//*[@id="didomi-notice-disagree-button"]')
            except Exception as e:
                print(f"Could not find or interact with cookies dialog: {e}")
                return

            # Wait for search button and click
            try:
                self.click_button('//button[@type="button" and @data-testid="search-submit-button"]')
            except Exception as e:
                print(f"Could not find or interact with the search button: {e}")
                return

            # Additional wait to ensure page has loaded after search
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//div[.//a and .//button]'  # Adjusted XPath  # Again, adjust this XPath to your needs
                ))
            )

            self.close_browser()
            return self.driver.page_source
        finally:
            self.close_browser()
