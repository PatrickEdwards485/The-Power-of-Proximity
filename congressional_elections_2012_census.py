import pandas as pd
import matplotlib.pyplot as plt

# Read the 2012 Excel file
file_path_2012 = "2012congresults.xls"
df_2012 = pd.read_excel(file_path_2012, sheet_name='2012 US House & Senate Results')

# Read the 2014 Excel file
file_path_2014 = "results14.xls"
df_2014 = pd.read_excel(file_path_2014, sheet_name='2014 US House Results by State')

# Read the 2016 Excel file
file_path_2016 = "federalelections2016.xlsx"
df_2016 = pd.read_excel(file_path_2016, sheet_name='2016 US House Results by State')

# Read the 2018 Excel file
file_path_2018 = "federalelections2018.xlsx"
df_2018 = pd.read_excel(file_path_2018, sheet_name='2018 US House Results by State')

# Read the 2020 Excel file
file_path_2020 = "federalelections2020.xlsx"
df_2020 = pd.read_excel(file_path_2020, sheet_name='13. US House Results by State')

# Create a dictionary to store the "District Votes:" totals for each district in each year
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate the maximum vote total across all districts and years
max_vote_total = max(max(district.values()) for district in district_votes.values())

# Plot bar graphs for each district
for district in ['10', '17', '21', '25', '31']:
    plt.figure(figsize=(8, 6))
    
    # Calculate maximum vote totals for the current district
    max_votes_2012 = district_votes[district]['2012']
    max_votes_2014 = district_votes[district]['2014']
    max_votes_2016 = district_votes[district]['2016']
    max_votes_2018 = district_votes[district]['2018']
    max_votes_2020 = district_votes[district]['2020']
    
    # Plot for 2012
    plt.bar('2012', max_votes_2012, color='red', label='2012')
    
    # Plot for 2014
    plt.bar('2014', max_votes_2014, color='red', label='2014')
    
    # Plot for 2016
    plt.bar('2016', max_votes_2016, color='red', label='2016')
    
    # Plot for 2018
    plt.bar('2018', max_votes_2018, color='red', label='2018')
    
    # Plot for 2020
    plt.bar('2020', max_votes_2020, color='red', label='2020')
    
    plt.xlabel('Year')
    plt.ylabel('Vote Totals')
    plt.title(f'Vote Totals for District {district} (2012-2020 Elections)')
    plt.legend()
    plt.ylim(0, max_vote_total * 1.1)
    plt.show()
    
    
#%%
from census import Census
from us import states
import matplotlib.pyplot as plt

# Set up Census API connection with your API key
c = Census("397e2c2610f07f1b5c63d726a8d2d6959274f01d")

# Function to retrieve population data for a given year and state
def get_population(year, state):
    # Specify the variables you want to retrieve from the API
    variables = ("NAME", "B01003_001E")  # NAME is the district name, B01003_001E is total population
    
    # Query the API for population data
    population_data = c.acs5.state_district(variables, state, year)
    
    return population_data

# Function to calculate residual population (Total Population - District Votes)
def calculate_residual_population(population, district_votes, year):
    residual_population = {}
    for district, data in population.items():
        total_population = data["B01003_001E"]
        votes = district_votes[district][str(year)]  # Access vote total for the current year
        residual_population[district] = total_population - votes
    return residual_population

# Example usage
state = states.TX.fips  # Texas FIPS code
years = [2012, 2014, 2016, 2018, 2020]

# Retrieve population data for each year
population_by_year = {}
for year in years:
    population_by_year[year] = get_population(year, state)

# Example district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate residual population for each year
residual_population_by_year = {}
for year, population in population_by_year.items():
    residual_population_by_year[year] = calculate_residual_population(population, district_votes, year)

# Create stacked bar graphs for each district in each year
for year in years:
    plt.figure(figsize=(10, 6))
    
    # Get population and residual population data for the current year
    population_data = [population["B01003_001E"] for population in population_by_year[year].values()]
    residual_population_data = [residual_population_by_year[year][district] for district in district_votes.keys()]
    
    # Create stacked bar graph
    districts = list(district_votes.keys())
    plt.bar(districts, population_data, label='Total Population')
    plt.bar(districts, residual_population_data, bottom=population_data, label='Residual Population')
    
    plt.xlabel('District')
    plt.ylabel('Population')
    plt.title(f'Population vs. Residual Population by District for {year}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    
    
#%%
import requests
import re
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    for_clause = 'congressional district:*'
    in_clause = 'state:48'
    key_value = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'
    
    # Construct the API request URL
    url = f"{api_url}?get=NAME,B01003_001E&for={for_clause}&in={in_clause}&key={key_value}"
    
    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        
        # Bebugging print to inspect the data structure
        print("API response:", data)
        
        # Extract district names and population data
        district_population = {}
        for row in data[1:]:
            district_name = row[0]
            population = int(row[1])
            district = district_name.split(',')[0].split(' ')[-1]
            district_population[district] = population
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Function to extract district number from district name
def extract_district_number(name):
    """
    Extracts the district number from the congressional district name.
    """
    match = re.search(r'(\d+)', name)
    if match:
        return match.group(1)
    else:
        return None

state_code = '48'  # Texas state code
years = [2012, 2014, 2016, 2018, 2020]
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Retrieve population data for each year
population_by_year = {}
for year in years:
    population_by_year[year] = get_population(year, state_code, api_key)

# Example district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate residual population for each year
residual_population_by_year = {}
for year, population in population_by_year.items():
    if population:
        residual_population_by_year[year] = {district: population[district] - district_votes.get(district, {}).get(str(year), 0) for district in population}
    else:
        print(f"No population data available for {year}")

# Create stacked bar graphs for each district in each year
for year in years:
    plt.figure(figsize=(10, 6))
    
    if year in residual_population_by_year:
        # Get population and residual population data for the current year
        population_data = [population for population in population_by_year[year].values()]
        residual_population_data = [residual_population_by_year[year][district] for district in population_by_year[year].keys()]
        
        # Create stacked bar graph
        districts = list(population_by_year[year].keys())
        plt.bar(districts, population_data, label='Total Population')
        plt.bar(districts, residual_population_data, bottom=population_data, label='Residual Population')
        
        plt.xlabel('District')
        plt.ylabel('Population')
        plt.title(f'Population vs. Residual Population by District for {year}')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No residual population data available for {year}")
        
        
#%%
import requests
import re
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    for_clause = 'congressional district:*'
    in_clause = 'state:48'
    key_value = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'
    
    # Construct the API request URL
    url = f"https://api.census.gov/data/2010/dec/sf1?get=P001001&for=congressional%20district:*&in=state:48&key=397e2c2610f07f1b5c63d726a8d2d6959274f01d"

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        
        # Bebugging print to inspect the data structure
        print("API response:", data)
        
        # Extract district names and population data
        district_population = {}
        for row in data[1:]:
            district_name = row[0]
            population = int(row[1])
            district = district_name.split(',')[0].split(' ')[-1]
            district_population[district] = population
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Function to extract district number from district name
def extract_district_number(name):
    """
    Extracts the district number from the congressional district name.
    """
    match = re.search(r'(\d+)', name)
    if match:
        return match.group(1)
    else:
        return None

state_code = '48'  # Texas state code
years = [2012, 2014, 2016, 2018, 2020]
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Retrieve population data for each year
population_by_year = {}
for year in years:
    population_by_year[year] = get_population(year, state_code, api_key)

# Example district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate residual population for each year
residual_population_by_year = {}
for year, population in population_by_year.items():
    if population:
        residual_population_by_year[year] = {district: population[district] - district_votes.get(district, {}).get(str(year), 0) for district in population}
    else:
        print(f"No population data available for {year}")

# Function to create stacked bar graphs
def create_stacked_bar_graph(district, year, population, district_votes_data):
    plt.figure(figsize=(8, 6))
    
    # Get population and district votes data for the current year and district
    population_value = population
    district_votes_value = district_votes_data.get(str(year), 0)
    
    # Create stacked bar graph
    plt.bar(year, population_value, label='Total Population')
    plt.bar(year, district_votes_value, bottom=population_value, label='District Votes')
    
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title(f'Population vs. District Votes for District {district}')
    plt.legend()
    plt.xticks([year])
    plt.tight_layout()
    plt.show()

# Create stacked bar graphs for each district in each year
for district in district_votes.keys():
    for year in years:
        if year in population_by_year and year in residual_population_by_year and district in population_by_year[year]:
            population_data = population_by_year[year][district]
            district_votes_data = district_votes.get(district, {})
            create_stacked_bar_graph(district, year, population_data, district_votes_data)
        else:
            print(f"No data available for District {district} in {year}")


#%%
import requests

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/dec/sf1'
    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'
    
    # Construct the API request URL
    url = f"{api_url}?get=H001001,NAME&for={for_clause}&in={in_clause}&key={api_key}"
    
    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        
        # Bebugging print to inspect the data structure
        print("API response:", data)
        
        # Extract district names and population data
        district_population = {}
        for row in data[1:]:
            district_name = row[1]
            population = int(row[0])
            district = district_name.split(',')[0].split(' ')[-1]
            district_population[district] = population
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

state_code = '48'  # Texas state code
year = 2010  # 2010 Census
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'  # Replace 'YOUR_API_KEY' with your actual API key

# Retrieve population data for the 2010 Census
population_2010 = get_population(year, state_code, api_key)
print("Population data for 2010 Census:", population_2010)



#%%
# CORRECTLY FORMATTED STACKED BAR GRAPH
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/dec/sf1'
    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'
    
    # Construct the API request URL
    url = f"{api_url}?get=H001001,NAME&for={for_clause}&in={in_clause}&key={api_key}"
    
    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        
        # Debugging print to inspect the data structure
        print("API response:", data)
        
        # Extract district names and population data
        district_population = {}
        for row in data[1:]:
            population = int(row[0])
            district_name = row[1]
            # Extract the district number from the district name
            district_number = district_name.split('District ')[-1].split(' ')[0]
            district_population[district_number] = population
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None

# Function to calculate total population for each district across the years
def calculate_total_population(population_data):
    total_population = {}
    for year_data in population_data.values():
        for district, population in year_data.items():
            if district not in total_population:
                total_population[district] = 0
            total_population[district] += population
    return total_population

# Retrieve population data for the 2010 Census
state_code = '48'  # Texas state code
year = 2010  # 2010 Census
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'  # Replace 'YOUR_API_KEY' with your actual API key
population_2010 = get_population(year, state_code, api_key)

# Example district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate total population for each district across the years
total_population = calculate_total_population({'2010': population_2010})

# Plot stacked bar graphs for each district
for district in district_votes.keys():
    years = list(district_votes[district].keys())
    district_population = [population_2010[district]] * len(years)
    district_votes_data = [district_votes[district][year] for year in years]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, district_population, label='Total Population')
    plt.bar(years, district_votes_data, bottom=district_population, label='District Votes')
    
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title(f'Stacked Bar Graph for District {district}')
    plt.legend()
    plt.show()
    
    
#%%
import requests
import pandas as pd
import matplotlib.pyplot as plt 
#%%
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
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})
        
        
        # # Extract district names and population data
        # district_population = {}
        # for row in data[1:]:
        #     district_name = row[1]
        #     population = int(row[0])
        #     district = district_name.split(',')[0].split(' ')[-1]
        #     district_population[district] = population
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None
#%%
# Function to calculate total population for each district across the years
# def calculate_total_population(population_data):
#     total_population = {}
#     for year_data in population_data.values():
#         for district, population in year_data.items():
#             if district not in total_population:
#                 total_population[district] = 0
#             total_population[district] += population
#     return total_population

# # Retrieve population data for the 2010 Census
# state_code = '48'  # Texas state code
# year = 2010  # 2010 Census
# api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'  # Replace 'YOUR_API_KEY' with your actual API key
# population_2010 = get_population(year, state_code, api_key)
# print("Population data for 2010 Census:", population_2010)

# Example district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Function to calculate district votes by subtracting residual population from total population
def calculate_district_votes(population_data, district_votes_data):
    district_votes_calculated = {}
    for district, votes in district_votes_data.items():
        if district in population_data:
            district_population = population_data[district]
            district_votes_calculated[district] = {year: district_population - votes[year] for year in votes.keys()}
        else:
            print(f"No population data available for District {district}")
    return district_votes_calculated

# Calculate total population for each district across the years
total_population = calculate_total_population({'2010': population_2010})
print("Total population:", total_population)

# Calculate district votes by subtracting residual population from total population
district_votes_calculated = calculate_district_votes(population_2010, district_votes)
print("District votes (calculated):", district_votes_calculated)

# Plot stacked bar graphs for each district
for district in district_votes.keys():
    if district not in population_2010 or district not in district_votes_calculated:
        print(f"No population data available for District {district}")
        continue
    
    years = list(district_votes[district].keys())
    district_population = [population_2010[district]] * len(years)
    district_votes_data = [district_votes_calculated[district][year] for year in years]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, district_population, label='Total Population')
    plt.bar(years, district_votes_data, bottom=district_population, label='District Votes')
    
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title(f'Stacked Bar Graph for District {district}')
    plt.legend()
    plt.show()



#%%
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
    
    print("API URL:", url)

    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})

        print("Population Data:", district_population)
        
        return district_population
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"Error fetching data: {e}")
        print(f"Response content: {response.content}")
        return None
    
    except ValueError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None
    
    
# Call the function to retrieve population data
district_population = get_population(2019, "TX", "397e2c2610f07f1b5c63d726a8d2d6959274f01d")

# Check if district_population is None
if district_population is None:
    print("Failed to retrieve population data. Exiting...")
    exit()

# Call the function to plot vote percentage for each district
plot_vote_percentage(district_votes, district_population)
#%%
# Relevant district votes data
district_votes = {
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# TRYING SOMETHING NEW

def plot_vote_percentage(district_votes, district_population):
    for district, votes_data in district_votes.items():
        votes_percentage = {}
        for year, votes in votes_data.items():
            population = district_population.loc[district, "population"]
            percentage = (votes / population) * 100
            votes_percentage[year] = percentage
        years = list(votes_percentage.keys())
        percentages = list(votes_percentage.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(years, percentages, color='red')
        plt.xlabel('Year')
        plt.ylabel('Percentage of Votes Compared to Population')
        plt.title(f'District {district} Vote Percentage Over Years')
        plt.xticks(years)
        plt.ylim(0, max(percentages) + 10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()




#%%
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
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})
        
        
        # # Extract district names and population data
        # district_population = {}
        # for row in data[1:]:
        #     district_name = row[1]
        #     population = int(row[0])
        #     district = district_name.split(',')[0].split(' ')[-1]
        #     district_population[district] = population
        
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
    
# Initialize empty DataFrame to store population data
population_data = pd.DataFrame()

# Loop through each year in the district_votes dictionary
for year in district_votes['10'].keys():
    # Retrieve population data for the corresponding year
    population = get_population(year, '48', '397e2c2610f07f1b5c63d726a8d2d6959274f01d')
    # Concatenate population data for the current year to the DataFrame
    if population is not None:
        population_data = pd.concat([population_data, population], axis=0)

# Calculate the ratio of district votes to population for each year
ratios = {}
for district, votes in district_votes.items():
    district_ratios = {}
    for year, vote_count in votes.items():
        if year in population_data.index:
            district_population = population_data.loc[year, 'population']
            ratio = vote_count / district_population * 100
            district_ratios[year] = ratio
    ratios[district] = district_ratios

# Plotting
for district, district_ratios in ratios.items():
    plt.figure(figsize=(8, 6))
    plt.bar(district_ratios.keys(), district_ratios.values(), color='red')
    plt.title(f'District {district} - Voting Population by Year')
    plt.xlabel('Year')
    plt.ylabel('Percent of Population which Voted')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    
    
    
#%%
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
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
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
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Merge population and voting data for each district
merged_data = {}
for district, votes_data in district_votes.items():
    print(f"Fetching data for district {district}...")
    population_data = get_population(2019, 'TX', '397e2c2610f07f1b5c63d726a8d2d6959274f01d')
    if population_data is not None:
        print(f"Population data for district {district} retrieved successfully.")
        merged_data[district] = population_data.join(pd.DataFrame(votes_data, index=[0])).astype(int)
    else:
        print(f"Failed to retrieve population data for district {district}.")
#%%
# Plot bar graphs for each district on separate sheets
for district, data in merged_data.items():
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', stacked=True)
    plt.title(f'District {district} - Population vs Votes')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'district_{district}_bar_graph.png')
    plt.close()
    
    
    
#%%
# Import necessary modules
import requests
import pandas as pd

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
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
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
    '10': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2012': 228328, '2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2012': 264518, '2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2012': 240629, '2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2012': 237187, '2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Insert API code
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Merge population and voting data for each district
merged_data = {}
for district, votes_data in district_votes.items():
    for year, vote_count in votes_data.items():
        print(f"Fetching data for district {district} and year {year}...")
        population_data = get_population(int(year), 'TX', api_key)
        if population_data is not None:
            print(f"Population data for district {district} and year {year} retrieved successfully.")
            merged_data.setdefault(district, []).append(population_data.join(pd.DataFrame({'votes': [vote_count]}, index=[0])).astype(int))
        else:
            print(f"Failed to retrieve population data for district {district} and year {year}.")
            
#%%
# Function to retrieve population data for congressional districts in Texas
def get_population(year, state_code, api_key):
    api_url = f'https://api.census.gov/data/{year}/acs/acs5'
    for_clause = 'congressional district:*'
    in_clause = f'state:{state_code}'
    
    # Construct the API request URL
    url = f"{api_url}?get=B01001_001E,NAME&for={for_clause}&in={in_clause}&key={api_key}"
    print("API URL:", url)  # Print the URL
    
    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
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
    
#%%
# FINAL ITERATION OF PRACTICE SCRIPTS (2010 CENSUS CONGRESSIONAL DISTRICTS) CORRECT SCRIPT ON 2010_CENSUS_CONGRESS_RESULTS

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
        
        print(response.text)
        
        # Parse the JSON response
        data = response.json()
        colnames = data[0]
        datarows = data[1:]
        district_population = pd.DataFrame(columns=colnames, data=datarows)
        district_population = district_population.set_index("congressional district")
        district_population = district_population.rename(columns={"B01001_001E": "population"})
        
        print(district_population.index.unique())
        
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
for district, votes_data in district_votes.items():
    print(f"Fetching data for district {district}...")
    population_data = get_population(2019, '48', '397e2c2610f07f1b5c63d726a8d2d6959274f01d')
    if population_data is not None:
        print(f"Population data for district {district} retrieved successfully.")
        merged_data[district] = population_data.join(pd.DataFrame(votes_data, index=[0])).astype(int)
    else:
        print(f"Failed to retrieve population data for district {district}.")
        
        
#%%
# SCRAP aggregate_election_results.py files

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
        print("Invalid ACS type. Please specify '1-year' or '5-year'.")
        return None
    
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
    '10': {'2006': 176755, '2008': 333083, '2010': 224171, '2012': 237187},
    '17': {'2012': 228328},
    '21': {'2006': 203782, '2008': 304350, '2010': 236545, '2012': 264518},
    '25': {'2006': 163424, '2008': 291296, '2010': 189247, '2012': 240629},
    '31': {'2012': 237187},
}

district_votes_after = {
    '10': {'2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Insert your API key here
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Define a function to calculate turnout
def calculate_turnout(votes_data):
    turnout = {}
    for district, elections in votes_data.items():
        total_votes = sum(elections.values())
        turnout[district] = total_votes
    return turnout

# Calculate turnout for before treatment period
turnout_before = calculate_turnout(district_votes_before)

# Calculate turnout for after treatment period
turnout_after = calculate_turnout(district_votes_after)

# Combine turnout data into a DataFrame
turnout_data = pd.DataFrame({'Before Treatment': turnout_before, 'After Treatment': turnout_after})

# Create a boxplot to visualize the mean turnout before and after treatment
plt.figure(figsize=(8, 6))
turnout_data.boxplot()
plt.title('Mean Turnout Before and After Treatment')
plt.ylabel('Turnout Ratio')
plt.xlabel('Treatment Period')
plt.show()



#%%
# Imported necessary modules
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def get_election_data(eids):
    api = "https://services.austintexas.gov/election/byrecord.cfm"

    pages = []

    for e in eids:
        payload = {'eid': e}
        response = requests.get(api, payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.body.main
        tables = main.findAll('table')
        summary = tables[0]
        trs = summary.findAll('tr')
        rows = {}
        for tr in trs:
            tds = tr.findAll('td')
            rows[tds[0].string] = tds[1].string
        pages.append(rows)
        rest = tables[1:]

    return pd.DataFrame(pages)

def calculate_turnout(data):
    # Remove commas from 'Total Ballots Cast' and 'City Population' columns and convert to float
    data['Total Ballots Cast:'] = data['Total Ballots Cast:'].str.replace(',', '').astype(float)
    data['City Population (at Time of the Election):'] = data['City Population (at Time of the Election):'].str.replace(',', '').astype(float)

    # Calculate ratio of 'Total Ballots Cast' to 'City Population'
    data['Ballots to Population Ratio'] = data['Total Ballots Cast:'] / data['City Population (at Time of the Election):']

    # Convert 'Date of Election' to datetime and extract year
    data['Year'] = pd.to_datetime(data['Date of Election:']).dt.year

    # Sort the data by year
    data_sorted = data.sort_values(by='Year')

    return data_sorted

# EIDs for relevant elections
eids = [154, 179, 192, 196, 198, 201, 205, 208]

# Retrieve election data
election_data = get_election_data(eids)

# Calculate turnout
turnout_data = calculate_turnout(election_data)

# Calculate average turnout ratio for Austin City Council elections
average_turnout_city_council = turnout_data['Ballots to Population Ratio'].mean()

# Relevant district votes data (before and after treatment)
district_votes_before = {
    '10': {'2012': 237187},
    '17': {'2012': 228328},
    '21': {'2012': 264518},
    '25': {'2012': 240629},
    '31': {'2012': 237187}
}

district_votes_after = {
    '10': {'2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937},
    '17': {'2014': 228324, '2016': 257480, '2018': 287600, '2020': 293947},
    '21': {'2014': 278590, '2016': 313702, '2018': 343727, '2020': 361356},
    '25': {'2014': 263649, '2016': 293328, '2018': 320164, '2020': 330193},
    '31': {'2014': 257725, '2016': 289194, '2018': 312626, '2020': 323937}
}

# Calculate turnout for aggregated congressional elections before and after treatment
def calculate_congressional_turnout(votes_data):
    turnout = {}
    for district, elections in votes_data.items():
        total_votes = sum(elections.values())
        turnout[district] = total_votes
    return turnout

congressional_turnout_before = calculate_congressional_turnout(district_votes_before)
congressional_turnout_after = calculate_congressional_turnout(district_votes_after)

# Calculate average turnout ratio for aggregated congressional elections before treatment
average_turnout_congressional_before = sum(congressional_turnout_before.values()) / len(congressional_turnout_before)

# Calculate average turnout ratio for aggregated congressional elections after treatment
average_turnout_congressional_after = sum(congressional_turnout_after.values()) / len(congressional_turnout_after)

# Create a boxplot to compare the average turnout before and after treatment
plt.figure(figsize=(8, 6))
plt.boxplot([
    [average_turnout_city_council], 
    [average_turnout_congressional_before], 
    [average_turnout_congressional_after]
], 
labels=['City Council', 'Congressional Before', 'Congressional After'])
plt.title('Average Turnout Before and After Treatment')
plt.ylabel('Turnout Ratio')
plt.xlabel('Treatment Period')
plt.show()



#%%
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

# Define the API key
api_key = '397e2c2610f07f1b5c63d726a8d2d6959274f01d'

# Define the relevant district votes data for Austin, Texas
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

# Function to calculate average votes versus population ratio for congressional district elections
def calculate_congressional_turnout(district_votes):
    average_turnout = {}
    for year, district_data in district_votes.items():
        population_data = get_population(year, '48', api_key, acs_type='1-year')
        if population_data is not None:
            total_votes = sum(district_data.values())
            total_population = sum(population_data['population'].astype(int))
            average_turnout[year] = total_votes / total_population
    return average_turnout

# Function to plot the average turnout ratios for Austin City Council and Congressional District Elections
def plot_average_turnout():
    # Calculate average ballots cast versus total population for Austin City Council elections (2006-2012)
    average_turnout_city_council_before = turnout_data[turnout_data['Year'] <= 2012]['Ballots to Population Ratio'].mean()

    # Aggregate the data for congressional district elections (2006-2012) and calculate the average votes versus population ratio
    average_turnout_congressional_before = calculate_congressional_turnout(district_votes_before)

    # Calculate average ballots cast versus total population for Austin City Council elections (2014-2020)
    average_turnout_city_council_after = turnout_data[turnout_data['Year'] >= 2014]['Ballots to Population Ratio'].mean()

    # Aggregate the data for congressional district elections (2014-2020) and calculate the average votes versus population ratio
    average_turnout_congressional_after = calculate_congressional_turnout(district_votes_after)

    # Plotting the results
    plt.figure(figsize=(10, 8))

    # Bar width
    bar_width = 0.35

    # Define the x locations for the groups
    index = [1, 2]

    # Plotting the data for Austin City Council elections
    plt.bar(index[0], average_turnout_city_council_before, bar_width, label='City Council (2006-2012)', color='b')
    plt.bar(index[1], average_turnout_city_council_after, bar_width, label='City Council (2014-2020)', color='g')

    # Plotting the data for congressional district elections
    if average_turnout_congressional_before:
        avg_turnout_before = sum(average_turnout_congressional_before.values()) / len(average_turnout_congressional_before)
    else:
        avg_turnout_before = 0
    plt.bar(index[0] + bar_width, avg_turnout_before, bar_width, label='Congressional (2006-2012)', color='r')

    if average_turnout_congressional_after:
        avg_turnout_after = sum(average_turnout_congressional_after.values()) / len(average_turnout_congressional_after)
    else:
        avg_turnout_after = 0
    plt.bar(index[1] + bar_width, avg_turnout_after, bar_width, label='Congressional (2014-2020)', color='y')

    # Adding labels and title
    plt.xlabel('Period')
    plt.ylabel('Average Turnout Ratio')
    plt.title('Average Turnout Ratio for Austin City Council and Congressional District Elections')
    plt.xticks([index[0] + bar_width / 2, index[1] + bar_width / 2], ['Before Treatment', 'After Treatment'])
    plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()

# Execute the function to plot the average turnout ratios
plot_average_turnout()



#%%
# ORIGINAL AGGREGATE OUTPUT

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
plt.xlabel('Aggregated Elections')
plt.ylabel('Average Ratio of Voters vs Population')
plt.title('Average Turnout Ratios Before and After Ward District Representation')
plt.xticks(rotation=45)

# Add legend outside the plot area
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

print("Average Turnout Ratios:")
print("City Council (2006-2012) Before:", avg_city_council_before)
print("City Council (2014-2020) After:", avg_city_council_after)
print("Congressional Districts (2006-2012) Before:", avg_district_before.mean())
print("Congressional Districts (2014-2020) After:", avg_district_after.mean())


#%%
# PLOTTING ROUGH DRAFT FOR T_TEST FILE


# Plotting the comparison
plt.figure(figsize=(12, 8))

# Plotting the average voter participation ratios for the period before ward district representation
plt.plot(avg_voter_participation_before['year'], avg_voter_participation_before['votes_per_capita'], marker='o', label='Before (2006-2010)')

# Plotting the average voter participation ratios for the period after ward district representation
plt.plot(avg_voter_participation_after['year'], avg_voter_participation_after['votes_per_capita'], marker='o', label='After (2014-2020)')

# Plotting the ratio of ballots cast to population for Austin City Council elections
plt.plot(data_sorted['Year'], data_sorted['Ballots to Population Ratio'], color='orange', label='Austin City Council Elections')

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



#%%
# T_TEST SCRAPS

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