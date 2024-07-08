import pandas as pd

url = "https://en.wikipedia.org/wiki/Periodic_table"

#reading all the tables in the html 
tables = pd.read_html(url)

# print(len(tables))--> there are 29 tables in that wikipedia page 

target_data=tables[1]
pd.set_option('display.max_columns',35)
pd.set_option('display.max_rows',35)
print(target_data)

target_data.to_csv('Periodic Data.csv',index=False, encoding='utf-8')