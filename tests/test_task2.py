import pytest

from task2 import getDocs, averageCountWordInDocument
from vk_token import accessToken


countPostsToFetch = 50 #Максимум 100
vkGroupId = '52298374' 
get_spbu_vk_wall_url = f"https://api.vk.com/method/wall.get?v=5.131&owner_id=-{vkGroupId}&count={countPostsToFetch}"

def test_getDocs_content():
    docs = getDocs(accessToken, get_spbu_vk_wall_url)
    assert "Императорский Университет, 1898 год." in docs[0]

def test_getDocs_number():
    docs = getDocs(accessToken, get_spbu_vk_wall_url)
    assert len(docs) == 50


@pytest.mark.parametrize("test_docs,test_word,expected", [([], "hello", 0), (["abba hello brother", "cat dog cow"], "car", 0)])
def test_averageCountWordInDocument_nothing(test_docs, test_word, expected):
    assert averageCountWordInDocument(test_docs, test_word) == expected


@pytest.mark.parametrize("test_docs,test_word,expected", [(["actor sailor number singer zip believer number", "visitor wallet eat turn"], "number", 1), 
                                                          (["actor sailor number singer zip believer number", "visitor wallet number eat turn"], "number", 1.5)])
def test_averageCountWordInDocument_match_values(test_docs, test_word, expected):
    assert abs(averageCountWordInDocument(test_docs, test_word) - expected) < 0.0001
