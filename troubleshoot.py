import requests
import config
import pandas as pd
import matplotlib.pyplot as plt

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

        # Print the API response status code for debugging
        print("Response status code:", response.status_code)

        # Parse the JSON response
        data = response.json()

        # Print the parsed JSON data for debugging
        print("Parsed JSON data:", data)

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