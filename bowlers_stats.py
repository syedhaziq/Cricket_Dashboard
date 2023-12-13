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
import os
from player_info import player_info



def bowlers_stats():
    url = "https://www.espncricinfo.com/series/icc-cricket-world-cup-2023-24-1367856/pakistan-squad-1399493/series-squads"
    #HEADERS = ({'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(url)

    web_content = BeautifulSoup(webpage.content, "html.parser")

    list_of_players = web_content.find_all("div", attrs={'class':'ds-grid lg:ds-grid-cols-2'})

    ################################ importing player dictionary ###########################

    players_info, players_img  = player_info()



    ########################## Parsing Batters Stats ########################
    overall_batting_stats = pd.read_csv('overall_batting_stats')
    # all_rounder_stats = pd.DataFrame()
    overall_bowling_stats = pd.read_csv('overall_bowling_stats')
    Vs_team_stats_bowlers = pd.DataFrame()
    # Vs_team_T20I_Stats = pd.DataFrame()
    # Vs_team_Test_Stats = pd.DataFrame()
    #player_name_index = 0

    with open('index_carryforward.txt','r') as file:
        player_name_index = int(file.read())


    print(players_info)
    for i in range(2,3):
        players = list_of_players[i].find_all("a")
        
        for j in range(0,len(players),2):
            
            player_link = list_of_players[i].find_all("a")[j].get('href')
            link = "https://espncricinfo.com"+str(player_link)
            
            r = requests.get(link)
            df_list = pd.read_html(r.text)

            if i == 2 or str(player_link) == '/cricketers/mohammad-wasim-1185538':
                #print(i)
                batting_index = 1
                bowling_index = 0
            else:
                batting_index = 0
                bowling_index = 1

            print(player_name_index)
            print(players_info['player names'][player_name_index])
            temp_df_batting = df_list[batting_index]
            temp_df_batting['player_name'] = players_info['player names'][player_name_index]
            overall_batting_stats = pd.concat([overall_batting_stats,temp_df_batting],ignore_index=True)

            temp_df_bowling= df_list[bowling_index]
            temp_df_bowling['player_name'] = players_info['player names'][player_name_index]
            overall_bowling_stats = pd.concat([overall_bowling_stats,temp_df_bowling],ignore_index=True)

            print('##################### Batting and Bowling Stats have been parsed ############################')

            print('##################### Going for Granular Data #############################')

            try:
                driver = webdriver.Chrome()
                stats_link = link+'/bowling-batting-stats'
                # Open a website
                
                driver.get(stats_link)
                time.sleep(20)
                ####### closing pop up #################
                #time.sleep(15)
                element_xpath = "//*[@id='wzrk-cancel']"  # Replace with your XPath
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, element_xpath))
                ).click()
            
            
                time.sleep(5)
                # Now find the element using XPath with wait
                element_xpath = "//*[@id='main-container']/div[5]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/i"  # Replace with your XPath
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, element_xpath))
                )

                # Click on the found element
                element.click()

            ####### closing pop up #################
                # time.sleep(15)
                # element_xpath = "//*[@id='wzrk-cancel']"  # Replace with your XPath
                # element = WebDriverWait(driver, 15).until(
                #     EC.presence_of_element_located((By.XPATH, element_xpath))
                # ).click()

                page_source = driver.page_source

                print('######################################')
                
                soup = BeautifulSoup(page_source,'html.parser')

                check = soup.find_all("ul", attrs={'class':'ds-flex ds-flex-col ds-text-typo-mid2 ds-justify-center ds-overflow-ellipsis ds-max-h-8 ds-overflow-y-auto ds-w-full ds-grid ds-grid-cols-1 ds-items-center ds-gap-x-2 ds-max-h-96 ds-overflow-y-auto'})[0].find_all("span",attrs={'class':'ds-grow'})
                #check = check.find_all("li",attrs={'class':'ds-w-full ds-flex'})
                
                print('################# Format list has been parsed ################')

                time.sleep(5)
                # Now find the element using XPath with wait
                element_xpath = "//*[@id='main-container']/div[5]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/i"  # Replace with your XPath
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, element_xpath))
                )

                # Click on the found element
                element.click()

                print('##################################### Pulling granualar stats for each player #############################')
                


                

                for k in range(0,len(check)):
                    
                    k= k+1
                    # print(k)
                    

                    ####### clicking dropdown #################

                    time.sleep(5)
                    # Now find the element using XPath with wait
                    element_xpath = "//*[@id='main-container']/div[5]/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/i"  # Replace with your XPath
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, element_xpath))
                    ).click()

                    ####### Choosing options from dropdown #################

                    element_xpath = "//*[@id='tippy-13']/div/div/div/div/div/ul/li["+str(k)+"]"  # Replace with your XPath
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, element_xpath))
                    )
                    #//*[@id="wzrk-cancel"]
                    # Click on the found element
                    element.click()

                    time.sleep(5)

                    tables_source = driver.page_source
                    #print(tables)
                    #print(pd.read_html(tables_source)[1])

                    tables = pd.read_html(tables_source)

                    print('########################')
                
                    print('######################## Parsing for '+str(players_info['player names'][player_name_index])+' ################')
                    #print(check[k-1].text)
                    
                    temp_Vs_team_ODI_Stats = tables[1]
                    temp_Vs_team_ODI_Stats['player'] = players_info['player names'][player_name_index]
                    temp_Vs_team_ODI_Stats['format'] = check[k-1].text
                    Vs_team_stats_bowlers = pd.concat([temp_Vs_team_ODI_Stats,Vs_team_stats_bowlers],ignore_index=True)

                    ############## First three format (Test, ODI, T20I) ####################
                    if int(k) == 3:
                        break

                    
                
            finally:
                driver.quit()

            player_name_index = player_name_index+1
        
    print('################# Data has been parsed for each all rounder ###########')

    
    os.remove('index_carryforward.txt')

    Vs_team_stats_bowlers.to_csv('bowlers_stats', sep=',', index=False)
    overall_batting_stats.to_csv('overall_batting_stats', sep=',', index=False)
    overall_bowling_stats.to_csv('overall_bowling_stats', sep=',', index=False)
    return (Vs_team_stats_bowlers, player_name_index)

#stats, index = bowlers_stats()
#print(Vs_team_ODI_Stats.head())
