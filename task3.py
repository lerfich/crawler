import httplib2
from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
import httplib2
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

from vk_token import accessToken


#WEB 1.0
def getAllLinksFromWebsite():
    with open('./results/data.json') as json_file:
        data = json.load(json_file)
    
    allLinks = []
    for key, value in data.items():
        # temp = [key, value]
        allLinks.append(key)
    return allLinks


def NumberOfPages(soup, ):
    websiteAllLinks = getAllLinksFromWebsite()  # здесь я получаю вообще все ссылки через поиск в ширину
    allClickableLinks = []  # здесь я получаю все ссылки только с первой страницы
    for link in soup.find_all('a', href=True):
        allClickableLinks.append(link['href']) 
    return len(websiteAllLinks)


def isPageNotFound(link, driver):
    try:
        # response = requests.get(link)
        # return False
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        if ('не найден' in visible_text.lower()):
            return True
        return False
    except:     
        return True
    

#Не советую запускать без надобности - кроулер будет просматривать все 1600 страниц (около 25 мин)
# def NumberOfErrorLinks():
#     notWorkingLinks = []
#     allClickableValidLinks = []
#     for link in allClickableLinks:
#         if (len(link.split('/')[0]) == 0):
#             allClickableValidLinks.append(urlForWeb_1_0 + link)
#         else:     
#             allClickableValidLinks.append(link)

#     for link in allClickableValidLinks:
#         if (isPageNotFound(link)):
#             notWorkingLinks.append(link)   
#     # print(notWorkingLinks)        
#     print(f'Количество неработающих ссылок {len(notWorkingLinks)}')
#     return len(notWorkingLinks)


def NumberOfExternalLinks(allClickableLinks):
    externalLinksList = []
    for link in allClickableLinks:
        if ('spbu.ru' not in link and '//' in link):
            externalLinksList.append(link) 
    return len(externalLinksList), len(set(externalLinksList))


def NumberOfInternalSubDomensLinks(allClickableLinks):
    internalDomens = []
    for link in allClickableLinks:
        if ('spbu' in link and 'http' in link):
            internalDomens.append(link.split('.ru')[0] + '.ru')    
    print(internalDomens)
    return len(set(internalDomens))


def NumberOfDownloadableLinks(websiteAllLinks):
    filesLinksList = []
    for link in websiteAllLinks:
        if ('.doc' in link[-5:] or '.pdf' in link[-5:] or '.docx' in link[-5:]):
            filesLinksList.append(link)
    print(filesLinksList)
    return len(set(filesLinksList))


#WEB 2.0
def WordMentions(allPosts):
    def TimesWordMentioned(docs, word):
        count = 0
        for doc in docs:
            if (doc.upper().count(word.upper())):
                count += 1
        return count
    allPostsTexts = [post['text'] for post in allPosts]
    return TimesWordMentioned(allPostsTexts, 'спбгу')


def NumberOfUniquePublishers(allPosts):
    postAuthorsList = []
    for post in allPosts:
        try:
            # В признавашках только подпись есть, публикуется от имени сообщества (но не всегда она есть)
            postAuthorsList.append(post['signer_id'])
        except: 
            postAuthorsList.append(post['from_id'])  
    return len(set(postAuthorsList))


def ReactionsStatistics(allPosts):
    configuredPosts = [{
        'comments': post['comments']['count'],
        'views': post['views']['count'],
        'likes': post['likes']['count'],
        'reposts': post['reposts']['count'],
        } for post in allPosts]

    comments = 0
    views = 0
    likes = 0
    reposts = 0
    for post in configuredPosts:
        comments += post['comments']
        views += post['views']
        likes += post['likes']
        reposts += post['reposts']  
    return comments, views, likes, reposts


def PostsFrequencyGraph(allPosts):
    allPostsWithDates = []
    for post in allPosts:
        allPostsWithDates.append(datetime.datetime.fromtimestamp(post['date']).strftime("%Y/%m/%d")) #, 'text': post['text']})
    counter = {} #добавил свой counter, потому что у дефолтного сортировка по наиболее частому по дефолту
    for date in allPostsWithDates[::-1]:
        if date in counter.keys():
            counter[date] += 1
        else:
            counter[date] = 1  
    plt.plot(counter.keys(), counter.values())
    plt.title('График количество публикаций в день за собираемый период')
    plt.xticks(rotation=70)
    plt.show()
    return


# Сбор статистики обработанных страниц для Веб 1.0: общее 
# количество страниц и всех ссылок, количество внутренних
# страниц, количество неработающих страниц, количество внутренних
# поддоменов, общее количество ссылок на внешние ресурсы, 
# количество уникальных внешних ресурсов, количество уникальных
# ссылок на файлы doc/docx/pdf. Статистика для Веб 2.0: 
# количество публикаций об упоминании университета, количество 
# публикующих контент пользователей, количество 
# лайков/просмотров/комментариев/репостов, график 
# количество публикаций в день за собираемый период. 


# Статистика SPBU.RU
def stats_web1():
    urlForWeb_1_0 = "https://spbu.ru"

    driver = webdriver.Chrome()
    driver.get(urlForWeb_1_0)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    websiteAllLinks = getAllLinksFromWebsite()  # здесь я получаю вообще все ссылки через поиск в ширину
    allClickableLinks = []  # здесь я получаю все ссылки только с первой страницы
    for link in soup.find_all('a', href=True):
        allClickableLinks.append(link['href'])

    #WEB 1.0
    # NumberOfPages(soup)
    print(f'Общее количество страниц: {NumberOfPages(soup)}')   
    # NumberOfErrorLinks() #работает около 5 минут, проходит по всем страницам
    external_non_unique, exetranl_unique = NumberOfExternalLinks(allClickableLinks)
    print(f'Общее количество ссылок на внешние ресурсы: {external_non_unique}') ### НЕУНИКАЛЬНЫЕ  
    print(f'Общее количество уникальных ссылок на внешние ресурсы: {exetranl_unique}') ### УНИКАЛЬНЫЕ 
    # NumberOfInternalSubDomensLinks(allClickableLinks)
    print(f'Количество уникальных внутренних поддоменов: {NumberOfInternalSubDomensLinks(allClickableLinks)}') 
    # NumberOfDownloadableLinks(websiteAllLinks)
    print(f'Количество файлов .pdf, .doc или .docx: {NumberOfDownloadableLinks(websiteAllLinks)}')


# Статистика ВК
def stats_web2():
    vk_group_id = 59518047 #признавашки
    urlForWeb_2_0 = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vk_group_id}&count=100"
    http = httplib2.Http()
    res = http.request(urlForWeb_2_0, method='POST', 
                    headers={'Authorization': f'Bearer {accessToken}'})

    allPosts = json.loads(res[1])
    allPosts = allPosts['response']['items']
    #WEB 2.0
    print(allPosts[0])
    # WordMentions(allPosts)
    print(f"Количество упоминаний слова Спбгу {WordMentions(allPosts)}")
    # NumberOfUniquePublishers(allPosts)
    print(f"Количество уникальных пользователей, публикующих контент {NumberOfUniquePublishers(allPosts)}")  
    comments, views, likes, reposts = ReactionsStatistics(allPosts)
    print(f"Статистика за последние 100 постов \n 'comments': {comments} \n 'views': {views} \n 'likes': {likes} \n 'reposts': {reposts}")
    # PostsFrequencyGraph(allPosts)


if __name__ == "__main__":
    stats_web1()
