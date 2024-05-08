# Import necessary modules
import requests
import pandas as pd
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

# Relevant district votes data (hardcoded due to time constraints)
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

# Insert API key to access ACS data
api_key = 'your_API_key_here'

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

# Plotting the comparison
plt.figure(figsize=(10, 6))

# Plotting the average voter participation ratios for the period before ward district representation
plt.plot(avg_voter_participation_before['year'], avg_voter_participation_before['votes_per_capita'], marker='o', label='Before (2006-2010)')

# Plotting the average voter participation ratios for the period after ward district representation
plt.plot(avg_voter_participation_after['year'], avg_voter_participation_after['votes_per_capita'], marker='o', label='After (2012-2020)')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Average Ratio of Voters vs Population')
plt.title('Average Voter Participation Across Congressional Districts')
plt.xticks(rotation=45)

# Adding legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
