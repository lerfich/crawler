
import pytest

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
    assert vk_result[0] == "#ФотоархивСПбГУ  Императорский Университет, 1898 год."
    
def test_number():
    weather_result = parseTagsTexts(weatherUrl, weatherStyleClass, weatherHtmlTag)
    assert len(weather_result) == 1


@pytest.mark.xfail
def test_dynamic_number():
    vk_result = parseTagsTexts(vkSpbuUrl, vkSpbuStyleClass, vkSpbuHtmlTag)
    assert len(vk_result) == 23113