import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ["DATABASE_URL"]

# Read sqlite query results into a pandas DataFrame
connection = psycopg2.connect(database_url)
df = pd.read_sql_query("SELECT * from offers", connection)

# Verify that result of SQL query is stored in the dataframe
lista = []
for el in df["abilities"]:
    el = el[1:-1]
    el = el.replace("'", "")
    el = el.replace('"', "")
    el = el.replace("(", "")
    el = el.replace(")", "")

    lista.extend([el.lower() for el in el.split(", ")])

wyniki = {}
for el in lista:
    if el in wyniki:
        wyniki[el] += 1
    else:
        wyniki[el] = 1
"""
for el in ["3.x", "in", "3", "i", "/", "or"]:
    if el in wyniki:
        del wyniki[el]
"""

sort_dictionary = dict(sorted(wyniki.items(), key=lambda item: item[1], reverse=True))

keys_to_delete = []

for key, value in sort_dictionary.items():
    if value < 10:
        keys_to_delete.append(key)

for key in keys_to_delete:
    del sort_dictionary[key]

names = list(sort_dictionary.keys())
values = list(sort_dictionary.values())

plt.bar(range(len(sort_dictionary)), values, tick_label=names)
plt.show()
