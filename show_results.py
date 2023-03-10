import pandas as pd
import matplotlib.pyplot as plt

"""
# Version with postgresql
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ["DATABASE_URL"]
connection = psycopg2.connect(database_url)
# END Version with postgresql
"""

# Version with sqlite
import sqlite3

database_url = "sqlite.db"
connection = sqlite3.connect(database_url)
# END Version with sqlite

# from what number of occurrences should be drawn on the graph
number = 10


df = pd.read_sql_query("SELECT * from offers", connection)

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
    if value < number:
        keys_to_delete.append(key)

for key in keys_to_delete:
    del sort_dictionary[key]

names = list(sort_dictionary.keys())
values = list(sort_dictionary.values())

plt.bar(range(len(sort_dictionary)), values, tick_label=names)
plt.show()
