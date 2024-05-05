# Import necessary modules
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'

    # Construct the API request URL
    url = f"{api_url}?get=B01001_001E,NAME&for={for_clause}&in={in_clause}&key={api_key}"

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()

        # print(response.text)

        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})

        # print(district_population.index.unique())

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
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Merge population and voting data for each district
merged_data = {}

#for district, votes_data in district_votes.items():
#    print(f"Fetching data for district {district}...")
#    population_data = get_population(2019, '48', 'api_key')
#    if population_data is not None:
#        print(f"Population data for district {district} retrieved successfully.")
#        merged_data[district] = population_data.join(pd.DataFrame(votes_data, index=[0])).astype(int)
#    else:
#        print(f"Failed to retrieve population data for district {district}.")

api_key = 'your_API_key_here' # Replace code with your assigned Census API key

for year in ['2012','2014','2016','2018','2020']:
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
