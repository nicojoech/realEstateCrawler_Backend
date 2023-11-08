from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

class Extractor:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extract_data(self):
        # TODO: Extract data from soup
        #entries = self.soup.find_all('div', class_='ResultListAdRowLayout___StyledBox-sc-1rmys2w-0')
        pass

    def save_data(self, data):
        dir_name = './crawled_data'
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M") + '.json'
        file_path = os.path.join(dir_name, file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)