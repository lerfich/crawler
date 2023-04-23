import re

from task2 import getDocs
from task1 import parseTagsTexts
from vk_token import accessToken


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def remove_smth(data):
    r = re.compile("\[\w+\|(.+?)\]", re.UNICODE)
    search_res = re.search(r, data)
    while search_res:
        data = re.sub(r, search_res.group(1), data, count=1)
        search_res = re.search(r, data)
    return data


url10 = "https://vk.com/spb1724"

countPostsToFetch = 10
vkGroupId = '52298374' 
url20 = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vkGroupId}&count={countPostsToFetch}"


def test_compare():
    res10 = parseTagsTexts(url10, "wall_post_text", "div")
    res10 = map(lambda x: x.replace('\n', ''), res10)
    res10 = map(lambda x: x.replace(' ', ''), res10)
    # При использовании WEB 1.0 краулера в текст добавляется надпись "Показать ещё" в середину текста
    res10 = map(lambda x: x.replace('Показатьещё', ''), res10)
    res20 = getDocs(accessToken, url20)
    res20 = map(lambda x: x.replace('\n', ''), res20)
    res20 = map(lambda x: x.replace(' ', ''), res20)
    # API сохраняет эмодзи
    res20 = map(remove_emojis, res20)
    # API Позволяет получить ссылки на другие группы, указанные в тексте
    res20 = map(remove_smth, res20)
    for elem10, elem20 in zip(res10, res20):
        assert elem10 == elem20
