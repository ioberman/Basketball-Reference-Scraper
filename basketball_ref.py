#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup
pd.set_option('display.max_columns', None)


#SCRAPE ALL PLAYER STATS

#add your base url with curly braces where year will be inserted
base_URL = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

#identify start and end years
start_year = 1956
end_year = 2023

#create empty list
dfs = []

request_delay = 6

#Loop through every year
for year in range(start_year, end_year + 1):

    url = base_URL.format(year)

    res = requests.get(url)
    
    #checking if successful request
    if res.status_code == 200:

        #uses beautiful soup to pull in content and find table
        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find('table', {'class': 'sortable'})

        #checking if a table is found
        if table:

            #create a blank list of table data
            table_data = []
            #find all <tr> elements in the table and iterate through them
            for row in table.find_all('tr'):
                #for each row find all <th> and <td> elements
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['th' and 'td'])]
                #append row data into our table_data list
                table_data.append(row_data)

            #check if there is table data
            if table_data:

                #checking for headers
                if table_data[0]:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])
                else:
                    df = pd.DataFrame(table_data)
                #adding year column using our year var
                df['Year'] = year
                #appends this df onto our larger df
                dfs.append(df)
                #basketball-reference rate limits ips that make more than 20 bot requests in a minute so this delay avoids that
                time.sleep(request_delay) 
                
# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Export the combined DataFrame to a CSV file
#combined_df.to_csv('basketball_reference_per_game_stats.csv', index=False)


#remove null rows
df_final = combined_df.dropna(subset=[0])


#add headers
headers = ['PLAYER', 'POS', 'AGE', 'TEAM', 'GP', 'GS', 'MPG', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', '2PM', '2PA', '2P%', 'eFG%', 'FTM', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'Year']

df_final.columns = headers

#add column that will be used to merge scraped data later
df_final['Merge Field'] = df_final['PLAYER'] + df_final['POS'] + df_final['Year'].astype(str)

#send to CSV (uncomment to send only this file to csv)
#df_final.to_csv('Documents/historical_nba_data.csv', index=False)



#SCRAPE MVPs

#url of table being scraped
url = "https://www.basketball-reference.com/awards/mvp.html"

#get request on url to pull data
res = requests.get(url)

#checks if get request is successful
if res.status_code == 200:

    #uses beautiful soup to pull in content and find table
    soup = BeautifulSoup(res.content, 'html.parser')

    table = soup.find('table', {'class': 'sortable'})

    #checks if a table is found
    if table:
        #creates empty list to hold our data
        table_data = []
        #initiates variable to hold column num int
        max_cols = 0
        #loops through the table to find all table rows
        for row in table.find_all('tr'):
            #for each row finds all table headers and data
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            #appends all data to our table_data list
            table_data.append(row_data)
            #sets max columns to the maximum number of columns for any single row
            max_cols = max(max_cols, len(row_data))

        #checks if table data does not have headers
        if not table_data[0]:
            #pulls from row 2 on
            table_data = table_data[1:]

        #checks if there is table data
        if table_data:
            #adds a blank into any rows that don't match the max number of columns
            for i, row in enumerate(table_data):
                table_data[i] = row + [''] * (max_cols - len(row))
        
        
    #convert our table into a data frame
    df1 = pd.DataFrame(table_data[1:], columns=table_data[0])
        
    time.sleep(request_delay) 
    #print the table (not really needed)
    #print(df1)

    #send the data to a csv
    #df.to_csv('Documents/2023.csv')



#add headers to df
headers = ['Season', 'Lg', 'Player','Voting','Age','Tm','G','MP','PTS',
           'TRB','AST','STL','BLK','FG%','3P%','FT%','WS','WS/48']


df1.columns = headers

#drop first row as it is blank
df1 = df1.drop(0)

#creating merge field for later
df1['year_start'] = df1['Season'].str.slice(0, 2)
df1['year_end'] = df1['Season'].str.slice(-2)
df1['Year'] = df1['year_start'] + df1['year_end']
df1['Merge Field'] = df1['Year'].astype(str) + df1['Player']


#SCRAPE SHOOTING STATS

#add your base url with curly braces where year will be inserted
base_URL = 'https://www.basketball-reference.com/leagues/NBA_{}_shooting.html'

#identify start and end years
start_year = 1998
end_year = 2023

#create empty list
dfs = []

#Loop through every year
for year in range(start_year, end_year + 1):

    url = base_URL.format(year)

    res = requests.get(url)
    
    #checking if successful request
    if res.status_code == 200:

        #uses beautiful soup to pull in content and find table
        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find('table', {'class': 'sortable'})
        
        #checks if a table is found
        if table:
            #creates empty list to hold our data
            table_data = []
            #find all <tr> elements in the table and iterate through them
            for row in table.find_all('tr'):
                #for each row find all <th> and <td> elements
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['th' and 'td'])]
                #append row data into our table_data list
                table_data.append(row_data)
                
            #check if there is table data
            if table_data:

                #checking for headers
                if table_data[0]:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])
                else:
                    df = pd.DataFrame(table_data)

                #adding year column
                df['Year'] = year

                #appending df to larger merged df created outside of loop
                dfs.append(df)

                #basketball-reference rate limits ips that make more than 20 bot requests in a minute so this delay avoids that
                time.sleep(request_delay) 
                
# Concatenate all DataFrames into a single DataFrame
combined_df2 = pd.concat(dfs, ignore_index=True)

# Export the combined DataFrame to a CSV file (if you want just this data)
#combined_df.to_csv('basketballref_shooting_stats.csv', index=False)



#add headers to df
headers = ['Player','POS', 'AGE', 'TEAM', 'GP', 'MP', 'FG%', 'Dist','blank1', '% of Shots from 2PT', 
           '% of Shots from 0-3ft','% of Shots from 3-10ft','% of Shots from 10-16ft',
           '% of Shots from 16+ft', '% of Shots from 3PT', 'blank2',
           'FG% 2PT','FG% 0-3ft','FG% 3-10ft','FG% 10-16ft','FG% 16+ft','FG% 3PT', 'blank3',
           '% assisted 2PT Shots', '% assisted 3PT Shots', 'blank4','FG% Dunks', 'Count Dunks', 'blank5',
          '% of 3PT attempts from corner', 'Corner 3PT %', 'blank6', 'Heaves Attempted', 'Heaves Made','Year']

combined_df2.columns = headers

#remove empty rows on top
rows_to_remove = [0,1]

combined_df2 = combined_df2.drop(rows_to_remove)

#remove blank columns
columns_to_remove = ['blank1','blank2','blank3','blank4','blank5','blank6']

combined_df2 = combined_df2.drop(columns=columns_to_remove, axis=1)

#creating combined merge field for later merge
combined_df2['Merge Field'] = combined_df2['Player'] + combined_df2['POS'] + combined_df2['Year'].astype(str)

#create merged dataset
merged_df = pd.merge(df_final, combined_df2, on='Merge Field', how='left')


#remove and rename columns
columns_to_remove = ['POS_y','AGE_y','TEAM_y','GP_y','FG%_y','Year_y','Merge Field']

merged_df = merged_df.drop(columns=columns_to_remove, axis=1)

merged_df['PLAYER'] = merged_df['PLAYER'].str.rstrip('*')

merged_df = merged_df.rename(columns={'POS_x': 'POS', 'AGE_x':'AGE', 'TEAM_x':'TEAM', 'GP_x': 'GP', 'FG%_x': 'FG%', 'Year_x': 'Year'})

merged_df['Merge Field'] = merged_df['Year'].astype(str) + merged_df['PLAYER']

#creating final merged df with all 3 df
NBA_df = pd.merge(merged_df, df1, on='Merge Field', how='left')

#removing unnecessary columns
final_columns_to_remove = ['Merge Field','Lg','year_start','year_end', 'Year_y','MP_y','PTS_y','TRB_y','AST_y','STL_y','BLK_y','FG%_y','3P%_y','FT%_y','Player_x']

NBA_df = NBA_df.drop(columns=final_columns_to_remove, axis=1)

#rename some columns
NBA_df = NBA_df.rename(columns={ 'FG%_x':'FG%', 'Year_x':'Year', '3P%_x':'3P%', 'TRB_x': 'TRB', 'FT%_x': 'FT%', 'AST_x': 'AST', 'STL_x': 'STL','BLK_x': 'BLK', 'PTS_x': 'PTS','MP_x':'MP','Player_y':'MVP Name'})
#shows df
NBA_df

#exporting to csv in documents folder
NBA_df.to_csv('Documents/HistoricalNBADataFinal_.csv', index=False)





