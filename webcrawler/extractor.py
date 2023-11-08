from bs4 import BeautifulSoup
import json
import os
from datetime import datetime


class Extractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract_data(self):
        # Debugging line
        # print(self.soup.prettify())

        entries = self.soup.select('a[id^="search-result-entry-header-"]')

        entries_list = []
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

        # Debugging line
        # print(entries_list)

        return entries_list  # Ensure this is returned

    def save_data(self, data):
        dir_name = './crawled_data'
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M") + '.json'
        file_path = os.path.join(dir_name, file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            # Debugging line
            # print(f"Saving data to {file_path}")
            json.dump(data, f, indent=4, ensure_ascii=False)
