import httplib2
from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
import httplib2
import matplotlib.pyplot as plt



###################################
###################################
print('\n\n\n---------------Статистика SPBU.RU: ---------------\n')
###################################
###################################


def getAllLinksFromWebsite():
    with open('./results/data.json') as json_file:
        data = json.load(json_file)
    
    allLinks = []
    for key, value in data.items():
        # temp = [key, value]
        allLinks.append(key)
    return allLinks


urlForWeb_1_0 = "https://spbu.ru"

driver = webdriver.Chrome()
driver.get(urlForWeb_1_0)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

websiteAllLinks = getAllLinksFromWebsite()  # здесь я получаю вообще все ссылки через поиск в ширину
allClickableLinks = []  # здесь я получаю все ссылки только с первой страницы
for link in soup.find_all('a', href=True):
    allClickableLinks.append(link['href'])

def NumberOfPages():
    websiteAllLinks = getAllLinksFromWebsite()  # здесь я получаю вообще все ссылки через поиск в ширину
    allClickableLinks = []  # здесь я получаю все ссылки только с первой страницы
    for link in soup.find_all('a', href=True):
        allClickableLinks.append(link['href'])
    # print(allClickableLinks)
    print(f'Общее количество страниц: {len(websiteAllLinks)}')   
    return len(websiteAllLinks)



def isPageNotFound(link):
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


def NumberOfExternalLinks():
    externalLinksList = []
    for link in allClickableLinks:
        if ('spbu.ru' not in link and '//' in link):
            externalLinksList.append(link) 
    # print(externalLinksList) ### НЕУНИКАЛЬНЫЕ 
    print(f'Общее количество ссылок на внешние ресурсы: {len(externalLinksList)}')  ### НЕУНИКАЛЬНЫЕ
    # print(set(externalLinksList)) ### УНИКАЛЬНЫЕ
    print(f'Общее количество уникальных ссылок на внешние ресурсы: {len(set(externalLinksList))}') ### УНИКАЛЬНЫЕ  
    return len(externalLinksList), len(set(externalLinksList))


def NumberOfInternalSubDomensLinks():
    internalDomens = []
    for link in allClickableLinks:
        if ('spbu' in link and 'http' in link):
            internalDomens.append(link.split('.ru')[0] + '.ru')
    # print(internalDomens)
    print(f'Количество уникальных внутренних поддоменов: {len(set(internalDomens))}')      
    return len(set(internalDomens))


def NumberOfDownloadableLinks():
    filesLinksList = []
    for link in websiteAllLinks:
        if ('.doc' in link or '.pdf' in link or '.docx' in link):
            filesLinksList.append(link)
    # print(set(filesLinksList))
    print(f'Количество файлов .pdf, .doc или .docx: {len(set(filesLinksList))}')
    return len(set(filesLinksList))


###################################
###################################
print('\n\n---------------Статистика ВК: ---------------\n')
###################################
###################################

#сюда нужно вставить свой токен желательно, инструкуция в файле get_access
access_token = "vk1.a.kak7aByTPqIBYnAMBYSK3P1f5DHYf9YA2hL0Ftjo9vBNK6COY2v92Hyrzo_GHgPjwUw_84n4Doi87ie2Zr4KI54ZODgqAzDPdht86I5fnF5fkfaQYAArjvk5LYcaer6cYVhtCSjANHtCN4iuaLzyErSBfxZQySEIUjyW40kIuzXBbtX6ehZDz-zY5w0WYf48Q-gjpTaUZeg7b_0_PPAyTg"

vk_group_id = 59518047 #признавашки
urlForWeb_2_0 = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vk_group_id}&count=100"
http = httplib2.Http()
res = http.request(urlForWeb_2_0, method='POST', 
                headers={'Authorization': f'Bearer {access_token}'})


allPosts = json.loads(res[1])
allPosts = allPosts['response']['items']


def WordMentions():
    def TimesWordMentioned(docs, word):
        count = 0
        for doc in docs:
            if (doc.upper().count(word.upper())):
                count += 1
        return count
    allPostsTexts = [post['text'] for post in allPosts]
    print(f"Количество упоминаний слова Спбгу {TimesWordMentioned(allPostsTexts, 'спбгу')}")
    return TimesWordMentioned(allPostsTexts, 'спбгу')

def NumberOfUniquePublishers():
    postAuthorsList = []
    for post in allPosts:
        try:
            # В признавашках только подпись есть, публикуется от имени сообщества (но не всегда она есть)
            postAuthorsList.append(post['signer_id'])
        except: 
            postAuthorsList.append(post['from_id'])  
    print(f"Количество уникальных пользователей, публикующих контент {len(set(postAuthorsList))}")  
    return len(set(postAuthorsList))

def ReactionsStatistics():
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
    print(f"Статистика за последние 100 постов \n 'comments': {comments} \n 'views': {views} \n 'likes': {likes} \n 'reposts': {reposts}")   
    return comments, views, likes, reposts


def PostsFrequencyGraph():
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
    plt.title('Частота публикаций за собираемый период', fontsize=15, color="blue")
    plt.xticks(rotation=45)
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

#WEB 1.0
# NumberOfPages()
# # NumberOfErrorLinks() #работает около 5 минут, проходит по всем страницам
# NumberOfExternalLinks()
# NumberOfInternalSubDomensLinks()
# NumberOfDownloadableLinks()

#WEB 2.0
WordMentions()
NumberOfUniquePublishers()
ReactionsStatistics()
PostsFrequencyGraph()
