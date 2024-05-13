# The-Power-of-Proximity
## Does voter engagement increase when city councils change from at-large to district representation?

### Summary 

In 2012, the city of Austin, Texas implemented a change to the organization of its city council districts. The council, whose composition is comprised of ten members not including the city mayor, had previously been appointed through at-large elections in which the constituencies of all ten seats consisted of the entire city's population. The change, which took affect in the 2014 municipal elections, created ten wards throughout the city in which each seat became represented a specific area of Austin as a single-member district. The mayoral election remained a citywide contest. 

Supporters of ward district representation argue that smaller, single-member districts allow greater minority representation within legislative bodies. Certain communities which may lack sufficient demographics to elect like-minded representatives on an at-large level may gain a greater ability to elect like-minded representatives in smaller ward districts where said community becomes the majority in particular districts. Additionally, ward district representation allows a greater degree of proximity between candidates and constituents as the geographic area and population of ward districts are often significantly smaller than at-large districts. 

The purpose of this repository is to analyze whether this change in representation spurred an increase in voter participation in municipal elections in Austin. To test this hypothesis, population data and election results of the four city council elections immediately preceding the redistricting (2006, 2008, 2010, and 2012) and the four city council elections immediately following the redistricting (2014, 2016, 2018, 2020) are compared to population data and election results of all congressional districts which overlap with Austin city limits in the four elections immediately preceding and the four elections immediately following the city council redistricting. 

### Input Data 

The data generated to produce voter participation rates in Austin City Council elections originate from a publicly available database of candidates and voting statistics for Austin elections from 1840 to the present which is provided by the Office of the City Clerk. Population data and election results for relevant elections have been webscraped from the database, which can be visited at <https://services.austintexas.gov/election/search.cfm>. 

The data generated to produce election results for congressional districts which overlap with Austin city limits originate from publicly available .csv files provided by the Federal Elections Commission. The files include: 

**federalelections2006.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL' on the '2006 US House & Senate Results' sheet,

**2008congresults.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL ' on the '2008 House and Senate Results' sheet,

**federalelections2010.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL ' on the '2010 US House & Senate Results' sheet, 

**2012congresults.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2012 US House & Senate Results' sheet, 

**results14.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2014 US House Results by State' sheet, 

**federalelections2016.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2016 US House Results by State' sheet,

**federalelections2018.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2018 US House Results by State' sheet,

**federalelections2020.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '13. US House Results by State' sheet. 

The data generated to produce population data for congressional districts which overlap with Austin city limits originate from the US Census Bureau. Utilization of the Census API requires an API key, which can be acquired by filing an API key request at <https://api.census.gov/data/key_signup.html>. The Census API utilizes American Community Survey (ACS) 1-Year Data for the 2006, 2008, and 2010 elections and American Community Survey (ACS) 5-Year Data for the 2012, 2014, 2016, 2018, and 2020 elections. The user should insert their assigned API key into all necessary scripts by replacing 'your_API_key_here' in lines coded "api_key = 'your_API_key_here'". All necessary scripts are denoted in Output Data. 

### Output Data 

A script called **austin_city_council_election_results.py** generates a graph (city_council_elections_graph.png) which shows the ratio of Austin City Council election voters versus the population of Austin in municipal elections from 2006 to 2022. 

A script called **2000_census_congressional_results** generates three graphs (district_10_2000_census.png; district_21_2000_census.png; district_25_2000_census.png) which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2006, 2008, and 2010 elections (Districts 10, 21, and 25) in congressional elections from 2006 to 2010. 
    * This script necessitates an API key. 

A script called **2010_census_congressional_results** generates five graphs (district_10_2010_census.png; district_17_2010_census.png; district_21_2010_census.png; district_25_2010_census.png; district_31_2010_census.png) which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2012, 2014, 2016, 2018, and 2020 elections (Districts 10, 17, 21, 25, and 31) in congressional elections from 2012 to 2020.  
    * This script necessitates an API key. 

A script called **aggregate_election_results.py** generates a graph (aggregate_congressional_elections_graph.png) which shows the average aggregate ratio of congressional election voters versus the population of the districts from 2006 to 2012 (before ward representation), and the average aggregate ratio of congressional election voters versus the population of the districts from 2014 to 2020 (after ward representation). 
    * This script necessitates an API key. 

A script called **election_comparison.py** generates a graph (elections_comparison_graph.png) which shows the average aggregate ratio of congressional election voters against the ratio of Austin City Council election voters from the 2006 to 2020 elections for user visualization and comparison. 
    * This script necessitates an API key. 

### Findings 

The output data generated by the repository scripts shows evidence of a significant change in voter participation rates between Austin City Council elections and congressional elections after the City Council change to ward district representation. In the elections before ward representation (2006-2012), voter participation rates follow similar patterns year over year in City Council elections and aggregate congressional elections. Moreover, City Council elections and aggregate congressional elections experience similar voter participation rates in each election during this period. 

These similarities do not exist in the elections after ward representation (2014-2020). Voter participation rates increase at a higher level in City Council elections compared to aggregate congressional elections over this period, which may support the hypothesis that a municipal change to ward representation in City Council elections led to an increase in voter participation rates within Austin. 

However, voter participation rates in the 2014 elections specifically experience an inverse result to other elections over this period. The voter participation rate for the 2014 City Council election decreases compared to 2012 and 2016 rates, whereas the 2014 aggregate congressional elections experiences little to no decrease compared to 2012 and 2016 rates. As the 2014 City Council election was the first election to occur after the municipal change to ward representation in City Council elections, a decrease in voter participation rates between the 2012 and 2014 City Council elections contradicts the hypothesis that a municipal change to ward representation in City Council elections led to an increase in voter participation rates within Austin. 

It should be acknowledged that outside variables have been omitted from the repository analysis. Omitted variables may skew relevant data and lead to an incorrect conclusion regarding repository findings if the user considers repository findings alone. 

There may be a variety of factors which influence these findings, such as: 

    1. Austin City Council elections are held concurrent to congressional elections. This means that all Austin voters who cast ballots in City Council elections have the opportunity to cast ballots for their congressional election at the same time. This may mean that congressional election participation rates regularly experience similar rates compared to City Council election participation because of the City Council election change due to the overlap between constituencies. 

    2. Omitted variables may affect the voter participation rates of both City Council elections and congressional elections. For example, a statewide election or initiative or a national election may affect voter participation rates across City Council wards and congressional districts. If these outside factors affect voter participation in relevant areas, then the affect of ward representation may be overshadowed or nullified. 

    3. Due to the focus on a particular city and a finite number of congressional districts, an uncontested race may skew voter participation results and affect election data. To nullify this potential, the repository scripts analyze data from multiple elections before and after the change to ward representation. However, ratios of voter participation rates in specific elections may still be affected due to a lack of choice for certain voters in a specific year. 

### Future Research 

The components of this repository have been designed to allow for further analyzation of the included data. If desired, the user may use the existing scripts to run a significance test on the data or to include further election statistics to structure a greater understanding of the repository findings. For example, the data generated in **election_comparison.py** can be taken to further analyze the repository findings through mechanisms such as running t-tests on the statistical significance of voter participation rates before and after the change to ward representation. 

Additionally, as the repository components comprise a launch pad for election analysis, the repository scripts may be mirrored or substantiated with similar data from other electoral districts to analyze whether voter participation rates in Austin are similar or divergent after the change to ward district representation compared to other jurisdictions who have made similar changes. While repository findings may only be applied to the effect of ward district representation in Austin due to concerns about external validity, the repository scripts may serve as tools for analyzation of data in similar circumstances if the user replaces or substantiates the repository data with outside data within the repository scripts. 
