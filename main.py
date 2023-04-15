from bs4 import BeautifulSoup
import requests
import httplib2
import vk_api
from selenium import webdriver
import json






#парсинг всех ссылок со страницы

# from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
# status, response = http.request(url)
# soup = BeautifulSoup(response, 'lxml')
    
# for a in soup.find_all('a', href=True):
#     print ("Found the URL:", a['href'])

# href_tags = soup.find_all(href=True)
# for a in href_tags:
#     print ("Found the URL:", a['href'])


access_token = "vk1.a.kak7aByTPqIBYnAMBYSK3P1f5DHYf9YA2hL0Ftjo9vBNK6COY2v92Hyrzo_GHgPjwUw_84n4Doi87ie2Zr4KI54ZODgqAzDPdht86I5fnF5fkfaQYAArjvk5LYcaer6cYVhtCSjANHtCN4iuaLzyErSBfxZQySEIUjyW40kIuzXBbtX6ehZDz-zY5w0WYf48Q-gjpTaUZeg7b_0_PPAyTg"

get_spbu_vk_wall_url = "https://api.vk.com/method/wall.get?v=5.131&owner_id=-52298374&count=98"
res = http.request(get_spbu_vk_wall_url, method='POST', 
                   headers={'Authorization': f'Bearer {access_token}'})


all_posts = json.loads(res[1])
all_posts = all_posts['response']['items']
texts = [post['text'] for post in all_posts]

def AverageCountWordInDocument(docs, word):
    avgCount = []
    for doc in docs:
        avgCount.append(doc.upper().count(word))
    return sum(avgCount)/len(docs)  

# print(AverageCountWordInDocument(texts, 'ВЫ'))

