from selenium.webdriver.common.by import By
import re
from scraper import Scraper


class BullDogScraper(Scraper):

    # Constructor
    def __init__(self, link, database_url) -> None:
        super().__init__(database_url)
        self.link = link

    # functions start

    def __find_in_block(self, args, block_data):
        for key in args:
            for block in block_data:
                lower = str(block).lower()
                if key in lower:
                    return block

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
            print(f"Scraping - {counter} of {length} - bulldogjobs")

            # Link
            link = block.find_element(By.TAG_NAME, "a").get_attribute("href")
            block_data = block.text.split("\n")

            for el in ["SPECIAL OFFER", "lokalizacji", "lokalizacje", "Aplikuj"]:
                for block in block_data:
                    if el in block:
                        block_data.remove(block)

            # Salary
            salary = block_data[-1].replace(" ", "")
            match = re.findall("\d+", "0 0 " + salary)
            match_currency = re.findall("[A-Z]{3}", salary)
            salary_currency = match_currency[0] if len(match_currency) > 0 else None
            salary_range1, salary_range2 = int(match[-2]), int(match[-1])

            position_name = block_data[1]
            block_data[1] = "None"

            # Position Level
            position_level = self.__find_in_block(
                ["junior", "mid", "regular", "senior", "expert"], block_data
            )

            # Contract Type
            contract_type = self.__find_in_block(
                [
                    "kontrakt b2b/umowa o pracę",
                    "umowa o pracę",
                    "kontrakt b2b",
                ],
                block_data,
            )

            if contract_type.lower() == "kontrakt b2b/umowa o pracę":
                contract_type = "B2B/Permanent"
            elif contract_type.lower() == "umowa o pracę":
                contract_type = "Permanent"
            elif contract_type.lower() == "kontrakt b2b":
                contract_type = "B2B"

            # Abilities
            abilities = block_data[5:-2]
            for el in [
                "Junior",
                "Mid",
                "Senior",
                "Kontrakt B2B/Umowa o pracę",
                "Kontrakt B2B",
                "Umowa o pracę",
            ]:
                if el in abilities:
                    abilities.remove(el)

            self.insert_to_offers(
                [
                    link,
                    block_data[0],  # company_name
                    None,  # company size
                    position_name,  # position_name
                    position_level,  # position_level
                    salary_range1,
                    salary_range2,
                    salary_currency,
                    "Brutto",
                    "mies",  # salary_type  # salary_period
                    contract_type,  # contract_type
                    str(abilities),
                ]
            )
        print("bulldogjobs - done")

    # functions end
