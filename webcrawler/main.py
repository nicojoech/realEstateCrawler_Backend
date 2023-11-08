from crawler import Crawler
from extractor import Extractor


def main():
    url = "https://www.willhaben.at/iad/immobilien"

    crawler = Crawler(base_url=url)
    page_source = crawler.crawl()

    extractor = Extractor(page_source)
    data = extractor.extract_data()
    extractor.save_data(data)


if __name__ == '__main__':
    main()
