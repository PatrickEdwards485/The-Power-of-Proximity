# Imported necessary modules
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

eids = [154, 179, 192, 196, 198, 201, 205, 208]

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

# Remove commas from 'Total Ballots Cast' and 'City Population' columns and convert to float
data['Total Ballots Cast:'] = data['Total Ballots Cast:'].str.replace(',', '').astype(float)
data['City Population (at Time of the Election):'] = data['City Population (at Time of the Election):'].str.replace(',', '').astype(float)

# Calculate ratio of 'Total Ballots Cast' to 'City Population'
data['Ballots to Population Ratio'] = data['Total Ballots Cast:'] / data['City Population (at Time of the Election):']

# Convert 'Date of Election' to datetime and extract year
data['Year'] = pd.to_datetime(data['Date of Election:']).dt.year

# Sort the data by year
data_sorted = data.sort_values(by='Year')

# Plot the ratio over the years
plt.figure(figsize=(10, 6))
plt.bar(data_sorted['Year'], data_sorted['Ballots to Population Ratio'], color='blue')
plt.title('Austin City Council Election Voter Participation Rates (2006-2020)')
plt.xlabel('Year')
plt.ylabel('Ratio of Voters vs Population')
plt.xticks(data_sorted['Year'], rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
