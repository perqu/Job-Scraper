from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3, time


class NoFluffScraper:

    # Constructor
    def __init__(self, link, filename) -> None:
        self.link = link
        self.links = []
        # create self.conn, self. c
        self.connect_to_database(filename)
        # create self.driver
        self.prepare_webdriver()

    def connect_to_database(self, filename: str) -> None:
        """
        Create connection with sqlite database.

            Args:
                filename (string): a file name

            Returns: None
        """
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

        self.c.execute(
            """
                CREATE TABLE IF NOT EXISTS offers
                (
                [offer_id] INTEGER PRIMARY KEY, 
                [offer_link] TEXT UNIQUE, 
                [company_name] TEXT, 
                [company_size] TEXT,
                [position_name] TEXT, 
                [position_level] TEXT,
                [salary_range1] INTEGER,
                [salary_range2] INTEGER,
                [salary_currency] TEXT,
                [salary_type] TEXT,
                [salary_period] TEXT,
                [contract_type] TEXT,
                [abilities] TEXT
                )
                """
        )

    def prepare_webdriver(self) -> None:
        """
        Preparing webdriver to work.

            Args: None

            Returns: None
        """
        options = Options()
        options.add_argument("--window-size=%s" % "800,600")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    # functions start

    def find_links(self) -> None:
        self.driver.get(self.link)
        self.links = [
            el.get_attribute("href")
            for el in self.driver.find_elements(By.CLASS_NAME, "posting-list-item")
        ]

    def scrap_offers(self) -> None:
        if len(self.links) == 0:
            print("no links to scrap, try to use find_links() before scraping")
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

                if "." in salary:
                    salary = salary.replace(".", "")
                    salary = salary.replace("k", "00")
                else:
                    salary = salary.replace("k", "000")

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

                    salary_range1 = int(salary[:comma])
                    salary_range2 = int(salary[comma + 1 :])

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

                try:
                    self.c.execute(
                        f"""
                            INSERT INTO offers
                            (
                            offer_link,
                            company_name,
                            company_size,
                            position_name,
                            position_level,
                            salary_range1,
                            salary_range2,
                            salary_currency,
                            salary_type,
                            salary_period,
                            contract_type,
                            abilities
                            )
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
                            """,
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
                        ],
                    )
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    print("To ogloszenie jest juz w bazie danych")
                except Exception as e:
                    print("wystapil blad przy dodaniu wierwsza w bazie danych: " + e)
        print("nofluffjobs - done")

    # functions end

    # Destructor
    def __del__(self):
        self.conn.close()
