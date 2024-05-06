# Import necessary modules
from scipy import stats
import numpy as np
import pandas as pd
import requests 
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key, acs_type):
    if acs_type == '1-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs1'
    elif acs_type == '5-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    else:
        raise ValueError("Invalid ACS type. Please specify '1-year' or '5-year'.")

    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'

    # Construct the API request URL
    url = f"{api_url}?get=B01001_001E,NAME&for={for_clause}&in={in_clause}&key={api_key}"

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})

        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None

    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Relevant district votes data
district_votes_before = {
    '10': {'2006': 176755, '2008': 333083, '2010': 224171},
    '21': {'2006': 203782, '2008': 304350, '2010': 236545},
    '25': {'2006': 163424, '2008': 291296, '2010': 189247},
}

district_votes_after = {
    '10': {'2014': 237187, '2016': 289194, '2018': 312626, '2020': 323937},
    '21': {'2014': 264518, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2014': 240629, '2016': 293328, '2018': 320164, '2020': 330193},
}

# Merge population and voting data for each district
merged_data_before = {}
merged_data_after = {}

api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Fetch and merge data for the period from 2006 to 2012
for year in ['2006', '2008', '2010']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '1-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_before.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_before[year] = population_data

# Fetch and merge data for the period from 2014 to 2020
for year in ['2014', '2016', '2018', '2020']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '5-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_after.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_after[year] = population_data

# Concatenate data for each period
merged_before = pd.concat(merged_data_before, names=['year', 'cd'])
merged_before = merged_before.reset_index()
merged_before = merged_before.dropna()

# Convert data types to numeric
merged_before['district'] = pd.to_numeric(merged_before['district'])
merged_before['population'] = pd.to_numeric(merged_before['population'])

merged_after = pd.concat(merged_data_after, names=['year', 'cd'])
merged_after = merged_after.reset_index()
merged_after = merged_after.dropna()

# Convert data types to numeric
merged_after['district'] = pd.to_numeric(merged_after['district'])
merged_after['population'] = pd.to_numeric(merged_after['population'])

# Calculate turnout ratio for each period
merged_before['turnout_ratio'] = merged_before['district'] / merged_before['population']
merged_after['turnout_ratio'] = merged_after['district'] / merged_after['population']

# Calculate the average turnout ratio for each group before and after the treatment
avg_turnout_ratio_city_council_before = merged_before['turnout_ratio'].mean()
avg_turnout_ratio_city_council_after = merged_after['turnout_ratio'].mean()

avg_turnout_ratio_district_before = merged_before['district'].mean()
avg_turnout_ratio_district_after = merged_after['district'].mean()

# Calculate the difference in means before and after the treatment for both groups
diff_in_means_city_council = avg_turnout_ratio_city_council_after - avg_turnout_ratio_city_council_before
diff_in_means_district = avg_turnout_ratio_district_after - avg_turnout_ratio_district_before

# Perform t-tests for City Council before and after treatment
t_statistic_before_cc, p_value_before_cc = stats.ttest_ind(merged_before['turnout_ratio'], merged_after['turnout_ratio'])
t_statistic_after_cc, p_value_after_cc = stats.ttest_ind(merged_before['district'], merged_after['district'])

# Print t-test results for before and after treatment separately for City Council
print("T-test results for City Council elections:")
print(f"Before treatment - T-statistic: {t_statistic_before_cc:.4f}, p-value: {p_value_before_cc:.4f}")
print(f"After treatment - T-statistic: {t_statistic_after_cc:.4f}, p-value: {p_value_after_cc:.4f}")

# Perform t-tests for Congressional districts before and after treatment
t_statistic_before_cd, p_value_before_cd = stats.ttest_ind(merged_before['turnout_ratio'], merged_after['turnout_ratio'])
t_statistic_after_cd, p_value_after_cd = stats.ttest_ind(merged_before['district'], merged_after['district'])

# Print t-test results for before and after treatment separately for Congressional districts
print("\nT-test results for Congressional district elections:")
print(f"Before treatment - T-statistic: {t_statistic_before_cd:.4f}, p-value: {p_value_before_cd:.4f}")
print(f"After treatment - T-statistic: {t_statistic_after_cd:.4f}, p-value: {p_value_after_cd:.4f}")


#%%
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key, acs_type):
    if acs_type == '1-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs1'
    elif acs_type == '5-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    else:
        raise ValueError("Invalid ACS type. Please specify '1-year' or '5-year'.")

    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'

    # Construct the API request URL
    url = f"{api_url}?get=B01001_001E,NAME&for={for_clause}&in={in_clause}&key={api_key}"

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})

        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None

    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Relevant district votes data
district_votes_before = {
    '10': {'2006': 176755, '2008': 333083, '2010': 224171},
    '21': {'2006': 203782, '2008': 304350, '2010': 236545},
    '25': {'2006': 163424, '2008': 291296, '2010': 189247},
}

district_votes_after = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Merge population and voting data for each district for the period before ward district representation
merged_data_before = {}
merged_data_after = {}

api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Fetch and merge data for the period from 2006 to 2010
for year in ['2006', '2008', '2010']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '1-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_before.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_before[year] = population_data

# Fetch and merge data for the period from 2012 to 2020
for year in ['2012', '2014', '2016', '2018', '2020']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '5-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_after.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_after[year] = population_data

# Concatenate data for each period
merged_before = pd.concat(merged_data_before, names=['year', 'cd'])
merged_before = merged_before.reset_index()
merged_before = merged_before.dropna()

# Convert data types to numeric
merged_before['district'] = pd.to_numeric(merged_before['district'])
merged_before['population'] = pd.to_numeric(merged_before['population'])

merged_after = pd.concat(merged_data_after, names=['year', 'cd'])
merged_after = merged_after.reset_index()
merged_after = merged_after.dropna()

# Convert data types to numeric
merged_after['district'] = pd.to_numeric(merged_after['district'])
merged_after['population'] = pd.to_numeric(merged_after['population'])

# Calculate turnout ratio for each period
merged_before['votes_per_capita'] = merged_before['district'] / merged_before['population']
merged_after['votes_per_capita'] = merged_after['district'] / merged_after['population']

# Aggregate the data by year and calculate the mean
avg_voter_participation_before = merged_before.groupby('year')['votes_per_capita'].mean().reset_index()
avg_voter_participation_after = merged_after.groupby('year')['votes_per_capita'].mean().reset_index()

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

# Plotting the comparison
plt.figure(figsize=(10, 6))

# Plotting the average voter participation ratios for the period before ward district representation
plt.plot(avg_voter_participation_before['year'], avg_voter_participation_before['votes_per_capita'], marker='o', label='Texas Congressional Districts')

# Plotting the average voter participation ratios for the period after ward district representation
plt.plot(avg_voter_participation_after['year'], avg_voter_participation_after['votes_per_capita'], marker='o', label='Texas Congressional Districts (Ward Representation)')

# Plotting the ratio of ballots cast to population for Austin City Council elections
plt.bar(data_sorted['Year'], data_sorted['Ballots to Population Ratio'], color='orange', label='Austin City Council Elections')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Ratio of Voters vs Population')
plt.title('Comparison of Voter Participation Rates')
plt.xticks(rotation=45)

# Adding legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()



#%%
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key, acs_type):
    if acs_type == '1-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs1'
    elif acs_type == '5-year':
        api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    else:
        raise ValueError("Invalid ACS type. Please specify '1-year' or '5-year'.")

    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'

    # Construct the API request URL
    url = f"{api_url}?get=B01001_001E,NAME&for={for_clause}&in={in_clause}&key={api_key}"

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})

        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None

    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Relevant district votes data
district_votes_before = {
    '10': {'2006': 176755, '2008': 333083, '2010': 224171},
    '21': {'2006': 203782, '2008': 304350, '2010': 236545},
    '25': {'2006': 163424, '2008': 291296, '2010': 189247},
}

district_votes_after = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Merge population and voting data for each district for the period before ward district representation
merged_data_before = {}
merged_data_after = {}

api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Fetch and merge data for the period from 2006 to 2010
for year in ['2006', '2008', '2010']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '1-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_before.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_before[year] = population_data

# Fetch and merge data for the period from 2012 to 2020
for year in ['2012', '2014', '2016', '2018', '2020']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key, '5-year')
    print("Building district data...")
    district_data = {district: votes_data[year] for district, votes_data in district_votes_after.items()}
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data_after[year] = population_data

# Concatenate data for each period
merged_before = pd.concat(merged_data_before, names=['year', 'cd'])
merged_before = merged_before.reset_index()
merged_before = merged_before.dropna()

# Convert data types to numeric
merged_before['district'] = pd.to_numeric(merged_before['district'])
merged_before['population'] = pd.to_numeric(merged_before['population'])

merged_after = pd.concat(merged_data_after, names=['year', 'cd'])
merged_after = merged_after.reset_index()
merged_after = merged_after.dropna()

# Convert data types to numeric
merged_after['district'] = pd.to_numeric(merged_after['district'])
merged_after['population'] = pd.to_numeric(merged_after['population'])

# Calculate turnout ratio for each period
merged_before['votes_per_capita'] = merged_before['district'] / merged_before['population']
merged_after['votes_per_capita'] = merged_after['district'] / merged_after['population']

# Aggregate the data by year and calculate the mean
avg_voter_participation_before = merged_before.groupby('year')['votes_per_capita'].mean().reset_index()
avg_voter_participation_after = merged_after.groupby('year')['votes_per_capita'].mean().reset_index()

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

# Separate Austin City Council elections into before and after segments
before_austin_data = data_sorted[data_sorted['Year'] < 2014]
after_austin_data = data_sorted[data_sorted['Year'] >= 2014]

# Calculate the average voter participation ratio for Austin City Council elections before and after
avg_voter_participation_before_austin = before_austin_data['Ballots to Population Ratio'].mean()
avg_voter_participation_after_austin = after_austin_data['Ballots to Population Ratio'].mean()

# Plotting the comparison with Austin City Council elections included
plt.figure(figsize=(12, 8))

# Plotting the average voter participation ratios for the period before ward district representation
plt.plot(avg_voter_participation_before['year'], avg_voter_participation_before['votes_per_capita'], marker='o', label='Congressional Before (2006-2012)')

# Plotting the average voter participation ratios for the period after ward district representation
plt.plot(avg_voter_participation_after['year'], avg_voter_participation_after['votes_per_capita'], marker='o', label='Congressional After (2014-2020)')

# Plotting the average voter participation ratio for Austin City Council elections before and after
plt.plot(before_austin_data['Year'], before_austin_data['Ballots to Population Ratio'], marker='o', label='Austin Before (Before 2014)')
plt.plot(after_austin_data['Year'], after_austin_data['Ballots to Population Ratio'], marker='o', label='Austin After (2014-2020)')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Ratio of Voters vs Population')
plt.title('Comparison of Voter Participation Rates')
plt.xticks(rotation=45, ha='right')

# Adjusting y-axis limits
plt.ylim(0, 0.6)

# Adding legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()



#%%
# Plotting the comparison with Austin City Council elections included
plt.figure(figsize=(12, 8))

# Plotting the average voter participation ratios for the period before ward district representation
plt.plot(avg_voter_participation_before['year'], avg_voter_participation_before['votes_per_capita'], marker='o', label='Congressional Before (2006-2010)')

# Plotting the average voter participation ratios for the period after ward district representation
plt.plot(avg_voter_participation_after['year'], avg_voter_participation_after['votes_per_capita'], marker='o', label='Congressional After (2014-2020)')

# Plotting the average voter participation ratio for Austin City Council elections before and after
plt.axhline(y=avg_voter_participation_before_austin, color='green', linestyle='--', label='Austin Before (Before 2014)')
plt.axhline(y=avg_voter_participation_after_austin, color='red', linestyle='--', label='Austin After (2014-2020)')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Ratio of Voters vs Population')
plt.title('Comparison of Voter Participation Rates')
plt.xticks(rotation=45, ha='right')

# Adding legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()