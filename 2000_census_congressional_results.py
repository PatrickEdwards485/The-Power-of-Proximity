# Import necessary modules
import requests
import config
import pandas as pd
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/acs/acs1'
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
district_votes = {
    '10': {'2006': 176755, '2008': 333083, '2010': 224171},
    '21': {'2006': 203782, '2008': 304350, '2010': 236545},
    '25': {'2006': 163424, '2008': 291296, '2010': 189247},
}

# Merge population and voting data for each district
merged_data = {}

api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

for year in ['2006','2008','2010']:
    print(f"Fetching Census data for year {year}...")
    population_data = get_population(year, '48', api_key)
    print("Building district data...")
    district_data = { district: votes_data[year] for district, votes_data in district_votes.items() }
    district_data = pd.Series(district_data)
    population_data['district'] = district_data
    merged_data[year] = population_data

merged = pd.concat(merged_data,names=['year','cd'])
merged = merged.reset_index()
merged = merged.dropna()

# Iterate over each congressional district
for district, data in merged.groupby('cd'):
    # Convert 'district' and 'population' columns to numeric, replacing non-numeric values with NaN
    data['district'] = pd.to_numeric(data['district'], errors='coerce')
    data['population'] = pd.to_numeric(data['population'], errors='coerce')

    # Drop rows with NaN values after conversion
    data = data.dropna()
    
    # Calculate votes per capita
    data['votes_per_capita'] = data['district'] / data['population']

    # Convert votes per capita to percentage
    data['votes_percentage'] = data['votes_per_capita'] * 100

    # Create a new figure and axis for each district
    fig, ax = plt.subplots()

    # Plot a bar graph for the current district
    ax.bar(data['year'], data['district'] / data['population'], color='red')

    # Set the title and labels
    ax.set_title(f'Voter Participation Rates for District {district}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Ratio of Voters vs Population')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()
