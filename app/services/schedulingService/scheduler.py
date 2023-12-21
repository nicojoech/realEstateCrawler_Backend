import threading
import time
from datetime import datetime, timedelta
from app.services.webcrawlerService.crawler import Crawler
from app.services.webcrawlerService.extractor import Extractor
from app.services.emailService.emailSender import send, send_formatted_listings


class Scheduler:
    """
    Scheduler class to perform the crawling at a given interval and duration

    Example usage:
    # Start crawling with default values
    service = SchedulingService(interval_hours=1, duration_hours=24, receiver_email="user@example.com",
        crawler_filter={"max_price": "300", "min_area": "50"}, zip_code="1100", number_of_rooms=4, state="Wien")
    service.start_crawling()

    Note: Best to use only state or zip_code, not both

    # Stop crawling
    service.stop_crawling()
    """

    def __init__(self, interval_hours: int = 1, duration_hours: int = 24, receiver_email: str | None = None,
                 crawler_filter: dict | None = None, zip_code: str | None = None, number_of_rooms: int | None = None,
                 state: str | None = None):
        self.interval_hours = interval_hours
        self.duration_hours = duration_hours
        self.crawler_filter = crawler_filter
        self.zip_code = zip_code
        self.number_of_rooms = number_of_rooms
        self.state = state
        self.receiver_email = receiver_email
        self.start_time = None
        self.end_time = None
        self.found_listings = []
        self.crawling_thread = None
        self.stop_requested = threading.Event()
        self.processed_listings = set()

    def _crawl(self) -> None:
        """
        Private method to perform the crawling
        :return:
        """
        url = "https://www.willhaben.at/iad/immobilien"  # Currently only willhaben crawlable

        # filters_dict = {
        #     "max_price": "300",
        #     "min_area": "50"
        # }

        crawler = Crawler(base_url=url, filters_dict=self.crawler_filter)
        while datetime.now() < self.end_time and not self.stop_requested.is_set():
            page_source = crawler.crawl()  # Perform the crawl

            extractor = Extractor(page_source)  # Initialize an extractor with the crawled page html source
            listings = extractor.extract_data()  # Extract the real estate listings from the page source
            filtered_listings = (extractor
                                 .filter_data(data=listings,
                                              zip_code=self.zip_code,
                                              number_of_rooms=self.number_of_rooms,
                                              state=self.state)
                                 )

            unique_listings = [listing for listing in filtered_listings if
                               listing['link'] not in self.processed_listings]
            if unique_listings:
                self.found_listings.extend(unique_listings)
                send_formatted_listings(self.receiver_email, unique_listings)
                self.processed_listings.update(listing['link'] for listing in unique_listings)

                # Use an interruptable wait instead of time.sleep()
                self.stop_requested.wait(
                    # self.interval_hours * 3600)  # Wait for the next interval 3600 because hourly in seconds
                    self.interval_hours * 120)  # for testing purposes

        # Send final notification
        if self.stop_requested.is_set():
            print("Crawling process has been manually stopped.")
            send(self.receiver_email, "Crawling process has been manually stopped.")
        elif self.found_listings:
            print(f"Number of findings: {len(self.found_listings)}")
            send(self.receiver_email, f"Summary of findings: {self.found_listings}")
        else:
            print("No listings found during the crawling period.")
            send(self.receiver_email, "No listings found during the crawling period.")

    def start_crawling(self) -> None:
        """
        Starts the crawling process in a separate thread
        :return:
        """

        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=2)#hours=self.duration_hours)
        crawling_thread = threading.Thread(target=self._crawl)
        crawling_thread.start()

        # Optional: Send a notification that the service has started
        print("Crawling service has started.")
        send(self.receiver_email, "Crawling service has started.")

    def stop_crawling(self):
        """
        Stops the crawling process.
        """
        self.stop_requested.set()
        if self.crawling_thread:
            print("Waiting for crawling thread to finish...")
            self.crawling_thread.join()


def main():
    service = Scheduler(interval_hours=1, duration_hours=1, receiver_email="wi21b026@technikum-wien.at",
                        crawler_filter={"max_price": "300", "min_area": "50"}, zip_code="3202", number_of_rooms=2)
    service.start_crawling()


if __name__ == '__main__':
    main()
