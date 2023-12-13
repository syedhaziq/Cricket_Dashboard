from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
import numpy as np
import time


def player_info():
    url = "https://www.espncricinfo.com/series/icc-cricket-world-cup-2023-24-1367856/pakistan-squad-1399493/series-squads"
    #HEADERS = ({'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(url)

    web_content = BeautifulSoup(webpage.content, "html.parser")

    ### Team parsing ####
    team = web_content.find_all("span", attrs={'class':'ds-text-title-xs ds-font-bold ds-text-typo'})
    team_name = team[1].text
    print(team_name)


    #### team year parsing ###

    year = web_content.find_all("span", attrs={'class':'ds-text-compact-xs ds-text-typo-mid3'})
    year = year[0].text.split("|")[0]

    ########################## parsing players Information  ########################

            ###########loop over array to get all the players ###################
    list_of_players = web_content.find_all("div", attrs={'class':'ds-grid lg:ds-grid-cols-2'})


    stats_dict = {'team':[],
                'year':[],
                'player names':[],
                'category':[],
                'Age':[]}
    
    players_image = {'player names':[],
                     'img link':[]}

    #print(list_of_players)

    for i in range(len(list_of_players)):
        players_list = list_of_players[i].find_all("span", attrs={'class':'ds-text-compact-s ds-font-bold ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer'})
    

        ############## Parsing Name and Category ###################
        for j in range(len(players_list)):
            player_names =list_of_players[i].find_all("span", attrs={'class':'ds-text-compact-s ds-font-bold ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer'})[j].text
            player_category =list_of_players[i].find_all("p", attrs={'ds-text-tight-s ds-font-regular ds-mb-2 ds-mt-1'})[j].text
            player_age =list_of_players[i].find_all("span", attrs={'ds-text-compact-xxs ds-font-bold'})[j].text
            #print(player_names)
            stats_dict['player names'].append(player_names)
            stats_dict['category'].append(player_category)

        ############# Parsing Age ###########################
        player_age = list_of_players[i].find_all("span", attrs={'ds-text-compact-xxs ds-font-bold'})
        
        for k in range(len(player_age)):
            try:
                
                age = int(list_of_players[i].find_all("span", attrs={'ds-text-compact-xxs ds-font-bold'})[k].text.split('y')[0])
                #print(age)
                stats_dict['Age'].append(age)
            except:
                pass

    
    ##################### Parsing player's Image link ##################################
    url = "https://www.pcb.com.pk/pakistan-ODI-team.html"
    #HEADERS = ({'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(url)

    web_content = BeautifulSoup(webpage.content, "html.parser")

    players_link  = len(web_content.find_all("div", attrs = {'class':'row-fluid'})[0].find_all("a")) - 15
    print(players_link-15)
    for l in range(0,players_link, 2):
        #print(l)
        pictures = web_content.find_all("div", attrs = {'class':'row-fluid'})[0].find_all("a")[l].find('img').get('src').split('/',1)[1]
        picture_link = 'www.pcb.com.pk/'+str(pictures)
        player_name = web_content.find_all("div", attrs = {'class':'row-fluid'})[0].find_all("a")[l].find('img').get('alt')
        players_image['player names'].append(player_name)
        players_image['img link'].append(picture_link)



    ####################### Adding Team name and Announce Date #########################
    for key, value in stats_dict.items():
        #print value
        count = len([item for item in value if item])
        team_list = [team_name]*count
        year_list = [year]*count
        stats_dict['team'] = team_list
        stats_dict['year'] = year_list

        if value == 'player name':
            break
    
    stats_df = pd.DataFrame.from_dict(stats_dict)
    images_df = pd.DataFrame.from_dict(players_image)
    stats_df.to_csv('Players_info')
    images_df.to_csv('Players_img')


    return stats_dict,players_image

dicts, img = player_info()

print(img)
