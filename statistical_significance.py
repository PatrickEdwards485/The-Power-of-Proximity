# Import necessary modules
import pandas as pd
import requests 
import matplotlib.pyplot as plt
from scipy import stats

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

# Control group data (for diff-in-diff)
control_before = [176755, 203782, 163424]  # Example values, replace with actual data
control_after = [237187, 264518, 240629]  # Example values, replace with actual data

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

# Calculate the difference in means for the diff-in-diff analysis
diff_in_means_before = merged_before['turnout_ratio'].mean() - pd.Series(control_before).mean()
diff_in_means_after = merged_after['turnout_ratio'].mean() - pd.Series(control_after).mean()

# Perform the t-test
t_statistic, p_value = stats.ttest_ind(merged_before['turnout_ratio'], pd.Series(control_before))
t_statistic_after, p_value_after = stats.ttest_ind(merged_after['turnout_ratio'], pd.Series(control_after))

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(['2006-2012', '2014-2020'], [merged_before['turnout_ratio'].mean(), merged_after['turnout_ratio'].mean()], color='blue', label='City Council')
plt.bar(['2006-2012', '2014-2020'], [pd.Series(control_before).mean(), pd.Series(control_after).mean()], color='red', label='Congressional Districts')

# Annotate the bars with the difference in means
plt.text(0, merged_before['turnout_ratio'].mean() + 0.01, f'Diff in Means: {diff_in_means_before:.4f}', ha='center', va='bottom')
plt.text(1, merged_after['turnout_ratio'].mean() + 0.01, f'Diff in Means: {diff_in_means_after:.4f}', ha='center', va='bottom')

plt.title('Average Turnout Ratio Comparison')
plt.xlabel('Period')
plt.ylabel('Turnout Ratio (Votes/Population)')
plt.grid(axis='y')
plt.legend()
plt.show()

# Print t-test results
print("T-test results for 2006-2012:")
print(f"T-statistic: {t_statistic:.4f}, p-value: {p_value:.4f}")
print("\nT-test results for 2014-2020:")
print(f"T-statistic: {t_statistic_after:.4f}, p-value: {p_value_after:.4f}")


#%%
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# Calculate the difference in means for the diff-in-diff analysis
diff_in_means_before = (merged_before['turnout_ratio'] - merged_before['district']).mean()
diff_in_means_after = (merged_after['turnout_ratio'] - merged_after['district']).mean()

# Perform the t-test
t_statistic, p_value = stats.ttest_ind(merged_before['turnout_ratio'] - merged_before['district'],
                                       merged_after['turnout_ratio'] - merged_after['district'])

# Plotting
plt.figure(figsize=(10, 6))

# Plot bars for the difference-in-differences
plt.bar(['2006-2012', '2014-2020'], [diff_in_means_before, diff_in_means_after], color=['blue', 'red'])

plt.title('Difference-in-Differences Analysis')
plt.xlabel('Period')
plt.ylabel('Difference in Means (Turnout Ratio)')
plt.grid(axis='y')
plt.show()

# Print t-test results
print("Difference-in-Differences T-test results:")
print(f"T-statistic: {t_statistic:.4f}, p-value: {p_value:.4f}")
