import selenium.common.exceptions
from selenium.webdriver.common.by import By
from scraper import Scraper
import re


class NoFluffScraper(Scraper):

    # Constructor
    def __init__(self, link, database_url) -> None:
        super().__init__(database_url)
        self.link = link
        self.links = []

    # functions start

    def __find_links(self) -> None:
        self.driver.get(self.link)
        self.links = [
            el.get_attribute("href")
            for el in self.driver.find_elements(By.CLASS_NAME, "posting-list-item")
        ]

    def __scrap_offer(self, link):
        self.driver.get(link)
        scraped_title = (self.driver.title).split("|")

        # Company Name

        company_name = scraped_title[2].strip()

        # Position Name

        position_name = scraped_title[0][6:-1]

        # Position Level

        position_level = self.driver.find_element(
            By.XPATH,
            "//span[contains(@class, 'mr-10 font-weight-medium ng-star-inserted')]",
        ).text

        # Salary

        try:
            salary = self.driver.find_element(
                By.XPATH, "//h4[contains(@class, 'tw-mb-0')]"
            ).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                salary = self.driver.find_element(
                    By.XPATH,
                    "//span[contains(@class, 'font-weight-bold')]",
                ).text
            except selenium.common.exceptions.NoSuchElementException:
                salary = None

        match = re.findall("\\d+\\.?\\d+", "0 0 " + salary)
        match_currency = re.findall("[A-Z]{3}", salary)
        salary_currency = match_currency[0] if len(match_currency) > 0 else None
        multiplication = 1000 if "k" in salary else 1
        salary_range1 = int(float(match[-2]) * multiplication)
        salary_range2 = int(float(match[-1]) * multiplication)

        # Contract
        try:
            contract_text = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'px-20 py-3 d-flex align-items-center justify-content-between ng-star-inserted')]",
            ).text.lower()
            if "b2b" in contract_text:
                contract = "B2B"
            elif "uop" in contract_text:
                contract = "Permanent"
            elif "uz" in contract_text:
                print("Mandatecontract")
        except selenium.common.exceptions.NoSuchElementException:
            contract = "None"

        # Abilities

        abilities = [
            el.text
            for el in self.driver.find_elements(
                By.XPATH,
                "//span[contains(@class, 'no-cursor text-truncate tw-border-2 tw-border-teal tw-btn tw-btn-xs tw-font-normal tw-text-sm tw-text-teal ng-star-inserted')]",
            )
        ]

        # INSERT TO DATABASE
        self.insert_to_offers(
            [
                link,
                company_name,  # company_name
                None,  # company size
                position_name,  # position_name
                position_level,  # position_level
                salary_range1,
                salary_range2,
                salary_currency,
                "Brutto",
                "mies",  # salary_type  # salary_period
                contract,  # contract_type
                str(abilities),
            ]
        )

    def scrap_offers(self) -> None:
        self.__find_links()
        if len(self.links) == 0:
            print("no links to scrap")
        else:
            counter = 0
            length = len(self.links)
            for link in self.links:

                counter += 1
                print(f"Scraping {counter} of {length} - nofluffjobs")

                done = False
                tries = 1
                while not done and tries <= 3:
                    try:
                        self.__scrap_offer(link)
                        done = True
                    except:
                        print(f"Blad, ponawiam probe")
                        tries += 1

        print("nofluffjobs - done")

    # functions end
