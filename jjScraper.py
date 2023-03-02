from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re, time, sqlite3


class JustJoinScraper:

    # Constructor
    def __init__(self, link) -> None:
        self.link = link
        self.links = []
        # create self.conn, self. c
        self.connect_to_database("sqlite.db")
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
                CREATE TABLE IF NOT EXISTS just_join_it_offers
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
        it = 0
        foundedEnd = False

        while not foundedEnd:
            # Slow down to human speed :)
            time.sleep(0.5)

            # Scroll down to next offers
            self.driver.execute_script(
                f"document.getElementsByClassName('css-ic7v2w')[0].scroll(0, {it*550})"
            )
            html = self.driver.page_source

            new_links = []
            for founded in re.finditer("""href="/offers/""", html):
                position = founded.start() + 6
                prefix = "https://justjoin.it"
                position_end = html[position:].find('"') + position
                new_link = prefix + html[position:position_end]
                new_links.append(new_link)

            # last loop as one-liner
            # new_links = ['https://justjoin.it' + html[founded.start()+6:(html[founded.start()+6:].find('\"')+founded.start()+6)] for founded in re.finditer('''href="/offers/''', html)]
            self.links.extend(new_links)

            try:
                self.driver.find_element(By.CLASS_NAME, "css-1w7o08v")
                foundedEnd = True
            except selenium.common.exceptions.NoSuchElementException:
                foundedEnd = False

            it += 1

        self.links = list(set(self.links))

    def scrap_offers(self) -> None:
        if len(self.links) == 0:
            print("no links to scrap, try to use find_links() before scraping")
        else:
            for link in self.links:
                self.driver.get(link)
                time.sleep(0.5)
                company_name = self.driver.find_element(
                    By.CLASS_NAME, "css-l4opor"
                ).text
                # there are three elements of class: css-1ji7bvd. Only first two are in our interest.
                company_size, position_level, _ = [
                    element.text
                    for element in self.driver.find_elements(
                        By.CLASS_NAME, "css-1ji7bvd"
                    )
                ]
                position_name = self.driver.find_element(
                    By.CLASS_NAME, "css-1id4k1"
                ).text

                # salary
                salary = (
                    self.driver.find_element(By.CLASS_NAME, "css-a2pcn2").text
                ).strip()
                salary_reversed = salary[::-1]
                salary_currency = (salary_reversed[: salary_reversed.find(" ")])[::-1]
                salary = (salary[: -len(salary_currency) - 1]).replace(" ", "")
                comma = salary.find("-")
                salary_range1 = int(salary[:comma])
                salary_range2 = int(salary[comma + 1 :])

                text = (
                    self.driver.find_element(By.CLASS_NAME, "css-rmoont").text
                ).strip()
                slash = text.find("/")
                salary_type = text[:slash]
                salary_period = text[slash + 1 :]

                text = self.driver.find_element(By.CLASS_NAME, "css-qy8eaj").text
                contract_type = text.replace(" ", "").replace("-", "")

                # abilities
                abilities_text = self.driver.find_elements(By.CLASS_NAME, "css-1q98d5e")
                abilities = str(
                    [ability.text.split("\n") for ability in abilities_text]
                )
                try:
                    self.c.execute(
                        f"""
                        INSERT INTO just_join_it_offers
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
                            abilities,
                        ],
                    )
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    print("To ogloszenie jest juz w bazie danych")
                except Exception as e:
                    print("wystapil blad przy dodaniu wierwsza w bazie danych: " + e)

    # functions end

    # Destructor
    def __del__(self):
        self.conn.close()


jj = JustJoinScraper(
    link="""https://justjoin.it/remote?q=python%20developer@keyword&tab=with-salary&sort=salary"""
)

jj.find_links()
jj.scrap_offers()
