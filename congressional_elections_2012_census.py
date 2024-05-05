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