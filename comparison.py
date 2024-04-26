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
    max_votes_2020 = relevant_districts_2020[relevant_districts_2020['DISTRICT'] == district]['GENERAL VOTES'].sum()
    
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