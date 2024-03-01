#import modules
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def dict_to_csv(filename, aList):
        '''
        dict_to_csv converts a list of list to a comma separated values file
        :param filename: string representing desired filename with extension .csv
        :param aList: list of lists representing dataframe to be converted
        :return: None
        ''' 
        #store file to the desired location
        rel_path = "./battlebots/data/"+filename
        #create dataframe and convert to csv
        pd.DataFrame(aList).to_csv(rel_path, sep=';')
        return


def list_to_csv(filename, aList):
        '''
        list_to_csv converts a list of strings to a comma separated values file
        :param filename: string representing desired filename with extension .csv
        :param aList: list of strings representing the csv lines
        :return: None
        ''' 
        #store file to the desired location
        rel_path = "./battlebots/data/"+filename
        #open file in write mode
        with open(rel_path, "w") as file: 
            file.writelines(aList)
            file.close()
        return


def robot_links():
        '''
        robot_links returns all the battlebots from 2019-2021 and their respective links
        :return: dictionary with robot for key and most recent webpage for value
        ''' 
        #list comprehension of urls for seasons of interest
        urls = [f'https://battlebots.com/{year}-season-robots/' for year in [2021, 2020, 2019]]
        dict_links = {}
        #loop through season's url
        for url in urls:
            r = requests.get(url, verify=False)
            #store robot names to list
            html_robots = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('h4', {'class': 'title'})
            html_robots = [x.get_text().strip() for x in html_robots]
            #store associated link to list
            html_hrefs = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all(lambda tag: tag.name == 'a' and 'View' in tag.text)
            #update dictionary if robot name doesnt exist in later seasons
            [dict_links.update({x: [html_hrefs[html_robots.index(x)]['href']]}) for x in html_robots if re.search(re.split('\s(?=\()', x)[0], ';'.join(dict_links.keys())) is None]
        return dict_links
     
def remove_newlines(string):
        '''
        list_to_csv converts a list of strings to a comma separated values file
        :param filename: string representing desired filename with extension .csv
        :param aList: list of strings representing the csv lines
        :return: None
        ''' 
        #strip leading and trailing spaces
        string = string.strip()
        #replace newline between words with comma and space
        string = re.sub('(?<=\w)\n(?=\w)', ', ', string)
        #replace latin character with empty string
        string = re.sub('\xa0', '', string)
        return string

dict_links = robot_links()

lst_infos = []
df = pd.DataFrame(index=['Total matches', 'Win percentage', 'Total wins', 'Losses', 'Knockouts', 'KO percentage', 'Average knockout time', 'Knockouts against', 'KO against percentage', 'Judges decision wins'])

for i, v in dict_links.items():  
    r = requests.get(v[0], verify=False)
    #get robot info
    html_info = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('div',  {'class':'info-grid--item'})
    extracted = [remove_newlines(x.get_text()) for x in html_info] 
    #store bot and team info
    lst_infos.append(dict([re.split(':\n|[:]$', x) for x in extracted[2:-3]]))
    #get stat table aka html_tables[0]
    html_tables = BeautifulSoup(r.text.encode('utf-8'), features="html.parser").find_all('table')
    
    if html_tables != []:
        table_head = html_tables[0].find_all('th')
        clsses = [' '.join(f['class']) for f in table_head]
        #customize dataframe header for each robot to include bot's name
        headr = [x.get_text().lower() if table_head.index(x) == 0 else f'{re.split('\s\(',i)[0]}_{x.get_text().lower()}' for x in table_head]
        #create empty dataframe for robot with table header
        df_bot = pd.DataFrame(columns= headr) 
        #ensure code is only looking at match stats and not match history
        if headr[0] == 'stats':
            for i in html_tables[0].find_all('tr')[1:]:
                #store all the data for the current row
                row = [item.get_text() for c in clsses for item in i.find_all('td', attrs={'class': c})]
                df_row = pd.DataFrame([row], columns=headr) 
                #add current row dataframe to current robot dataframe
                df_bot = pd.concat([df_bot, df_row], ignore_index=True)
            df_bot.set_index('stats', drop=True, inplace=True)
        #add current robot dataframe to overall dataframe along the vertical axis
        df = pd.concat([df, df_bot], axis=1)
#create csvs from dataframes/dictionaries
df.to_csv('./battlebots/data/stat-history-all.csv')
dict_to_csv('robot-info.csv', lst_infos)
