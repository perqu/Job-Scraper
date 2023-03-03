from jjScraper import JustJoinScraper
from bgScraper import BullDogScraper
from nfScraper import NoFluffScraper


bg = BullDogScraper(
    "https://bulldogjob.pl/companies/jobs/s/skills,Python/withSalary,true/experienceLevel,medium,senior/city,Remote"
)
bg.scrap_offers()
del bg

nf = NoFluffScraper(
    "https://nofluffjobs.com/pl/praca-zdalna/backend?page=1&criteria=requirement%3DPython%20%20seniority%3Dmid,senior,expert"
)
nf.find_links()
nf.scrap_offers()
del nf

jj = JustJoinScraper("https://justjoin.it/remote/python?tab=with-salary&sort=salary")
jj.find_links()
jj.scrap_offers()
del jj
