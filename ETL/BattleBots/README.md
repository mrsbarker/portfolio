![image](https://github.com/mrsbarker/portfolio/assets/65389492/4be09262-2668-41d2-9bd8-65b6b6e3f374)
With a background in mechanical engineering, its no wonder I am entertained and intrigued by Battlebots! Teams of engineers and designers build robots with the express purpose of surviving ~2 minute matches. A robot can win via knockout or judge decision based on points earned in the match. 

### Purpose
Display familiarity with extract-transform-load method and various data analysis skills with interesting engineering-related data that spanned a number of years and existed on multiple webpages.

### Technology
Python is the language used in this project's associated files. Data was extracted from the battlebots [website](https://battlebots.com/robots/) using Python web-scraping libraries: Requests and BeautifulSoup4. In addition to the expected data cleaning, special consideration had to be made as each season had a unique roster of robots and some robots have been competing since 2015. The code had to ensure the same robot wasn't recorded twice and the stored information came from the bot's page from its latest season. Python library, Pandas, was essential in compiling all the robots' statistics for all their seasons of competition. After the initial data cleaning tables were uploaded to PostgresSQL database for further organization and analysis. 

Feel free to view the [code](battlebots.py) for additional details on how I extracted and transformed the data to suit this project!

### Results
The main product of this code is a SQL database of all the 2019-2022 team/robot information and match statistics. 
