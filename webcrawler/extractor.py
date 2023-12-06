"""
This file contains the Extractor class which is responsible for extracting data from the HTML.
Extracted data gets saved to a JSON file.
"""
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime


class Extractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    @staticmethod
    def _extract_text(entry, css_selector=None, tag_name=None, attrs=None, pattern=None):
        """
        Extracts text from an entry based on provided css_selector, tag_name, attrs, or pattern.
        """
        if pattern:
            # Regex pattern based extraction
            element = entry.find(lambda tag: tag.name == "div" and pattern.match(tag.get('data-testid', '')))
        elif css_selector:
            # CSS Selector based extraction
            element = entry.select_one(css_selector)
        elif tag_name:
            # Tag name and attributes based extraction
            element = entry.find(tag_name, attrs)
        else:
            return None

        return element.get_text(strip=True) if element else None

    @staticmethod
    def _extract_numeric_part(text):
        """
        Extracts the numeric part from the provided text.
        """
        if text:
            # Check if the text starts with '€' and extract the numeric part and convert to flaot
            if text.strip().startswith('€'):
                # Regex pattern: € followed by 0 or more spaces followed by 1 or more digits can have a comma as decimal
                # separator followed by 0 or more digits
                match = re.search(r'€\s*(\d+(?:,\d+)?)', text)
                if match:
                    # Replace comma with dot for decimal
                    num = float(match.group(1).replace(',', '.'))
                    # Format to 2 decimal places
                    return "{:.2f}".format(num)

            # For other cases, extract the numeric part and convert to int
            else:
                match = re.search(r'\d+(\.\d+)?', text)
                if match:
                    return int(match.group())
        return None

    def extract_data(self):
        # Debugging line
        # print(self.soup.prettify())

        entries = self.soup.select('a[id^="search-result-entry-header-"]')

        entries_list = []

        print(f"Found {len(entries)} entries - Extracting data")

        for entry in entries:
            # Regex patterns for area and number of rooms
            area_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-0')
            rooms_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-1')
            additional_info_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-2')

            entry_data = {
                'link': entry.get('href'),
                'title': self._extract_text(entry, tag_name='h3'),
                'address': self._extract_text(entry, tag_name='span', attrs={'aria-label': True}),

                'area': self._extract_numeric_part(
                    self._extract_text(entry, pattern=area_pattern)
                ),
                'number_of_rooms': self._extract_numeric_part(
                    self._extract_text(entry, pattern=rooms_pattern)
                ),
                'additional_info': self._extract_text(entry, pattern=additional_info_pattern),
                'price': self._extract_numeric_part(
                    self._extract_text(entry, css_selector='span[data-testid^="search-result-entry-price"]')
                )
            }
            entries_list.append(entry_data)

        # Debugging line
        # print(entries_list)

        return entries_list  # Ensure this is returned

    def save_data(self, data):
        """
        Saves the provided data to a JSON file.
        This method saves data to a JSON file in a directory named 'crawled_data'. The filename
        is generated based on the current date and time, ensuring that each saved file has a
        unique name. If the 'crawled_data' directory does not exist, it is created.

        Args:
            data: The data to be saved. This should be a data structure that is compatible with
              json.dump(), such as a dict or a list.

        Returns:
            None: This method does not return any value.

        Note:
            - Ensure that the 'data' parameter is in a format that can be serialized to JSON.
            - The datetime module and os.path are used for generating the file path.
        """
        print("Saving data to JSON file")

        dir_name = './crawled_data'
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M") + '.json'
        file_path = os.path.join(dir_name, file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            # Debugging line
            # print(f"Saving data to {file_path}")
            json.dump(data, f, indent=4, ensure_ascii=False)
