import httplib2
from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
import httplib2
import matplotlib.pyplot as plt
import time
from glom import glom

# from vk_token import accessToken
access_token = "vk1..kak7aByTPqIBYnAMBYSK3P1f5DHYf9YA2hL0Ftjo9vBNK6COY2v92Hyrzo_GHgPjwUw_84n4Doi87ie2Zr4KI54ZODgqAzDPdht86I5fnF5fkfaQYAArjvk5LYcaer6cYVhtCSjANHtCN4iuaLzyErSBfxZQySEIUjyW40kIuzXBbtX6ehZDz-zY5w0WYf48Q-gjpTaUZeg7b_0_PPAyTg"

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
def WordMentions(allPosts, wordToSearch):
    def TimesWordMentioned(docs, word):
        count = 0
        for doc in docs:
            if (doc.upper().count(word.upper())):
                count += 1
        return count
    allPostsTexts = [post['text'] for post in allPosts]
    return TimesWordMentioned(allPostsTexts, wordToSearch)


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
        'comments': glom(post, 'comments.count', default=0),
        'views': glom(post, 'views.count', default=0),
        'likes': glom(post, 'likes.count', default=0),
        'reposts': glom(post, 'reposts.count', default=0),
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


def PostsFrequencyGraph(allPosts, university):
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
    # plt.locator_params(nbins=10)
    plt.title(f'Частота публикаций за собираемый период в {university}', fontsize=15, color="blue")
    plt.xticks(rotation=45)
    plt.show()

def vkPostsParser(count, vkGroupId, folderName):
    vk_links = []
    allPosts = []
    allComments = []
    for i in range(0, count):
        if (i == 0):
            vk_links.append(f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vkGroupId}&count=100")
        else:
            vk_links.append(f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vkGroupId}&count=100&offset={i*100}")

    http = httplib2.Http()
    for link in vk_links:
        res = http.request(link, method='POST', 
                        headers={'Authorization': f'Bearer {access_token}'})

        lastPosts = json.loads(res[1])
        lastPosts = lastPosts['response']['items']
        for lastPost in lastPosts:
            allPosts.append(lastPost)

            getPostCommentUrl = f"https://api.vk.com/method/wall.getComments?v=5.131&owner_id=-{vkGroupId}&post_id={lastPost['id']}"
            res = http.request(getPostCommentUrl, method='POST', 
                               headers={'Authorization': f'Bearer {access_token}'})
        
            # print(len(json.loads(res[1])['response']['items']))
            allCommentsFromPost = json.loads(res[1])['response']['items']

            if (len(allCommentsFromPost) > 0):
                # print(allComments)
                for comment in allCommentsFromPost:
                    allComments.append(comment['text'])
            time.sleep(0.5)
            

    # print(len(allComments))

    a_file = open(f"./results/{folderName}.json", "w")
    json.dump(allComments, a_file)
    a_file.close()

    b_file = open(f"./results/{folderName}_posts.json", "w")
    json.dump(allPosts, b_file)
    b_file.close()

    # return allPosts       
                    

#WEB 1.0
# NumberOfPages()
# # NumberOfErrorLinks() #работает около 5 минут, проходит по всем страницам
# NumberOfExternalLinks()
# NumberOfInternalSubDomensLinks()
# NumberOfDownloadableLinks()

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
def stats_web2(postsCount):
    vkGroupId_spbu = 58219172 #подслушано СПБГУ 28к
    vkGroupId_msu = 54295855 #подслушано МГУ 82к

    # urlForWeb_2_0 = f"https://api.vk.com/method/wall.getComments?v=5.131&owner_id=-{vk_group_id_msu}&post_id=445788"
    # http = httplib2.Http()


    # res = http.request(urlForWeb_2_0, method='POST', 
    #                 headers={'Authorization': f'Bearer {access_token}'})

    # allPosts = json.loads(res[1])
    # newPosts = allPosts['response']['items']
    # print(newPosts)
    # a_file = open("./results/posts.json", "w")
    # json.dump(newPosts, a_file)
    # a_file.close()

    with open('./results/spbu_comments.json') as json_file:
        spbu_comments_less = json.load(json_file)  
    with open('./results/msu_comments.json') as json_file:
        msu_comments_less = json.load(json_file)          


    with open('./results/msu_posts.json') as json_file:
        msu_posts = json.load(json_file)
    with open('./results/msu.json') as json_file:
        msu_comments = json.load(json_file)
    with open('./results/spbu_posts.json') as json_file:
        spbu_posts = json.load(json_file)
    with open('./results/spbu.json') as json_file:
        spbu_comments = json.load(json_file)  

    print(f'Всего постов: {len(msu_posts)}. Всего комментариев в группе СПБГУ: {len(spbu_comments)}, в группе МГУ: {len(msu_comments)}')          

 
    # vkPostsParser(postsCount // 100, vkGroupId_msu, 'msu')
    # vkPostsParser(postsCount // 100, vkGroupId_spbu, 'spbu')

    #WEB 2.0

    spbu_word_mention_in_posts = WordMentions(spbu_posts, 'спбгу')
    print(f"Количество упоминаний слова СПБГУ {spbu_word_mention_in_posts} в постах")
    msu_word_mention_in_posts = WordMentions(msu_posts, 'мгу')
    print(f"Количество упоминаний слова МГУ {msu_word_mention_in_posts} в постах")



    spbu_word_mention_in_comments = WordMentions([{'text': comment} for comment in spbu_comments], 'спбгу')
    print(f"Количество упоминаний слова СПБГУ {spbu_word_mention_in_comments} в комментариях")
    msu_word_mention_in_comments = WordMentions([{'text': comment} for comment in msu_comments], 'мгу')
    print(f"Количество упоминаний слова МГУ {msu_word_mention_in_comments} в комментариях")



    #за 8000 постов
    unique_spbu_commentators = NumberOfUniquePublishers(spbu_comments_less)
    print(f"Количество уникальных пользователей в комментариях СПБГУ, публикующих контент {unique_spbu_commentators} (8000 постов, {len(spbu_comments_less)} комментариев)") 
    unique_msu_commentators = NumberOfUniquePublishers(msu_comments_less)
    print(f"Количество уникальных пользователей в комментариях МГУ, публикующих контент {unique_msu_commentators} (8000 постов, {len(msu_comments_less)} комментариев)") 

    # print(spbu_posts[0])
    comments, views, likes, reposts = ReactionsStatistics(spbu_posts)
    print(f"Статистика за последние {len(spbu_posts)} постов в группе СПБГУ \n 'comments': {comments} \n 'views': {views} \n 'likes': {likes} \n 'reposts': {reposts}")
    comments, views, likes, reposts = ReactionsStatistics(msu_posts)
    print(f"Статистика за последние {len(msu_posts)} постов в группе МГУ \n 'comments': {comments} \n 'views': {views} \n 'likes': {likes} \n 'reposts': {reposts}")

    print(datetime.datetime.fromtimestamp(spbu_posts[14999]['date']).strftime("%Y/%m/%d <- начало сбора СПБГУ"))
    print(datetime.datetime.fromtimestamp(spbu_posts[0]['date']).strftime("%Y/%m/%d <- конец сбора СПБГУ"))
    print(datetime.datetime.fromtimestamp(msu_posts[14999]['date']).strftime("%Y/%m/%d <- начало сбора МГУ"))
    print(datetime.datetime.fromtimestamp(msu_posts[0]['date']).strftime("%Y/%m/%d <- конец сбора МГУ"))

    PostsFrequencyGraph(spbu_posts, 'СПБГУ')
    PostsFrequencyGraph(msu_posts, 'МГУ')
    


if __name__ == "__main__":
    stats_web2(15000)
