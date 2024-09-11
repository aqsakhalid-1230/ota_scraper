import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

class HotelScraper:
    def __init__(self, proxies=None, scroll_pause_time=2, max_scroll_attempts=3):
        self.url = 'https://us.trip.com/hotels/list?city=1187&locale=en-US&curr=USD'
        self.proxies = proxies
        self.proxy_index = 0
        self.scroll_pause_time = scroll_pause_time
        self.max_scroll_attempts = max_scroll_attempts
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = self._get_chrome_options()

        if self.proxies:
            proxy = self._get_next_proxy()
            chrome_options.add_argument(f'--proxy-server={proxy}')

        return webdriver.Chrome(options=chrome_options)

    def _get_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        return chrome_options

    def _get_next_proxy(self):
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def scrape_hotels(self):
        self.driver.get(self.url)
        self._scroll_until_no_more_content()

        self._wait_for_listings()

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        hotels_data = self._extract_hotel_data(soup)

        self.driver.quit()
        return hotels_data

    def _scroll_until_no_more_content(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0

        while True:
            self._scroll_to_bottom()
            new_height = self._get_page_height()

            if new_height == last_height:
                scroll_attempts += 1
                if scroll_attempts >= self.max_scroll_attempts:
                    break
            else:
                scroll_attempts = 0

            last_height = new_height

    def _scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.scroll_pause_time)

    def _get_page_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def _wait_for_listings(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'long-list'))
        )

    def _extract_hotel_data(self, soup):
        ul_element = soup.find('ul', class_='long-list long-list-v8 version-b')
        li_tags = ul_element.find_all('li')
        room_li_tags = [li for li in li_tags[1:] if li.find('div', class_='with-decorator-wrap-v8')]

        return [
            self._parse_hotel_data(li) for li in room_li_tags
        ]

    def _parse_hotel_data(self, li):
        hotel_name = li.select_one('.list-card-title .name').text.strip()
        location = li.find('p', class_='transport').find_all('span')[1].text.strip()
        room_type = li.find('div', class_='room-type').find_all('span')[0].text.strip()
        price = li.select_one('.room-panel-price #meta-real-price').text.strip()

        return {
            'Hotel Name': hotel_name,
            'Location': location,
            'Room Types': room_type,
            'Prices': price
        }

    def save_to_csv(self, hotels_data, filename):
        fieldnames = ['Hotel Name', 'Location', 'Room Types', 'Prices']
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(hotels_data)
        print(f"Hotel data has been saved to {filename}")


if __name__ == "__main__":
    proxies = [
      "http://127.0.0.1:8080",
      "http://127.0.0.1:8081",
      "http://127.0.0.1:8082"
    ]

    scraper = HotelScraper(proxies)
    hotels_data = scraper.scrape_hotels()

    print(hotels_data)
    scraper.save_to_csv(hotels_data, 'scraped_hotels_data.csv')
