# Import necessary modules
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

# Calculate average ratios for each category
avg_city_council_before = merged_before['turnout_ratio'].mean()
avg_district_before = merged_before.groupby('year')['turnout_ratio'].mean()
avg_city_council_after = merged_after['turnout_ratio'].mean()
avg_district_after = merged_after.groupby('year')['turnout_ratio'].mean()

# Plot the bar graph
plt.figure(figsize=(10, 6))

# Define x-axis values for each category
x_labels = ['City Council (2006-2012)', 'Congressional Districts (2006-2012)',
            'City Council (2014-2020)', 'Congressional Districts (2014-2020)']

# Define y-axis values (average ratios)
y_values = [avg_city_council_before.mean(), avg_district_before.mean(),
            avg_city_council_after.mean(), avg_district_after.mean()]

# Define bar width
bar_width = 0.35

# Plot bars with colors correlated to blue for city council and red for congressional districts
plt.bar(x_labels[:1], y_values[:1], color='blue', width=bar_width, label='City Council (2006-2012)')
plt.bar(x_labels[2:3], y_values[2:3], color='blue', width=bar_width, label='City Council (2014-2020)')
plt.bar(x_labels[1:2], y_values[1:2], color='red', width=bar_width, label='Congressional Districts (2006-2012)')
plt.bar(x_labels[3:], y_values[3:], color='red', width=bar_width, label='Congressional Districts (2014-2020)')

# Add legend
plt.legend()

# Add labels and title
plt.xlabel('Category')
plt.ylabel('Average Ratio of Voters vs Population')
plt.title('Average Turnout Ratios Before and After Treatment')
plt.xticks(rotation=45)

# Add legend outside the plot area
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()
