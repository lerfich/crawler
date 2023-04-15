import json
import httplib2



#сюда нужно вставить свой токен желательно, инструкуция в файле get_access
access_token = "vk1.a.kak7aByTPqIBYnAMBYSK3P1f5DHYf9YA2hL0Ftjo9vBNK6COY2v92Hyrzo_GHgPjwUw_84n4Doi87ie2Zr4KI54ZODgqAzDPdht86I5fnF5fkfaQYAArjvk5LYcaer6cYVhtCSjANHtCN4iuaLzyErSBfxZQySEIUjyW40kIuzXBbtX6ehZDz-zY5w0WYf48Q-gjpTaUZeg7b_0_PPAyTg"


###### Вместо слова wordToSearch можно вставить любое слово, частоту которого ты хочешь узнать в последних countPostsToFetch постах
wordToSearch = 'спбгу'
countPostsToFetch = 20 #Максимум 100
vk_group_id = '52298374' 

get_spbu_vk_wall_url = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vk_group_id}&count={countPostsToFetch}"
http = httplib2.Http()
res = http.request(get_spbu_vk_wall_url, method='POST', 
                   headers={'Authorization': f'Bearer {access_token}'})


all_posts = json.loads(res[1])
all_posts = all_posts['response']['items']
texts = [post['text'] for post in all_posts]

def AverageCountWordInDocument(docs, word):
    avgCount = []
    for doc in docs:
        avgCount.append(doc.upper().count(word.upper()))
    return sum(avgCount)/len(docs)  


print(AverageCountWordInDocument(texts, wordToSearch), f'Частота употребления термина *{wordToSearch}* в последних {countPostsToFetch} постах оф. группы СПБГУ ВК')