# Imported necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import zipfile

with zipfile.ZipFile("federalelections2006.zip", 'r') as zip_ref:
    zip_ref.extractall(".")
    
congress = pd.read_csv("federalelections2006.zip", dtype=str, encoding='latin1')

desired_districts = ['TX-10', 'TX-21', 'TX-25']
filtered_data = congress[congress['district'].isin(desired_districts)]

filtered_data['votes'] = filtered_data['votes'].replace('UNOPPOSED', '0')





def filter_austin_districts(df):
    return df[df['District'].str.contains('Austin, Texas', case=False)]

def calculate_turnout_percentage(df):
    total_registered = df['Registered Voters'].sum()
    total_votes = df['Votes'].sum()
    return (total_votes / total_registered) * 100

years = []
turnout_percentages = []

for year, file_path in file_paths.items():
    df = pd.read_excel(file_path)
    austin_df = filter_austin_districts(df)
    turnout_percentage = calculate_turnout_percentage(austin_df)
    years.append(year)
    turnout_percentages.append(turnout_percentage)



#%%
# THIS IS THE CORRECT CODE FOR 2006 RESULTS ON city_council_results.py
# Imported necessary module
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "federalelections2006.xls"

df = pd.read_excel(file_path, sheet_name='2006 US House & Senate Results')

relevant_districts = df[(df['STATE'] == 'Texas') &
                        (df['DISTRICT'].isin(['10', '21', '25']))]

relevant_districts['GENERAL'] = relevant_districts['GENERAL'].replace('UNOPPOSED', np.nan)

nan_values = relevant_districts['GENERAL'].isna().sum()
print("Number of NaN values in 'GENERAL' column:", nan_values)
print(relevant_districts)

total_votes_by_district = relevant_districts.groupby('DISTRICT')['GENERAL'].sum()

print(total_votes_by_district)


plt.figure(figsize=(10, 6))
plt.bar(years, turnout_percentages, color='red')
plt.xlabel('Election Year')
plt.ylabel('Voter Turnout Percentage')
plt.title('Voter Turout Percantage in Congressional Districts Overlapping Austin, Texas')
plt.xticks(years)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()



#%%
# THIS IS THE CORRECT CODE FOR 2008 RESULTS ON city_council_results.py
import pandas as pd
import numpy as np

# Specify the file path for the 2008 Excel file
file_path = "2008congresults.xls"

# Specify the sheet name for the 2008 Excel file
sheet_name = "2008 House and Senate Results"

# Read the 2008 Excel file into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)

print("Column names for the DataFrame:")
print(df.columns)
print("First few rows of the DataFrame:")
print(df.head())

# Filter the DataFrame to include only the relevant districts in Texas
relevant_districts = df[(df['STATE'] == 'Texas') &
                        (df['DISTRICT'].isin(['10', '21', '25']))]

print("Structure of the DataFrame relevant_districts:")
print(relevant_districts.info())

# Remove the trailing space from the column name 'GENERAL '
relevant_districts.rename(columns={'GENERAL ': 'GENERAL'}, inplace=True)

# Print the first few rows of the DataFrame to verify the changes
print("First few rows of the DataFrame after renaming the column:")
print(relevant_districts.head())

# Now try accessing the 'GENERAL' column again
if 'GENERAL' in relevant_districts.columns:
    nan_values = relevant_districts['GENERAL'].isna().sum()
    print("Number of NaN values in 'GENERAL' column:", nan_values)
    
    print("Data types of 'GENERAL' column:")
    print(relevant_districts['GENERAL'].dtype)

    # Calculate total votes by district
    total_votes_by_district = relevant_districts.groupby('DISTRICT')['GENERAL'].sum()
    print(total_votes_by_district)
else:
    print("Column 'GENERAL' not found in the DataFrame relevant_districts")

# Convert 'GENERAL' column to numeric, coercing non-numeric values to NaN
relevant_districts['GENERAL'] = pd.to_numeric(relevant_districts['GENERAL'], errors='coerce')

# Print the data types of the 'GENERAL' column after conversion
print("Data types of 'GENERAL' column after conversion:")
print(relevant_districts['GENERAL'].dtype)


#%%
# CORRECT SCRIPT ON city_council_results.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the 2006 Excel file
file_path_2006 = "federalelections2006.xls"
df_2006 = pd.read_excel(file_path_2006, sheet_name='2006 US House & Senate Results')

# Filter relevant districts for 2006
relevant_districts_2006 = df_2006[df_2006['DISTRICT'].isin(['10', '21', '25'])]

# Clean data for 2006
relevant_districts_2006['GENERAL'] = relevant_districts_2006['GENERAL'].replace('UNOPPOSED', np.nan)
relevant_districts_2006['GENERAL'] = pd.to_numeric(relevant_districts_2006['GENERAL'], errors='coerce')

# Read the 2008 Excel file
file_path_2008 = "2008congresults.xls"
df_2008 = pd.read_excel(file_path_2008, sheet_name='2008 House and Senate Results')

# Filter relevant districts for 2008
relevant_districts_2008 = df_2008[df_2008['DISTRICT'].isin(['10', '21', '25'])]

# Clean data for 2008
relevant_districts_2008.rename(columns={'GENERAL ': 'GENERAL'}, inplace=True)
relevant_districts_2008['GENERAL'] = pd.to_numeric(relevant_districts_2008['GENERAL'], errors='coerce')

# Plot bar graphs for each district
for district in ['10', '21', '25']:
    plt.figure(figsize=(8, 6))
    
    # Plot for 2006
    plt.bar('2006', relevant_districts_2006[relevant_districts_2006['DISTRICT'] == district]['GENERAL'].sum(), color='blue', label='2006')
    
    # Plot for 2008
    plt.bar('2008', relevant_districts_2008[relevant_districts_2008['DISTRICT'] == district]['GENERAL'].sum(), color='red', label='2008')
    
    plt.xlabel('Year')
    plt.ylabel('Vote Totals')
    plt.title(f'Vote Totals for District {district} (2006 vs 2008)')
    plt.legend()
    plt.show()



#%%
# PREVIOUS CONTENTS OF city_council_elections.py BEFORE THE ABOVE SCRIPT WAS INSERTED
# Imported necessary module
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_paths = {
    2006: "federalelections2006.xls",
    2008: "2008congresults.xls"
    }

for year, file_path in file_paths.items():
    if year == 2006:
        sheet_name = '2006 US House & Senate Results'
    if year == 2008:
        sheet_name = '2008 House and Senate Results'
        
    df = pd.read_excel(file_path, sheet_name=sheet_name)

print(f"Column names for the DataFrame for the year {year}:")
print(df.columns)
print(f"First few rows of the DataFrame for the year {year}:")
print(df.head())

relevant_districts = df[(df['STATE'] == 'Texas') &
                        (df['DISTRICT'].isin(['10', '21', '25']))]

relevant_districts['GENERAL'] = relevant_districts['GENERAL'].replace('#', np.nan)
relevant_districts['GENERAL'] = relevant_districts['GENERAL'].replace('UNOPPOSED', np.nan)


print(f"Columns of the DataFrame relevant_districts for the year {year}")
print(relevant_districts)


nan_values = relevant_districts['GENERAL'].isna().sum()
print("Number of NaN values in 'GENERAL' column:", nan_values)
print(relevant_districts)


if 'GENERAL' in relevant_districts.columns:
    total_votes_by_district = relevant_districts.groupby('DISTRICT')['GENERAL'].sum()
    print(total_votes_by_district)
else:
    print("Column 'GENERAL' not found in the DataFrame relevant_districts")
#%%

total_votes_by_district = relevant_districts.groupby('DISTRICT')['GENERAL'].sum()

print(total_votes_by_district)



#%%
# UPDATED CORRECT SCRIPT FOR 2006 AND 2008 RESULTS ON city_council_results.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the 2006 Excel file
file_path_2006 = "federalelections2006.xls"
df_2006 = pd.read_excel(file_path_2006, sheet_name='2006 US House & Senate Results')

# Filter relevant districts for 2006 in Texas
relevant_districts_2006 = df_2006[(df_2006['DISTRICT'].isin(['10', '21', '25'])) & (df_2006['STATE'] == 'Texas')]

# Clean data for 2006
relevant_districts_2006['GENERAL'] = relevant_districts_2006['GENERAL'].replace('UNOPPOSED', np.nan)
relevant_districts_2006['GENERAL'] = pd.to_numeric(relevant_districts_2006['GENERAL'], errors='coerce')

# Read the 2008 Excel file
file_path_2008 = "2008congresults.xls"
df_2008 = pd.read_excel(file_path_2008, sheet_name='2008 House and Senate Results')

# Filter relevant districts for 2008 in Texas
relevant_districts_2008 = df_2008[(df_2008['DISTRICT'].isin(['10', '21', '25'])) & (df_2008['STATE'] == 'Texas')]

# Clean data for 2008
relevant_districts_2008.rename(columns={'GENERAL ': 'GENERAL'}, inplace=True)
relevant_districts_2008['GENERAL'] = relevant_districts_2008['GENERAL'].replace('UNOPPOSED', np.nan)
relevant_districts_2008['GENERAL'] = pd.to_numeric(relevant_districts_2008['GENERAL'], errors='coerce')

# Plot bar graphs for each district
for district in ['10', '21', '25']:
    plt.figure(figsize=(8, 6))
    
    # Calculate maximum vote totals for 2006 and 2008
    max_votes_2006 = relevant_districts_2006[relevant_districts_2006['DISTRICT'] == district]['GENERAL'].sum()
    max_votes_2008 = relevant_districts_2008[relevant_districts_2008['DISTRICT'] == district]['GENERAL'].sum()
    
    # Find the maximum of the two maximum values
    max_votes = max(max_votes_2006, max_votes_2008)
    
    # Plot for 2006
    plt.bar('2006', relevant_districts_2006[relevant_districts_2006['DISTRICT'] == district]['GENERAL'].sum(), color='blue', label='2006')
    
    # Plot for 2008
    plt.bar('2008', relevant_districts_2008[relevant_districts_2008['DISTRICT'] == district]['GENERAL'].sum(), color='red', label='2008')
    
    plt.xlabel('Year')
    plt.ylabel('Vote Totals')
    plt.title(f'Vote Totals for District {district} (2006 vs 2008)')
    plt.legend()
    plt.ylim(0, max_votes * 1.1)
    plt.show()



#%%
file_path_2010 = "federalelections2010.xls"
df_2010 = pd.read_excel(file_path_2010, sheet_name='2010 US House & Senate Results')
df_2010['DISTRICT'] = df_2010['DISTRICT'].astype(str)

relevant_districts_2010 = df_2010[(df_2010['DISTRICT'].isin(['10', '21', '25'])) & (df_2010['STATE'] == 'Texas')].copy()
relevant_districts_2010['DISTRICT'] = relevant_districts_2010['DISTRICT'].astype(str)

# Summing up the votes for each district
votes_per_district = relevant_districts_2010.groupby('DISTRICT')['GENERAL '].sum()

# Printing the total number of votes for each district
print("Total votes per district:")
print(votes_per_district)

# ADD ONS TO HELP WITH EXCEL DISCREPANCIES
# Filter relevant districts for 2010
relevant_districts_2010 = df_2010[(df_2010['DISTRICT'] == '10') & (df_2010['STATE'] == 'Texas')]

# Print filtering conditions
print("Filtering conditions for District 10 in 2010:")
print(relevant_districts_2010)

file_path_2010 = "federalelections2010.xls"
df_2010 = pd.read_excel(file_path_2010, sheet_name='2010 US House & Senate Results')
print(df_2010.head())

relevant_districts_2010 = df_2010[(df_2010['DISTRICT'].isin(['10', '21', '25'])) & (df_2010['STATE'] == 'Texas')]
print(relevant_districts_2010)

print(relevant_districts_2010['DISTRICT'].unique())


#%%
# PREVIOUS congressional_elections_2012_census.py SCRIPT BEFORE CREATING UNIVERSAL Y-AXIS SCALE
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    plt.ylim(0, max(max_votes_2012, max_votes_2014, max_votes_2016, max_votes_2018, max_votes_2020) * 1.1)
    plt.show()



#%%
# PREVIOUS congressional_elections_2012_census.py SCRIPT BEFORE ABOVE CHANGE (USING ONLY 'DISTRICT VOTES:' VOTE TOTALS)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the 2012 Excel file
file_path_2012 = "2012congresults.xls"
df_2012 = pd.read_excel(file_path_2012, sheet_name='2012 US House & Senate Results')

# Filter relevant districts for 2012 in Texas
relevant_districts_2012 = df_2012[(df_2012['D'].isin(['10', '17', '21', '25', '31'])) & (df_2012['STATE'] == 'Texas')]

# Clean data for 2012
relevant_districts_2012.rename(columns={'GENERAL VOTES ': 'GENERAL VOTES'}, inplace=True)
relevant_districts_2012.loc[:, 'GENERAL VOTES'] = relevant_districts_2012['GENERAL VOTES'].replace('UNOPPOSED', np.nan)
relevant_districts_2012.loc[:, 'GENERAL VOTES'] = pd.to_numeric(relevant_districts_2012['GENERAL VOTES'], errors='coerce')

# Read the 2014 Excel file
file_path_2014 = "results14.xls"
df_2014 = pd.read_excel(file_path_2014, sheet_name='2014 US House Results by State')

# Filter relevant districts for 2014 in Texas
relevant_districts_2014 = df_2014[(df_2014['D'].isin(['10', '17', '21', '25', '31'])) & (df_2014['STATE'] == 'Texas')]

# Clean data for 2014
relevant_districts_2014.rename(columns={'GENERAL VOTES ': 'GENERAL VOTES'}, inplace=True)
relevant_districts_2014.loc[:, 'GENERAL VOTES'] = relevant_districts_2014['GENERAL VOTES'].replace('UNOPPOSED', np.nan)
relevant_districts_2014.loc[:, 'GENERAL VOTES'] = pd.to_numeric(relevant_districts_2014['GENERAL VOTES'], errors='coerce')

# Read the 2016 Excel file
file_path_2016 = "federalelections2016.xlsx"
df_2016 = pd.read_excel(file_path_2016, sheet_name='2016 US House Results by State')

# Filter relevant districts for 2016 in Texas
relevant_districts_2016 = df_2016[(df_2016['D'].isin(['10', '17', '21', '25', '31'])) & (df_2016['STATE'] == 'Texas')]

# Clean data for 2016
relevant_districts_2016.rename(columns={'GENERAL VOTES ': 'GENERAL VOTES'}, inplace=True)
relevant_districts_2016.loc[:, 'GENERAL VOTES'] = relevant_districts_2016['GENERAL VOTES'].replace('UNOPPOSED', np.nan)
relevant_districts_2016.loc[:, 'GENERAL VOTES'] = pd.to_numeric(relevant_districts_2016['GENERAL VOTES'], errors='coerce')

# Read the 2018 Excel file
file_path_2018 = "federalelections2018.xlsx"
df_2018 = pd.read_excel(file_path_2018, sheet_name='2018 US House Results by State')
df_2018['DISTRICT'] = df_2018['DISTRICT'].astype(str)

# Filter relevant districts for 2018 in Texas
relevant_districts_2018 = df_2018[(df_2018['DISTRICT'].isin(['10', '17', '21', '25', '31'])) & (df_2018['STATE'] == 'Texas')]

# Clean data for 2018
relevant_districts_2018.rename(columns={'GENERAL VOTES ': 'GENERAL VOTES'}, inplace=True)
relevant_districts_2018.loc[:, 'GENERAL VOTES'] = relevant_districts_2018['GENERAL VOTES'].replace('UNOPPOSED', np.nan)
relevant_districts_2018.loc[:, 'GENERAL VOTES'] = pd.to_numeric(relevant_districts_2018['GENERAL VOTES'], errors='coerce')

# Read the 2020 Excel file
file_path_2020 = "federalelections2020.xlsx"
df_2020 = pd.read_excel(file_path_2020, sheet_name='13. US House Results by State')

# Filter relevant districts for 2020 in Texas
relevant_districts_2020 = df_2020[(df_2020['DISTRICT'].isin(['10', '17', '21', '25', '31'])) & (df_2020['STATE'] == 'Texas')]

# Clean data for 2020
relevant_districts_2020.rename(columns={'GENERAL VOTES ': 'GENERAL VOTES'}, inplace=True)
relevant_districts_2020.loc[:, 'GENERAL VOTES'] = relevant_districts_2020['GENERAL VOTES'].replace('UNOPPOSED', np.nan)
relevant_districts_2020.loc[:, 'GENERAL VOTES'] = pd.to_numeric(relevant_districts_2020['GENERAL VOTES'], errors='coerce')

# Plot bar graphs for each district
for district in ['10', '17', '21', '25', '31']:
    plt.figure(figsize=(8, 6))
    
    # Calculate maximum vote totals
    max_votes_2012 = relevant_districts_2012[relevant_districts_2012['D'] == district]['GENERAL VOTES'].sum()
    max_votes_2014 = relevant_districts_2014[relevant_districts_2014['D'] == district]['GENERAL VOTES'].sum()
    max_votes_2016 = relevant_districts_2016[relevant_districts_2016['D'] == district]['GENERAL VOTES'].sum()
    max_votes_2018 = relevant_districts_2018[relevant_districts_2018['DISTRICT'] == district]['GENERAL VOTES'].sum()
    max_votes_2020 = relevant_districts_2018[relevant_districts_2018['DISTRICT'] == district]['GENERAL VOTES'].sum()
    
    # Find the maximum of the two maximum values
    max_votes = max(max_votes_2012, max_votes_2014, max_votes_2016, max_votes_2018, max_votes_2020)
    
    # Plot for 2012
    plt.bar('2012', relevant_districts_2012[relevant_districts_2012['D'] == district]['GENERAL VOTES'].sum(), color='red', label='2012')
    
    # Plot for 2014
    plt.bar('2014', relevant_districts_2014[relevant_districts_2014['D'] == district]['GENERAL VOTES'].sum(), color='red', label='2014')
    
    # Plot for 2016
    plt.bar('2016', relevant_districts_2016[relevant_districts_2016['D'] == district]['GENERAL VOTES'].sum(), color='red', label='2016')
    
    # Plot for 2018
    plt.bar('2018', relevant_districts_2018[relevant_districts_2018['DISTRICT'] == district]['GENERAL VOTES'].sum(), color='red', label='2018')
    
    # Plot for 2020
    plt.bar('2020', relevant_districts_2020[relevant_districts_2020['DISTRICT'] == district]['GENERAL VOTES'].sum(), color='red', label='2020')
    
    plt.xlabel('Year')
    plt.ylabel('Vote Totals')
    plt.title(f'Vote Totals for District {district} (2012-2020 Elections)')
    plt.legend()
    plt.ylim(0, max_votes * 1.1)
    plt.show()
    