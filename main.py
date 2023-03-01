from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re, time, sqlite3

conn = sqlite3.connect('test_database.db') 
c = conn.cursor()

c.execute('''
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
          ''')

options = Options()
#options.add_argument("--headless")
options.add_argument("--window-size=%s" % "800,600")
    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://justjoin.it/remote?q=python%20developer@keyword&tab=with-salary&sort=salary')

links = []
it = 0
founded = False
while not founded:
    driver.execute_script(f"document.getElementsByClassName('css-ic7v2w')[0].scroll(0, {it*550})")
    html = driver.page_source
    gen = (m.start()+6 for m in re.finditer('''href="/offers/''', html))
    links.extend(['https://justjoin.it' + html[el:(html[el:].find('\"')+el)] for el in gen])
    time.sleep(0.5)
    try:
        driver.find_element(By.CLASS_NAME, 'css-1w7o08v')
        founded = True
    except:
        founded = False
    it += 1
links = list(set(links))

for link in links:
    driver.get(link)
    time.sleep(2)
    company_name = driver.find_element(By.CLASS_NAME, 'css-l4opor').text
    company_size, position_level, _ = [element.text for element in driver.find_elements(By.CLASS_NAME, 'css-1ji7bvd')]
    position_name = driver.find_element(By.CLASS_NAME, 'css-1id4k1').text
    
    #salary
    salary = (driver.find_element(By.CLASS_NAME, 'css-a2pcn2').text).strip()
    salary_reversed = salary[::-1]
    salary_currency = (salary_reversed[:salary_reversed.find(' ')])[::-1]
    salary = (salary[:-len(salary_currency)-1]).replace(' ', '')
    comma = salary.find('-')
    salary_range1 = int(salary[:comma])
    salary_range2 = int(salary[comma+1:])
    
    text = (driver.find_element(By.CLASS_NAME, 'css-rmoont').text).strip()
    slash = text.find('/')
    salary_type = text[:slash]
    salary_period = text[slash+1:]

    text = driver.find_element(By.CLASS_NAME, 'css-qy8eaj').text
    contract_type = text.replace(' ', '').replace('-', '')

    #abilities
    abilities_text = driver.find_elements(By.CLASS_NAME, 'css-1q98d5e')
    abilities = str([ability.text.split('\n') for ability in abilities_text])
    try:
        c.execute(f'''
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
            VALUES
            (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
            );
            ''', 
                    [link, 
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
                    abilities])
        conn.commit()
    except sqlite3.IntegrityError:
        print('To ogloszenie jest juz w bazie danych')
conn.close()