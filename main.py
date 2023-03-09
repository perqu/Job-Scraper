from jjScraper import JustJoinScraper
from bgScraper import BullDogScraper
from nfScraper import NoFluffScraper
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ["DATABASE_URL"]

bg = BullDogScraper(
    "https://bulldogjob.pl/companies/jobs/s/skills,Python/withSalary,true/experienceLevel,medium,senior/city,Remote",
    database_url,
)
bg.scrap_offers()

nf = NoFluffScraper(
    "https://nofluffjobs.com/pl/praca-zdalna/backend?page=1&criteria=requirement%3DPython%20%20seniority%3Dmid,senior,expert",
    database_url,
)
nf.scrap_offers()

jj = JustJoinScraper(
    "https://justjoin.it/remote/python?tab=with-salary&sort=salary", database_url
)
jj.scrap_offers()
