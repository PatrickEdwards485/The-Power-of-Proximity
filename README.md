# The-Power-of-Proximity
## Does voter engagement increase when city councils change from at-large to district representation?

### Summary 

In 2012, the city of Austin, Texas implemented a change to the organization of its city council districts. The council, whose composition is comprised of ten members not including the city mayor, had previously been appointed through at-large elections in which the constituencies of all ten seats consisted of the entire city's population. The change, which took affect in the 2014 municipal elections, created ten wards throughout the city in which each seat became represented a specific area of Austin as a single-member district. The mayoral election remained a citywide contest. 

Supporters of ward district representation argue that smaller, single-member districts allow greater minority representation within legislative bodies. Certain communities which may lack sufficient demographics to elect like-minded representatives on an at-large level may gain a greater ability to elect like-minded representatives in smaller ward districts where said community becomes the majority in particular districts. Additionally, ward district representation allows a greater degree of proximity between candidates and constituents as the geographic area and population of ward districts are often significantly smaller than at-large districts. 

The purpose of this repository is to analyze whether this change in representation spurred an increase in voter participation in municipal elections in Austin. To test this hypothesis, population data and election results of the four city council elections immediately preceding the redistricting (2006, 2008, 2010, and 2012) and the four city council elections immediately following the redistricting (2014, 2016, 2018, 2020) are compared to population data and election results of all congressional districts which overlap with Austin city limits in the four elections immediately preceding and the four elections immediately following the city council redistricting. 

### Input Data 

The data generated to produce voter participation rates in Austin City Council elections originate from a publicly available database of candidates of voting statistics for Austin elections from 1840 to the present which is provided by the Office of the City Clerk. Population data and election results for relevant elections have been webscraped from the database, which can be visited at <https://services.austintexas.gov/election/search.cfm>. 

The data generated to produce election results for congressional districts which overlap with Austin city limits originate from publicly available .csv files provided by the Federal Elections Commission. The files include: 

**federalelections2006.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL' on the '2006 US House & Senate Results' sheet,

**2008congresults.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL ' on the '2008 House and Senate Results' sheet,

**federalelections2010.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL ' on the '2010 US House & Senate Results' sheet, 

**2012congresults.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2012 US House & Senate Results' sheet, 

**federalelections2016.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2016 US House Results by State' sheet,

**federalelections2018.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '2018 US House Results by State' sheet,

**federalelections2020.csv**, which includes relevant columns 'STATE', 'DISTRICT', and 'GENERAL VOTES ' on the '13. US House Results by State' sheet. 

The data generated to produce population data for congressional districts which overlap with Austin city limits originate from the US Census Bureau. Utilization of the Census API requires an API key, which can be acquired by filing an API key request at <https://api.census.gov/data/key_signup.html>. The API utilizes American Community Survey (ACS) 1-Year Data for the 2006, 2008, and 2010 elections and American Community Survey (ACS) 5-Year Data for the 2012, 2014, 2016, 2018, and 2020 elections. 

### Output Data 

A script called **austin_city_council_elections.py** generates a graph which shows the ratio of Austin City Council election voters versus the population of Austin in municipal elections from 2006 to 2022. 

A script called **2000_census_congressional_results** generates three graphs which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2006, 2008, and 2010 elections (Districts 10, 21, and 25) in congressional elections from 2006 to 2010. 

A script called **2010_census_congressional_results** generates five graphs which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2012, 2012, 2016, 2018, and 2020 elections (Districts 10, 17, 21, 25, and 31) in congressional elections from 2012 to 2020. 

A script called **config.py**, which exists in the .getignore file and holds the API key to access ACS information. 

A script called **aggregate_election_results.py** generates a graph which shows the average aggregate ratio of congressional election voters versus the population of the districts from 2006 to 2012 (before ward representation), and the average aggregate ratio of congressional election voters versus the population of the districts from 2014 to 2020 (after ward representation). 

A script called **t_test.py** generates a t-test on the statistical significance of the difference of means between Austin City Council election turnout and congressional election turnout before and after the change to ward representation ahead of the 2014 elections. 

### Findings 

The output data generated by the repository scripts show little sign of significant changes in voter participation rates with Austin city elections after the implementation of ward district representation in comparison to congressional voter participation rates. 

There may be a variety of factors which influence these findings, such as: 

    1. Austin City Council elections are held concurrent to congressional elections. This means that all Austin voters who cast ballots in City Council elections have the opportunity to cast ballots for their congressional election at the same time. This may mean that congressional election participation rates rose at similar rates compared to City Council election participation because of the City Council election change due to the overlap between constituencies. 

    2. Omitted variables may affect the voter participation rates of both City Council elections and congressional elections. For example, a statewide election or initiative or a national election may affect voter participation rates across City Council wards and congressional districts. If these outside factors affect voter participation in relevant areas, then the affect of ward representation may be overshadowed or nullified. 
    
    3. Due to the focus on a particular city and a finite number of congressional districts, an uncontested race may skew voter participation results and affect election data. To nullify this potential, the repository scripts analyze data from multiple elections before and after the change to ward representation. However, average ratios may still be affected due to a lack of choice for certain voters. 

### Future Research 

The components of this repository have been designed to allow for further analyzation of the included data. If desired, the user may use the existing scripts to run a significance test on the data or include further election statistics to structure a greater understanding of the repository findings. 

Additionally, as the repository components comprise a launch pad for election analysis, the repository scripts may be mirrored or substantiated with similar data from other electoral districts to analyze whether voter participation rates in Austin are similar or divergent after the change to ward district representation compared to other jurisdictions who have made similar changes. 