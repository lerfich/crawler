import httplib2
from bs4 import BeautifulSoup
import requests
import vk_api
from selenium import webdriver
import httplib2


urlForWeb_1_0 = "https://spbu.ru"
urlForWeb_2_0 = "https://spbu.ru"


driver = webdriver.Chrome()
driver.get(urlForWeb_1_0)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')



allClickableLinks = []
for link in soup.find_all('a', href=True):
    allClickableLinks.append(link['href'])
    # print("Found the URL:", link['href'])
# print(allClickableLinks)
# print(f'Количество ссылок: {len(allClickableLinks)}')   


externalLinksList = []
for link in allClickableLinks:
    if ('spbu.ru' not in link and '//' in link):
        externalLinksList.append(link) 
# print(externalLinksList) ### НЕУНИКАЛЬНЫЕ 
# print(f'Общее количество ссылок на внешние ресурсы: {len(externalLinksList)}')  ### НЕУНИКАЛЬНЫЕ
# print(set(externalLinksList)) ### УНИКАЛЬНЫЕ
# print(f'Общее количество уникальных ссылок на внешние ресурсы: {len(set(externalLinksList))}') ### УНИКАЛЬНЫЕ  
#     
# response = requests.get('http://www.example.com')

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


#Не советую запускать без надобности - кроулер будет просматривать все 306 страниц (около 5 мин)
# notWorkingLinks = []
# allClickableValidLinks = []
# for link in allClickableLinks:
#     if (len(link.split('/')[0]) == 0):
#         allClickableValidLinks.append(urlForWeb_1_0 + link)
#     else:     
#         allClickableValidLinks.append(link)

# for link in allClickableValidLinks:
#     if (isPageNotFound(link)):
#         notWorkingLinks.append(link)   
# print(notWorkingLinks)        
# print(f'Количество неработающих ссылок {len(notWorkingLinks)}')


internalDomens = []
for link in allClickableLinks:
    if ('spbu' in link and 'http' in link):
        internalDomens.append(link.split('.ru')[0] + '.ru')
# print(internalDomens)
# print(f'Количество уникальных внутренних поддоменов: {len(set(internalDomens))}')          


filesLinksList = []
for link in allClickableLinks:
    if ('.doc' in link or '.pdf' in link or '.docx' in link):
        filesLinksList.append(link)
# print(set(filesLinksList))
# print(f'Количество файлов .pdf, .doc или .docx: {len(set(filesLinksList))}')


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