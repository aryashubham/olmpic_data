import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd


conn = sqlite3.connect("data.db")
cursor = conn.cursor()

table= """CREATE TABLE IF NOT EXISTS Players(id integer PRIMARY KEY,
        name varchar(256),
        game_name varchar(256),
        madel varchar(10),
        year varchar(256))"""

cursor.execute(table)
conn.commit()


url ="https://sportstar.thehindu.com/olympics/paris-2024/news/indian-olympic-medallists-all-medals-full-complete-list-of-athletes/article68409728.ece"

res =requests.get(url)

soup=BeautifulSoup(res.content, "html5lib")
a=soup.find_all('table', {'class':"table"})
for i in a:
    for j in i.find_all('tr')[1::]:
        cols = j.find_all('td')
        player_data= {
        'name': cols[0].text.strip(),
        "game_name": cols[3].text.strip(),
        "madel": cols[1].text.strip(),
        "year": cols[2].text.strip()
        }
        cursor.execute("""INSERT INTO Players(name, game_name, madel, year) VALUES(:name, :game_name, :madel, :year)""", player_data)
        conn.commit()

data = cursor.execute("""SELECT * FROM Players""")
data = data.fetchall()
df = pd.DataFrame(data, columns=["Index","Name", "Medal", "Edition", "Event"])
filename = "indian_olympic_medalists.csv"
df.to_csv(filename, index=False)
conn.close()


