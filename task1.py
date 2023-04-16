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
    return [tag.text for tag in tags]


# Вывод погоды
def print_weather():
    urlDefault = "https://yandex.com.am/weather/?lat=46.20832443&lon=6.142743111" #погода в Женеве
    styleClass = "temp__value temp__value_with-unit" #стиль для тега, содержащего температуру (число)
    htmlTag = 'span' #типа тега для сайта погоды
    weather_info = parseTagsTexts(urlDefault, styleClass, htmlTag)
    print("Погода в Женеве сейчас: ", weather_info[1])


# Вывод ВК
def print_vk():
    vkSpbuUrl = "https://vk.com/spb1724" #группа спбгу вк
    vkSpbuStyleClass = "wall_post_text" #стиль для тега, содержащего пост
    vkSpbuHtmlTag = 'div' #тип тега для вк
    vk_info = parseTagsTexts(vkSpbuUrl, vkSpbuStyleClass, vkSpbuHtmlTag)
    print(vk_info[0], '\n\n ############################## \n\n Последний пост в группе Спбгу ВК (https://vk.com/spb1724)')


if __name__ == "__main__":
    # print_weather()
    print_vk()
