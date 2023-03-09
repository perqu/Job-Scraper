import selenium.common.exceptions
from selenium.webdriver.common.by import By
from scraper import Scraper


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

                if salary == None:
                    salary_currency = None
                    salary_range1 = None
                    salary_range2 = None
                else:
                    salary_reversed = salary[::-1]
                    salary_currency = (salary_reversed[: salary_reversed.find(" ")])[
                        ::-1
                    ]
                    salary = (salary[: -len(salary_currency) - 1]).replace(" ", "")
                    comma = salary.find("–")
                    if comma == -1:
                        comma = salary.find("-")
                    if comma == -1:
                        comma = salary.find("-")

                    salary_range1 = salary[:comma]
                    if "." in salary:
                        salary_range1 = salary_range1.replace(".", "")
                        salary_range1 = salary_range1.replace("k", "00")
                    else:
                        salary_range1 = salary_range1.replace("k", "000")
                    salary_range2 = salary[comma + 1 :]
                    if "." in salary:
                        salary_range2 = salary_range2.replace(".", "")
                        salary_range2 = salary_range2.replace("k", "00")
                    else:
                        salary_range2 = salary_range2.replace("k", "000")

                # Contract
                try:
                    text_contract = self.driver.find_element(
                        By.XPATH,
                        "//div[contains(@class, 'paragraph tw-text-xs lg:tw-text-sm tw-flex tw-items-center tw-flex-wrap type tw-relative')]",
                    ).text
                    contract = ("UoP" if "brutto" in text_contract else "B2B",)
                except selenium.common.exceptions.NoSuchElementException:
                    contract = "UoP/B2B"

                # Abilities

                abilities = [
                    el.text
                    for el in self.driver.find_elements(
                        By.XPATH,
                        "//span[contains(@class, 'no-cursor text-truncate tw-border-2 tw-border-teal tw-btn tw-btn-xs tw-font-normal tw-text-sm tw-text-teal ng-star-inserted')]",
                    )
                ]

                # INSERT TO DATABASE
                super().insert_to_offers(
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

        print("nofluffjobs - done")

    # functions end
