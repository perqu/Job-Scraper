import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:
    def __init__(self, database_url) -> None:
        self.conn = self.set_connection(database_url)
        self.cursor = self.set_cursor()
        self.create_table_offers()
        self.driver = self.prepare_webdriver()

    def prepare_webdriver(self):
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

    def set_connection(self, database_url):
        return psycopg2.connect(database_url)

    def set_cursor(self):
        return self.conn.cursor()

    def create_table_offers(self) -> None:
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
        pass
        # self.conn.close()
