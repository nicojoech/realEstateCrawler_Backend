from crawler import Crawler
from extractor import Extractor
import sys


def main():
    url = "https://www.willhaben.at/iad/immobilien"

    filters_dict = {
        "max_price": "300",
        "min_area": "50"
    }

    crawler = Crawler(base_url=url, filters_dict=filters_dict)
    page_source = crawler.crawl()

    extractor = Extractor(page_source)
    data = extractor.extract_data()
    filtered_data = extractor.filter_data(data=data, zip_code="4600", number_of_rooms=3)
    extractor.save_data(filtered_data)
    sys.exit(0)


if __name__ == '__main__':
    main()
