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
 