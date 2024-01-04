"""
This file contains the Extractor class which is responsible for extracting data from the HTML.
Extracted data gets saved to a JSON file.
"""
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime


def _zip_code_to_state(zip_code):
    """
    Helper function to map zip codes to states.
    Taken from: http://www.mcca.or.at/info/at/idxplz.htm
    """
    if zip_code:
        first_digit = int(zip_code[0])
        if first_digit == 1:
            return 'Wien'
        elif first_digit == 2:
            return 'Niederösterreich, Burgenland/Nord'
        elif first_digit == 3:
            return 'Niederösterreich'
        elif first_digit == 4:
            return 'Oberösterreich'
        elif first_digit == 5:
            return 'Salzburg'
        elif first_digit == 6:
            return 'Tirol, Vorarlberg'
        elif first_digit == 7:
            return 'Burgenland/Süd'
        elif first_digit == 8:
            return 'Steiermark'
        elif first_digit == 9:
            return 'Kärnten'
    return None


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


def _extract_title_from_link(link):
    """
    Extracts the title from a willhaben link.
    1. Splits the link by '/' and takes the last title part
    2. Splits the title part by '-' and removes the last part which is a number which returns a list
    3. Joins the list with spaces and returns the title
    """

    return ' '.join(link.split('/')[-2].split('-')[:-1])


def _extract_state_from_link(link):
    """
    Extracts the state from a willhaben link.
    1. Splits the link by '/' and takes the 5th part
    """

    return link.split('/')[5]


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
                return float("{:.2f}".format(num))

        # For other cases, extract the numeric part and convert to int
        else:
            match = re.search(r'\d+(\.\d+)?', text)
            if match:
                return int(match.group())
    return None


def _parse_address(address, link):
    """
    Parses the address into ZIP Code, City, Street, and District (if applicable).
    Additionally parses the state from the link.
    """
    if not address:
        return {"zip_code": None, "state": None, "city": None, "street": None, "district": None}

    # Split the address into components
    parts = address.split(', ')
    zip_and_city = parts[0].split()
    zip_code = zip_and_city[0]
    city = ' '.join(zip_and_city[1:])
    state = _extract_state_from_link(link)

    street = parts[1] if len(parts) > 1 else None
    district = None

    # Special handling for Vienna addresses
    if city == "Wien" and len(parts) > 2:
        # Extracting the district number
        district = parts[1].split('.')[0] + '. Bezirk'
        street = parts[2] if len(parts) > 2 else None

    return {"zip_code": zip_code, "state": state, "city": city, "street": street, "district": district}


class Extractor:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract_data(self):
        # Debugging line
        # print(self.soup.prettify())

        entries = self.soup.select('a[id^="search-result-entry-header-"]')

        entries_list = []

        print(f"Found {len(entries)} entries - Extracting data")

        for entry in entries:
            link = entry.get('href')

            # Regex patterns for area and number of rooms
            area_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-0')
            rooms_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-1')
            additional_info_pattern = re.compile(r'search-result-entry-teaser-attributes-\d+-2')

            address = _extract_text(entry, tag_name='span', attrs={'aria-label': True})
            parsed_address = _parse_address(address, link)

            entry_data = {
                'link': link,
                'title': _extract_title_from_link(link),
                'address': parsed_address,

                'area': _extract_numeric_part(
                    _extract_text(entry, pattern=area_pattern)
                ),
                'number_of_rooms': _extract_numeric_part(
                    _extract_text(entry, pattern=rooms_pattern)
                ),
                'additional_info': _extract_text(entry, pattern=additional_info_pattern),
                'price': _extract_numeric_part(
                    _extract_text(entry, css_selector='span[data-testid^="search-result-entry-price"]')
                )
            }
            entries_list.append(entry_data)

        # Debugging line
        # print(entries_list)

        return entries_list  # Ensure this is returned

    def filter_data(self, data, zip_code=None, number_of_rooms=None, state=None):
        """
        Filters the data based on ZIP code, number of rooms, and state.
        """
        filtered_data = []
        print("Filtering extracted data..")
        for entry in data:
            entry_state = _zip_code_to_state(entry['address']['zip_code'])

            # Apply ZIP code filter
            if zip_code and entry['address']['zip_code'] != zip_code:
                continue

            # Apply number of rooms filter
            if number_of_rooms and entry.get('number_of_rooms') != number_of_rooms:
                continue

            # Apply state filter
            if state and entry_state != state:
                continue

            filtered_data.append(entry)

        print(f"Found {len(filtered_data)} entries - Extracting data")

        return filtered_data

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

        dir_name = 'crawled_data'
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M") + '.json'
        file_path = os.path.join(dir_name, file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            # Debugging line
            # print(f"Saving data to {file_path}")
            json.dump(data, f, indent=4, ensure_ascii=False)
