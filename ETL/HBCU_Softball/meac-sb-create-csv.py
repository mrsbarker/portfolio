#import modules
import re
import requests
from bs4 import BeautifulSoup

def list_to_csv(filename, aList):
    '''
    list_to_csv converts a list of strings to a comma separated values file
    :param filename: string representing desired filename with extension .csv
    :param aList: list of strings representing the csv lines
    :return: None
    ''' 
    #store file to the desired location
    rel_path = "./hbcu-softball/data/"+filename
    #open file in write mode
    with open(rel_path, "w") as file: 
        file.writelines(aList)
        file.close()
    return


def team_stats(year):
    '''
    team_stats gets the league's overall statistics from the MEAC softball website
    :param year: integer of four digits
    :return: None
    '''
    #save url with year of interest
    url = f"https://static.meacsports.com/custompages/stats/softball/{year}/lgteams.htm"
    #save response
    r = requests.get(url)
    #store all tables found in the response
    tables = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('table')
    #verify the page used tables in html code (earlier years did not)
    if len(tables) != 0:
        #loop through the overall statistics tables (hitting, pitching, fielding)
        for table in tables[1:6:2]:
            #create filename based on table and year
            filename = f'MEAC-{year}-{str.strip(table.find_all('td')[1].text).upper()}.csv'
            lstNew = []
            #loop through table's rows
            for row in table.find_all('tr'):
                #add cleaned data to list
                data = [str.strip(x.text) for x in row.find_all('td')]
                #create string for csv format
                strRow = ", ".join(data)+"\n"
                lstNew.append(strRow)
            #convert list to csv
            list_to_csv(filename, lstNew)
    else:
        #store overall statistics as text since tables not present
        txt = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('font')[2].text
        #split text into the hitting, pitching, fielding tables
        tables = re.split(r"\(.+\)", txt)
        for table in tables:
            #split lines capturing newline pattern
            lst = [x for x in re.split(r"(?:\r*)\n+", table) if x] 
            #store index for line indicating the start of specialty rows
            idx = [id for id, s in enumerate(lst) if 'Totals' in s][0]
            #add cleaned data to list
            keep = [x for x in lst if lst.index(x) < idx]
            #save header in csv format
            keep[0] = re.sub(r"\s+", ",", str.strip(lst[0]))
            #create filename based on table and year
            filename = f'MEAC-{year}-{re.split(",", keep[0])[1]}.csv' 
            #replace spaces with commas for csv format
            data = [re.sub(r"\s+(?=[^a-zA-Z])", ",", str.strip(line))+"\n" for line in keep]
            #convert list to csv
            list_to_csv(filename, data) 
    return

#save csv files for years of interest
[team_stats(year) for year in range(2013, 2014)] 