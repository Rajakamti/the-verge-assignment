import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

import pandas as pd
import re
from datetime import datetime 

news_url="https://www.theverge.com/rss/index.xml"
Client=urlopen(news_url)
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("entry")


final_data = pd.DataFrame()

Headline = []
Link = []
Date = []
Author_list = []


for news in news_list:
  try:
    Headline.append("".join(news.title.text))
  except:
    Headline.append(" ")
    
  try:
    Link.append("".join(news.id.text))
  except:
    Link.append(" ")
    
  try:
    Date.append("".join(news.published.text))
    Date = [d[:10].strip() for d in Date]
      
    
  except:
    Date.append(" ")
    
  try:
    Author_list.append("".join(news.author.text))
    Author = [s.strip('\n') for s in Author_list]
    
    
  except:
    Author.append(" ")
    break


  
#print(Headline)
#print(Link)
#print(Date)
#print(Author)


data = []
data = pd.DataFrame({"url":Link,
                             "headline":Headline,
                             "author":Author,
                             "date":Date})
final_data = final_data.append(data)
final_data.index.name = 'id'
date = datetime.now().strftime("%d_%m_%Y")

file_name = f"{date}_Verge.csv"
final_data.to_csv(file_name)

#Create a database on sqlite3


import sqlite3




df = pd.read_csv(file_name)
print(df.columns)

conn = sqlite3.connect('Verge_News.db')
cursor = conn.cursor()

#creating table
cursor.execute('''
              CREATE TABLE IF NOT EXISTS The_Verge (
                         id int primary key,
                         url varchar(500),
                         headline varchar(500),
                         author varchar(100),
                         date varchar(50))
               ''')
#inserting values
for row in df.itertuples():
               cursor.execute('INSERT OR REPLACE INTO The_Verge VALUES(?, ?, ?, ?, ?)',(row.id, row.url, row.headline, row.author, row.date))
               conn.commit()
               
#printing the sql table
read = pd.read_sql('''SELECT * FROM The_Verge''', conn)
print(read)







               

