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
                salary_range2 = int(re.findall(r"\d+", salary.replace(" ", ""))[0])

            elif "-" in salary:
                salary_reversed = salary[::-1]
                salary_currency = (salary_reversed[: salary_reversed.find(" ")])[::-1]
                salary = (salary[: -len(salary_currency) - 1]).replace(" ", "")
                comma = salary.find("-")
                salary_range1 = int(salary[:comma])
                salary_range2 = int(salary[comma + 1 :])
            else:
                salary_currency = None
                salary_range1 = -1
                salary_range2 = -1

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

            # position level

            position_level = self.find_in_block(
                ["junior", "mid", "regular", "senior", "expert"], block_data
            )

            contract_type = self.find_in_block(
                [
                    "kontrakt b2b/umowa o pracę",
                    "umowa o pracę",
                    "kontrakt b2b",
                    "employment contract",
                    "b2b contract",
                    "b2b contract/employment contract",
                ],
                block_data,
            )
            super().insert_to_offers(
                [
                    link,
                    block_data[0],  # company_name
                    None,  # company size
                    block_data[1],  # position_name
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
