# Imported necessary modules
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

eids = [154, 179, 192, 196, 198, 201, 205, 208, 214]

api = "https://services.austintexas.gov/election/byrecord.cfm"

pages = []

for e in eids:
    payload = {'eid':e}
    response = requests.get(api, payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    main = soup.body.main
    tables = main.findAll('table')
    summary = tables[0]
    trs = summary.findAll('tr')
    rows = {}
    for tr in trs:
        tds = tr.findAll('td')
        print(' ')
        for td in tds:
            print(td.string)
        rows[ tds[0].string ] = tds[1].string
    pages.append(rows)
    rest = tables[1:]
    
data = pd.DataFrame(pages)

print(data)

data['Percent of Registered Voters Who Voted:'] = data['Percent of Registered Voters Who Voted:'].str.rstrip('%').astype(float)
data['Year'] = pd.to_datetime(data['Date of Election:']).dt.year

data_sorted = data.sort_values(by='Year')

plt.figure(figsize=(10, 6))
plt.bar(data_sorted['Date of Election:'], data_sorted['Percent of Registered Voters Who Voted:'], color='skyblue')
plt.title('Austin City Council General Election Turnout (2006-2022)')
plt.xlabel('Date of Election')
plt.ylabel('Turnout (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
 