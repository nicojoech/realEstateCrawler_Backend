"""
This module provide a crawler class to crawl the willhaben.at website
It uses selenium to interact with the website and extract the html
"""
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time


# from msedge.selenium_tools import Edge, EdgeOptions
# from webdriver_manager.microsoft import EdgeChromiumDriverManager


# def _init_driver():
#     options = EdgeOptions()
#     options.use_chromium = True
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     driver = Edge(options=options, executable_path=EdgeChromiumDriverManager().install())
#     return driver

def _init_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
    return driver


class Crawler:

    def __init__(self, base_url, filters_dict, crawl_all=False):
        self.base_url = base_url
        self.driver = None
        self.filters_dict = filters_dict
        self.crawl_all = crawl_all

    def open_page(self, url):
        self.driver.get(url)

    def click_button(self, button_selector):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_selector))
        )
        button.click()

    def is_next_page_available(self):
        """
        Check if there's a 'Next' button available for pagination.
        """
        try:
            next_button = self.driver.find_element(By.XPATH,
                                                   '//a[@data-testid="pagination-top-next-button" and not('
                                                   '@aria-disabled="true")]')
            return next_button.is_enabled()
        except NoSuchElementException as e:
            return False

    def go_to_next_page(self):
        """
        Click the 'Next' button to navigate to the next page.
        """
        next_button = self.driver.find_element(By.XPATH, '//a[@data-testid="pagination-top-next-button"]')
        next_button.click()

    def close_browser(self):
        self.driver.quit()

    def scroll_down(self):
        scroll_pause_time = 0.5
        screen_height = self.driver.execute_script("return window.innerHeight;")
        i = 1

        while True:
            # Scroll down by half of the screen height
            self.driver.execute_script(f"window.scrollTo(0, {screen_height * i / 2});")
            i += 1

            # Wait to load the page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if (screen_height * i / 2) > new_height:
                break  # Exit loop when the bottom of the page is reached

    def wait_for_site_load(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//a[starts-with(@id, 'search-result-entry-header-')]"
            ))
        )

    def crawl(self):
        self.driver = _init_driver()
        page_sources = ""
        try:
            print("Crawling...")
            self.open_page(self.base_url)

            # Wait for cookies dialog and decline
            try:
                self.click_button('//*[@id="didomi-notice-disagree-button"]')
            except Exception as e:
                print(f"Could not find or interact with cookies dialog: {e}")
                return

            # Apply filters if max price and min area are provided
            self.apply_filters(**self.filters_dict)

            # Wait for search button and click
            try:
                submit_button = self.driver.find_element(By.XPATH, '//button[@data-testid="search-submit-button"]')
                submit_button.click()
            except Exception as e:
                print(f"Could not find or interact with the search button: {e}")
                return

            while True:
                # Wait for site to load and scroll down
                self.wait_for_site_load()
                self.scroll_down()

                # Append the current page's source to the list
                page_sources = page_sources + self.driver.page_source
                # Crawl all pages if the flag is set and there's a 'Next' button available
                if self.crawl_all and self.is_next_page_available():
                    print("Crawling next page...")
                    self.go_to_next_page()
                    time.sleep(2)  # Adjust this delay as needed
                else:
                    break

            print("Crawling finished. Browser closed.")
            return page_sources
        finally:
            self.close_browser()

    def apply_filters(self, **filters):
        """
        Apply various filters to the search
        Args:
            filters (dict): A dictionary of filters where keys are the filter types (e.g., 'max_price', 'min_area')
                and values are the corresponding values for these filters.

                Supported filters:
                    - 'max_price': Maximum price filter.
                    - 'min_area': Minimum area filter.

        Returns:
            None: This method does not return any value.

        Note:
            - The element IDs used are specific to the 'willhaben' website and may need adjustment
              if used with a different website or interface.
            - The method assumes that 'self.driver' is a valid Selenium WebDriver instance.
        """
        for key, value in filters.items():
            if key == "max_price":
                # Handle max price filter
                max_price_field = WebDriverWait(self.driver, 10).until(
                    # NOTE: ID is willhaben specific
                    EC.presence_of_element_located((By.ID, "navigator-price-to-input"))
                )
                max_price_field.clear()
                max_price_field.send_keys(value)

            elif key == "min_area":
                # Handle area filter
                area_field = WebDriverWait(self.driver, 10).until(
                    # NOTE: ID is willhaben specific
                    EC.presence_of_element_located((By.ID, "navigator-livingarea-from-input"))
                )
                area_field.clear()
                area_field.send_keys(value)

            time.sleep(2)
