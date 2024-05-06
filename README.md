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

## Deliverables 

A script called **austin_city_council_elections.py** generates a graph which shows the ratio of Austin City Council election voters versus the population of Austin in municipal elections from 2006 to 2022. 

A script called **2000_census_congressional_results** generates three graphs which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2006, 2008, and 2010 elections (Districts 10, 21, and 25) in congressional elections from 2006 to 2010. 

A script called **2010_census_congressional_results** generates five graphs which each show the ratio of congressional election voters versus the population of the district in each respective congressional district which overlapped with Austin city limits during the 2012, 2012, 2016, 2018, and 2020 elections (Districts 10, 17, 21, 25, and 31) in congressional elections from 2012 to 2020. 
