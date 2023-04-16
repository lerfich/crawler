from bs4 import BeautifulSoup
from selenium import webdriver



###################
# ЧТОБЫ ЗАПУСТИТЬ, ДОСТАТОЧНО РАЗКОММЕНТИРОВАТЬ ОДИН ИЗ ПРИНТОВ В САМОМ НИЗУ
###################

urlDefault = "https://yandex.com.am/weather/?lat=46.20832443&lon=6.142743111" #погода в Женеве
vkSpbuUrl = "https://vk.com/spb1724" #группа спбгу вк


styleClass = "temp__value temp__value_with-unit" #стиль для тега, содержащего температуру (число)
vkSpbuStyleClass = "wall_post_text" #стиль для тега, содержащего пост


htmlTag = 'span' #типа тега для сайта погоды
vkSpbuHtmlTag = 'div' #тип тега для вк


#парсинг значения определенного тега со страницы
def parseTagsTexts(url, styles, tag):
    driver = webdriver.Chrome()
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    tags = soup.findAll(tag, styles)
    # for tag in tags:
        # print(tag.text)
    return tags[1].text

# print(parseTagsTexts(vkSpbuUrl, vkSpbuStyleClass, vkSpbuHtmlTag), '\n\n ############################## \n\n Предпоследний пост в группе Спбгу ВК (https://vk.com/spb1724)')
print("Погода в Женеве сейчас: ", parseTagsTexts(urlDefault, styleClass, htmlTag))

