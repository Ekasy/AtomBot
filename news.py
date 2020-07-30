import requests
import config

categories = {'спорт': 'sport', 'бизнесс': 'business', 'технолог': 'technology', 'политик': 'politics',
              'наук': 'science', 'музык': 'music', 'культур': 'culture', 'экономик': 'economic'}
tags = {'спорт': 'sport', 'бизнесс': 'business', 'ит': 'it', 'технолог': 'technology', 'политик': 'politics',
        'наук': 'science', 'футбол': 'football', 'маск': 'musk', 'путин': 'putin', 'трамп': 'trump',
        'гугл': 'google', 'банк': 'bank', 'музык': 'music', 'росси': 'russia', 'сша': 'usa', 'америк': 'usa',
        'москв': 'moscow', 'культур': 'culture', 'экономика': 'economic'}
eng_tags = ['sport', 'business', 'it', 'technology', 'politics', 'science', 'football', 'musk', 'putin', 'trump',
            'google', 'bank', 'music', 'russia', 'moscow', 'usa', 'economic', 'culture']
eng_letter = ['a', 'e', 'i', 'o', 'u', 'y']


def is_news(message):
    return True if ('новост' in message.lower()) or ('new' in message.lower()) else False


def get_news_by_tag(tag):
    url = ''
    for letter in eng_letter:
        if letter in tag:
            for i in eng_tags:
                if tag.find(i) != -1:
                    tag = i
                    url = 'https://newsapi.org/v2/top-headlines?language=en&q={category}&apiKey={API_KEY}' \
                        .format(category=tag, API_KEY=config.TOKEN_NEWS)

    if url == '':
        for key in categories:
            if tag.find(key) != -1:
                tag = categories[key]
                url = 'https://newsapi.org/v2/top-headlines?country=ru&category={category}&apiKey={API_KEY}' \
                    .format(category=tag, API_KEY=config.TOKEN_NEWS)

    if url == '':
        for key in tags:
            if tag.find(key) != -1:
                tag = tags[key]
                url = 'https://newsapi.org/v2/top-headlines?language=en&q={tag}&apiKey={API_KEY}' \
                    .format(tag=tag, API_KEY=config.TOKEN_NEWS)
    if url == '':
        return 'Странно, новостей с введенным тегом нет. Попробуйте ввести другой тег'
    req = requests.get(url)
    if req.json()['status'] == 'error':
        return 'Что-то пошло не так... Раньше такого не случалось, попробуйте позже'
    news = req.json()['articles']
    if not news:
        return 'Странно, новостей с введенным тегом нет. Попробуйте ввести другой тег'
    answer = 'Вот подборка самых популярных по тегу "{tag}":\n'.format(tag=tag)
    size = 10 if req.json()['totalResults'] > 10 else req.json()['totalResults']
    for i in range(0, size):
        answer += '{number}. {title} - {url}\n'.format(number=i + 1, title=news[i]['title'], url=news[i]['url'])
    return answer


def get_news(message):      # передается строка типа новости, новости спорта, новости спорт
    string_list = message.split(' ')
    q = ''
    for i in string_list:
        if not (i.find('новост') != -1 or i.find('new') != -1):
            q += i + ', '
    if q == '':
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey={API_KEY}'\
            .format(API_KEY=config.TOKEN_NEWS)
        req = requests.get(url)
        if req.json()['status'] == 'error':
            return 'Что-то пошло не так... Раньше такого не случалось, попробуйте позже'
        news = req.json()['articles']
        if not news:
            return 'Странно, новостей с введенным тегом нет. Попробуйте ввести другой тег'
        answer = 'Вот подборка самых популярных:\n'
        size = 10 if req.json()['totalResults'] > 10 else req.json()['totalResults']
        for i in range(0, size):
            answer += '{number}. {title} - {url}\n'.format(number=i+1, title=news[i]['title'], url=news[i]['url'])
        return answer
    else:
        q = q[:-2]
        return get_news_by_tag(q)


# print(get_news('q'))
