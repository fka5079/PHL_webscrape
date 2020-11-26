"""
Web Scraper Demo
Website: Doctor's Lounge'

@author: Fariha
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Extracting data from healthboards.com: a medical forum

url = 'https://www.doctorslounge.com/forums/viewforum.php?f=27&sid=022a9fa656df6d2dee50e512fb296006'
baseurl = 'https://www.doctorslounge.com/forums'

headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

posts = soup.find_all('div', class_ = 'list-inner')

postlinks = []
profilelinks = []

for item in posts:
    for link in item.find_all('a', href = True, class_ = 'topictitle'):
        postlinks.append(baseurl + (link['href'].lstrip('.')))

userposts = []
for link in postlinks:
    r = requests.get(link, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    
    # Within each post:
    post_count = soup.find('div', class_ = 'pagination').text.split('•')
    post_count = int(post_count[0].strip().rstrip(' posts'))
    
    user_IDs = []
    
    # For each reply/post on the main post
    for x in range(0, post_count):
        r = requests.get(link, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')
        
    
        post_date = soup.find('p', class_='author').text.split('»')
        post_topic = soup.find('h3', class_ = "first").text
        post_content = soup.select_one('div', class_ = 'content').text.split('Quote')
        user_stat = soup.find_all('dd', class_ = 'profile-rank')
        userID = post_content[x+1][15:40].split('»')
        user_IDs.append(userID[0])
        post_body = post_content[x+1].split('»' and 'Top')
        
        user_status = user_stat[x].text
        
        if user_status == "Guest":
            profile_link = soup.find_all('a', href = True, class_ = 'username')
        elif user_status == "Medical Doctor" or user_status == "Nurse":
            profile_link = soup.find_all('a', href = True, class_ = 'username-coloured')
        profilelinks.append(baseurl + profile_link[0]['href'].lstrip('.'))
        
        for lin in profilelinks:
            # Retrieve information from profile page
            r = requests.get(lin, headers = headers)
            soup = BeautifulSoup(r.content, 'lxml')
        
            user_details = soup.find_all('dd')
            user_join = user_details[len(user_details)-5]
            user_totalposts = user_details[len(user_details)-3]
            user_mostactive = user_details[len(user_details)-2]
            user_mostactivetopic = user_details[len(user_details)-1]
        
        data = {'Date': post_date[1],
                'No of Posts': post_count,
                'User ID': userID[0],
                'User Status': user_status,
                'Post Topic': post_topic,
                'Post': post_body[0],
                'User Age': user_details[2].text,
                'User Gender': user_details[4].text,
                'Date Joined': user_join.text,
                'Total Posts': user_totalposts.contents[0].rstrip(' |'),
                'Most Active Forum': user_mostactive.text.split('(')[0],
                'Most Active Topic': user_mostactivetopic.text.split('(')[0]}
        userposts.append(data)
        
        time.sleep(30)
    print('Completed 1 link')
    time.sleep(10)
    
data_df = pd.DataFrame(userposts)
data_csv = data_df.to_csv("Doctor's_Lounge_Data.csv", index = False)