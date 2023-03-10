from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

'''
# Version with postgresql
import psycopg2


class Scraper:
    def __init__(self, database_url) -> None:
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor()
        self.__create_table_offers()
        self.driver = self.__prepare_webdriver()

    def __prepare_webdriver(self):
        """
        Preparing webdriver to work.

            Args: None

            Returns: None
        """
        options = Options()
        options.add_argument("--window-size=%s" % "800,600")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def __create_table_offers(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS offers
            (
            offer_id SERIAL PRIMARY KEY, 
            offer_link TEXT UNIQUE, 
            company_name TEXT, 
            company_size TEXT,
            position_name TEXT, 
            position_level TEXT,
            salary_range1 INTEGER,
            salary_range2 INTEGER,
            salary_currency TEXT,
            salary_type TEXT,
            salary_period TEXT,
            contract_type TEXT,
            abilities TEXT
            )
            """
        )

    def insert_to_offers(self, args: list) -> None:
        try:
            self.cursor.execute(
                """
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
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                args,
            )
        except Exception as e:
            print(e)
        self.conn.commit()

    # Destructor
    def __del__(self):
        self.conn.close()


# END Version with postgresql
'''


# Version with sqlite
import sqlite3


class Scraper:
    def __init__(self, database_url) -> None:
        self.conn = sqlite3.connect(database_url)
        self.cursor = self.conn.cursor()
        self.__create_table_offers()
        self.driver = self.__prepare_webdriver()

    def __prepare_webdriver(self):
        """
        Preparing webdriver to work.

            Args: None

            Returns: None
        """
        options = Options()
        options.add_argument("--window-size=%s" % "800,600")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def __create_table_offers(self) -> None:
        self.cursor.execute(
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

    def insert_to_offers(self, args: list) -> None:
        try:
            self.cursor.execute(
                """
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
                args,
            )
        except Exception as e:
            print(e)
        self.conn.commit()

    # Destructor
    def __del__(self):
        self.conn.close()


# END Version with sqlite
