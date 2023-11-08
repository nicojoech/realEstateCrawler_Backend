from bs4 import BeautifulSoup
import json
import os
from datetime import datetime


class Extractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract_data(self):
        # We look for <div> tags that contain an <a> and a <button> tag as this seems to be a unique combination
        entries = []
        for div in self.soup.find_all('div'):
            a_tag = div.find('a', recursive=False)
            button_sibling = div.find('button', recursive=False)
            # Check if both tags are present and then process
            if a_tag and button_sibling:
                entries.append(a_tag)

        entries_list = []
        # Now iterate over each entry and extract the required information
        for entry in entries:
            entry_data = {
                'link': entry.get('href'),
                'title': entry.find('h3').get_text(strip=True) if entry.find('h3') else None,
                'address': entry.find('span', {'aria-label': True}).get_text(strip=True) if entry.find('span', {
                    'aria-label': True}) else None,
                'price': entry.select_one('span[data-testid^="search-result-entry-price"]').get_text(strip=True)
                if entry.select_one('span[data-testid^="search-result-entry-price"]') else None
            }
            entries_list.append(entry_data)

    def save_data(self, data):
        dir_name = './crawled_data'
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M") + '.json'
        file_path = os.path.join(dir_name, file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
