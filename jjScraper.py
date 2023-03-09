import selenium.common.exceptions
from selenium.webdriver.common.by import By
import re
from scraper import Scraper


class JustJoinScraper(Scraper):

    # Constructor
    def __init__(self, link, database_url) -> None:
        super().__init__(database_url)
        self.link = link
        self.links = []

    # functions start

    def __find_links(self) -> None:
        self.driver.get(self.link)
        it = 0
        foundedEnd = False

        while not foundedEnd:
            done = False
            while not done:
                try:
                    self.driver.execute_script(
                        f"document.getElementsByClassName('css-ic7v2w')[0].scroll(0, {it*550})"
                    )
                    done = True
                except:
                    pass
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

    def __scrap_offer(self, link):
        self.driver.get(link)

        company_name = self.driver.find_element(By.CLASS_NAME, "css-l4opor").text
        # there are three elements of class: css-1ji7bvd. Only first two are in our interest.
        company_size, position_level, _ = [
            element.text
            for element in self.driver.find_elements(By.CLASS_NAME, "css-1ji7bvd")
        ]
        position_name = self.driver.find_element(By.CLASS_NAME, "css-1id4k1").text

        # salary
        salary = (self.driver.find_element(By.CLASS_NAME, "css-a2pcn2").text).replace(
            " ", ""
        )
        match = re.findall("\d+", "0 0 " + salary)
        match_currency = re.findall("[A-Z]{3}", salary)
        salary_currency = match_currency[0] if len(match_currency) > 0 else None
        salary_range1, salary_range2 = int(match[-2]), int(match[-1])

        # Type and period of salary
        text = (self.driver.find_element(By.CLASS_NAME, "css-rmoont").text).strip()
        slash = text.find("/")
        salary_type = text[:slash]
        salary_period = "mies" if text[slash + 1 :] == "month" else text[slash + 1 :]

        # Contract Type
        text = self.driver.find_element(By.CLASS_NAME, "css-qy8eaj").text
        contract_type = text.replace(" ", "").replace("-", "")

        # abilities
        abilities_text = self.driver.find_elements(By.CLASS_NAME, "css-1q98d5e")
        abilities = str([ability.text.split("\n")[0] for ability in abilities_text])

        self.insert_to_offers(
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
                print(f"Scraping - {counter} of {length} - justjoinit")

                done = False
                tries = 1
                while not done and tries <= 3:
                    try:
                        self.__scrap_offer(link)
                        done = True
                    except:
                        print(f"Blad, ponawiam probe")
                        tries += 1

        print("justjoinit - done")

    # functions end
