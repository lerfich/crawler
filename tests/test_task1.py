from task1 import parseTagsTexts


weatherUrl = "https://yandex.com.am/weather/?lat=46.20832443&lon=6.142743111" #погода в Женеве
vkSpbuUrl = "https://vk.com/spb1724" #группа спбгу вк

weatherStyleClass = "link__condition day-anchor i-bem" #стиль для тега, содержащего температуру (число)
vkSpbuStyleClass = "wall_post_text" #стиль для тега, содержащего пост

weatherHtmlTag = "div" #типа тега для сайта погоды
vkSpbuHtmlTag = "div" #тип тега для вк


def test_nothing():
    assert parseTagsTexts(weatherUrl, "", "") == []
    assert parseTagsTexts(vkSpbuUrl, "", "") == []


def test_matching_values():
    weather_result = parseTagsTexts(weatherUrl, weatherStyleClass, weatherHtmlTag)
    assert weather_result[0] == "Пасмурно"
    vk_result = parseTagsTexts(vkSpbuUrl, vkSpbuStyleClass, vkSpbuHtmlTag)
    assert vk_result[0] == "В #СПбГУ наградили победителей регионального этапа Всероссийской олимпиады школьников и их педагогов: https://vk.cc/cn6c3d." + \
                           "Концерт, медали, благодарственные письма от губернатора и поздравления от руководства комитета по образованию и Университета — " + \
                           "большой и заслуженный праздник для тех, кто ставит знания на первое место!"
    
def test_number():
    weather_result = parseTagsTexts(weatherUrl, weatherStyleClass, weatherHtmlTag)
    assert len(weather_result) == 1


def test_dynamic_number():
    vk_result = parseTagsTexts(vkSpbuUrl, vkSpbuStyleClass, vkSpbuHtmlTag)
    assert len(vk_result) != 23113