import pytest

from task3 import NumberOfExternalLinks, NumberOfInternalSubDomensLinks, NumberOfDownloadableLinks, WordMentions, NumberOfUniquePublishers, ReactionsStatistics


lists_test_links = [
  [
  "https://www.spbu.ru/openuniversity/documents/52openuniversity/documents/", 
  "https://www.spbu.ru/postupayushchim/programms/magistraturapostupayushchim/",
  "'http://forum.spbu.ru"
  ],
  [
  "https://stackoverflow.com/questions/24507078/how-to-deal-with-certificates-using-selenium", 
  "https://yandex.ru/pogoda/geneva",
  "https://vk.com/spb1724"
  ],
  [
  "https://www.spbu.ru/postupayushchim/programms/magistraturapostupayushchim/",
  "https://yandex.ru/pogoda/geneva",
  "https://stackoverflow.com/questions/24507078/how-to-deal-with-certificates-using-selenium",
  "https://www.spbu.ru/openuniversity/documents/52openuniversity/documents/", 
  "https://yandex.ru/pogoda/geneva",
  "https://vk.com/spb1724",
  "https://www.spbu.ru/postupayushchim/programms/magistraturapostupayushchim/"
  ]
]

list_test_docs = [
  [
  {"text": "Как дела?", "signer_id": "Q", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}, 
  {"text": "Всем привет из спбгу", "from_id": "admin", "comments":{"count": 9}, "views":{"count": 90}, "likes":{"count": 40}, "reposts":{"count": 5}}, 
  {"text": "Спбубгот", "signer_id": "Q", "comments":{"count": 1}, "views":{"count": 45}, "likes":{"count": 10}, "reposts":{"count": 2}}
  ],
  [
  {"text": "Как дела?", "from_id": "admin", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}, 
  {"text": "Всем привет из спбгy", "from_id": "admin", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}, 
  {"text": "Спбубгот", "from_id": "admin", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}
  ],
  [
  {"text": "Как дела?", "signer_id": "Q", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}, 
  {"text": "Всем привет из спбгуспбгу", "signer_id": "w", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}, 
  {"text": "Спб\nгу СПБГУ", "signer_id": "e", "comments":{"count": 3}, "views":{"count": 10}, "likes":{"count": 1}, "reposts":{"count": 0}}
  ]
]


@pytest.mark.parametrize(
        "test_links, expected", 
        [(lists_test_links[0], (0, 0)), 
         (lists_test_links[1], (3, 3)),
         (lists_test_links[2], (4, 3))])
def test_NumberOfExternalLinks(test_links,expected):
  assert NumberOfExternalLinks(test_links) == expected


@pytest.mark.parametrize(
        "test_links, expected", 
        [(lists_test_links[0], 2), 
         (lists_test_links[1], 0),
         (lists_test_links[2], 1)])
def test_NumberOfInternalSubDomensLinks(test_links,expected):
  assert NumberOfInternalSubDomensLinks(test_links) == expected

@pytest.mark.parametrize(
        "test_links, expected", 
        [(lists_test_links[0], 0),
         (["https://www.spbu.ru/300letsites/default/files/plan_300letspbu.pdf",
           "https://www.spbu.ru/universitet/podrazdeleniya-i-rukovodstvosites/default/files/2023-04/struktura_podchineniya_2023_0.doc",
           "https://www.spbu.ru/nauka/nacionalnyy-proekt-nauka-i-universitetysites/default/files/nauka_univers_booklet_2021_0.docx",
           "https://www.spbu.ru/nauka/nacionalnyy-proekt-nauka-i-universitetysites/default/files/nauka_univers_booklet_2021_0.pdf.zip"], 3)])
def test_NumberOfDownloadableLinks(test_links, expected):
  assert NumberOfDownloadableLinks(test_links) == expected


@pytest.mark.parametrize(
        "test_docs, expected", 
        [(list_test_docs[0], 1),
         (list_test_docs[1], 0),
         (list_test_docs[2], 2)])
def test_WordMentions(test_docs, expected):
  assert WordMentions(test_docs) == expected


@pytest.mark.parametrize(
        "test_docs, expected", 
        [(list_test_docs[0], 2),
         (list_test_docs[1], 1),
         (list_test_docs[2], 3)])
def test_NumberOfUniquePublishers(test_docs, expected):
  assert NumberOfUniquePublishers(test_docs) == expected


def test_ReactionsStatistics():
  assert ReactionsStatistics(list_test_docs[0]) == (13, 145, 51, 7)
