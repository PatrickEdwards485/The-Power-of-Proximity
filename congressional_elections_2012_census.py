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