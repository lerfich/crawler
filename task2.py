import json
import httplib2
from vk_token import accessToken


def averageCountWordInDocument(docs, word):
    avgCount = []
    for doc in docs:
        avgCount.append(doc.upper().count(word.upper()))
    return sum(avgCount)/len(docs)


def getDocs(accessToken, get_spbu_vk_wall_url):
    http = httplib2.Http()
    res = http.request(get_spbu_vk_wall_url, method='POST', 
                    headers={'Authorization': f'Bearer {accessToken}'})

    all_posts = json.loads(res[1])
    all_posts = all_posts['response']['items']
    return [post['text'] for post in all_posts]


def print_vk():
    ###### Вместо слова wordToSearch можно вставить любое слово, частоту которого ты хочешь узнать в последних countPostsToFetch постах
    wordToSearch = 'спбгу'
    countPostsToFetch = 20 #Максимум 100
    vkGroupId = '52298374' 
    get_spbu_vk_wall_url = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vkGroupId}&count={countPostsToFetch}"
    docs = getDocs(accessToken, get_spbu_vk_wall_url)
    num = averageCountWordInDocument(docs, wordToSearch)
    print(num, f'Частота употребления термина *{wordToSearch}* в последних {countPostsToFetch} постах оф. группы СПБГУ ВК')


if __name__ == "__main__":
    print_vk()