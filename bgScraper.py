from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sqlite3, re


class BullDogScraper:

    # Constructor
    def __init__(self, link, filename) -> None:
        self.link = link
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

    def scrap_offers(self) -> None:
        self.driver.get(self.link)
        blocks = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'p-8 lg:flex gap-6 relative bg-white mb-4 rounded-lg shadow cursor-pointer ')]",
        )
        counter = 0
        length = len(blocks)
        for block in blocks:
            counter += 1
            print(f"Scraping - {counter} of {length} done")

            link = block.find_element(By.TAG_NAME, "a").get_attribute("href")
            block_data = block.text.split("\n")
            block_data.remove("Aplikuj")
            for i in range(len(block_data)):
                if "lokalizacji" in block_data[i] or "lokalizacje" in block_data[i]:
                    del block_data[i]
                    break

            salary = block_data[-1]
            if "Up" in salary or "Do" in salary:
                salary_reversed = salary[::-1]
                salary_currency = (salary_reversed[: salary_reversed.find(" ")])[::-1]
                salary_range1 = 0
                salary_range2 = int(re.findall(r"\d+", salary)[0])

            elif "-" in salary:
                salary_reversed = salary[::-1]
                salary_currency = (salary_reversed[: salary_reversed.find(" ")])[::-1]
                salary = (salary[: -len(salary_currency) - 1]).replace(" ", "")
                comma = salary.find("-")
                salary_range1 = int(salary[:comma])
                salary_range2 = int(salary[comma + 1 :])
            else:
                salary_currency = None
                salary_range1 = None
                salary_range2 = None

            abilities = block_data[5:-2]
            if "Junior" in abilities:
                abilities.remove("Junior")
            if "Mid" in abilities:
                abilities.remove("Mid")
            if "Senior" in abilities:
                abilities.remove("Senior")
            if "B2B contract/Employment contract" in abilities:
                abilities.remove("B2B contract/Employment contract")
            if "B2B contract" in abilities:
                abilities.remove("B2B contract")
            if "Employment contract" in abilities:
                abilities.remove("Employment contract")
            if "Kontrakt B2B/Umowa o pracę" in abilities:
                abilities.remove("Kontrakt B2B/Umowa o pracę")
            if "Kontrakt B2B" in abilities:
                abilities.remove("Kontrakt B2B")
            if "Umowa o pracę" in abilities:
                abilities.remove("Umowa o pracę")

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
                        block_data[0],  # company_name
                        None,  # company size
                        block_data[1],  # position_name
                        block_data[3],  # position_level
                        salary_range1,
                        salary_range2,
                        salary_currency,
                        "Brutto",
                        "mies",  # salary_type  # salary_period
                        block_data[4],  # contract_type
                        str(abilities),
                    ],
                )
                self.conn.commit()
            except sqlite3.IntegrityError:
                print("To ogloszenie jest juz w bazie danych")
            except Exception as e:
                print("wystapil blad przy dodaniu wierwsza w bazie danych: " + e)
        print("bulldogjobs - done")

    # functions end

    # Destructor
    def __del__(self):
        self.conn.close()
