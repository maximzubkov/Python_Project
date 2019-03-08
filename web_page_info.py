### TODO: потестить

import requests
from bs4 import BeautifulSoup

api_key = "trnsl.1.1.20190308T130505Z.54bc8184ebd6c2e8.87af28bd612e1abcccc8a24fd7f50bc587b05014"
yandex_translator_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"

def yandex_translater(text, lang = 'ru'):
    """
        Функция переводящая с занного языка на заданный параметром land язык, при этом если необходимо перевести слово 
        с английского на русский параметр lang необходимо задать как "en-ru"
    """
    url = yandex_translator_url + "?" + "key=" + api_key + "&" + "text=" + text + "&" + "lang=" + lang
    r = requests.get(url)
    return r.json()['text'][0]
    
def media_files_frequency(soup, media_type):
    """
        Количество встреченных медиа-файлов, media_type = [песни, видео, картинки...]
    """
    num = 0
    for i in soup.find_all(media_type):
        num += 1
    return num

def word_frequency(text, lang = "ru"):
    """
        Найдем 10 наиболее часто встречающихся слов и переведем их в случае необходимости на русский
    """
    for sep in " .,:;\'!?\"\}\{\(\)\[\]\^=@#": # убираем все разделители
        text = text.replace(sep, " ")
    text = text.split()
    d = dict()
    for word in text:
        if d.get(word) == None:
            d[word] = 1
        else:
            d[word] += 1
    sort = sorted(word_frequency(text).items(), key=lambda kv: -kv[1]) #минус означает сортировку по убыванию
    most_frequent_words = sort[0:10] # 10 наиболее часто встречащийся слов
    if lang != "ru":
        for i in range(len(most_frequent_words)):
            most_frequent_words[i] = yandex_translater(most_frequent_words[i], lang) 
            # TODO: оделать перевода по уже известному языку, полученному из html
    return most_frequent_words

def info_from_html(url, 
                   headers = {
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
                   }):
    """
        Функция, получающая иформация с веб-страницы, заданной url адресом, headers здесь параметр необходимый для того,
        чтобы сайты не посчитали наше преложение вирусным
    """
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ''.join(soup.findAll(text=True))
    # TODO: вытащить из html язык, на котором написана страница
    num_of_audio = media_files_frequency(soup, 'audio')
    num_of_video = media_files_frequency(soup, 'video')
    num_of_pics = media_files_frequency(soup, 'img')
    print(num_of_pics)
    
info_from_html('https://ru.wikipedia.org/wiki/Ассоциативный_массив')