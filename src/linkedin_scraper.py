from playwright.sync_api import sync_playwright
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkedInScraper:
    def __init__(self, cookies, url, headless=True):
        self.cookies = cookies
        self.url = url
        self.headless = headless
        self.browser = None
        self.page = None

    def start_browser(self):
        """Starts a Playwright browser instance."""
        playwright = sync_playwright().start()
        self.browser = playwright.firefox.launch(headless=False)
        self.page = self.browser.new_page()

    def close_browser(self):
        """Closes the Playwright browser instance."""
        if self.browser:
            self.browser.close()

    def set_cookies(self):
        """Sets cookies for the page context."""
        try:
            self.page.context.add_cookies(self.cookies)
            logging.info("Cookies have been set successfully.")
        except Exception as e:
            logging.error(f"Failed to set cookies: {e}")

    def navigate_to_url(self):
        """Navigates to a specified URL."""
        try:
            self.page.goto(self.url, wait_until='domcontentloaded')
            logging.info(f'Navigated to {self.url}')
            return True
        except Exception as e:
            logging.error(f'Failed to navigate to {self.url}: {e}')
            return False

    def save_html_content(self, filename):
        """Saves the current page content to an HTML file."""
        try:
            html_content = self.page.content()
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html_content)
            logging.info(f'HTML content saved to {filename}')
        except Exception as e:
            logging.error(f'Failed to save HTML content: {e}')

    def scrape(self, filename):
        """Executes the scraping process."""
        self.start_browser()
        self.set_cookies()
        if self.navigate_to_url():
            time.sleep(10)
            self.save_html_content(filename)
        self.close_browser()
