import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("sqlite.db")
df = pd.read_sql_query("SELECT * from offers", con)

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

for key, value in sort_dictionary.items():
    print(f"{key} - {value}")
