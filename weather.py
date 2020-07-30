import requests
import config


cities = {'москв': 'moscow', 'петер': 'saint petersburg', 'питер': 'saint petersburg', 'химк': 'khimki',
          'мытищ': 'mytishchi', 'лондон': 'london', 'париж': 'paris', 'нью йорк': 'new york city',
          'лос анджелес': 'los angeles', 'киев': 'kyiv', 'минск': 'minsk', 'токио': 'tokyo',
          'одинцов': 'odintsovo'}


clothes_by_weather = {'-25': 'Не забудте ресничный очиститель)',
                      '-20': 'Стоит подумать о второй куртке)',
                      '-15': 'Я бы надел свитер.',
                      '-10': 'Как насчет шарфика?',
                      '-5': 'Не забудь перчатки!',
                      '-1': 'Зимняя обувь ждет тебя',
                      '0': 'Ух... тут даже вода не может определиться с состоянием, '
                           'а ты меня спрашиваешь что тебе надеть',
                      '5': 'Прохладненько, одевайся теплее',
                      '10': 'Неплохая температура, не забудь ветровку, вдруг похолодает',
                      '15': 'Красота, футболка и легкие брючки ждут тебя',
                      '20': 'Идеально, можно надеть шорты',
                      '25': 'Все просто: майка, шорты, шлепки',
                      '30': 'Уф, жарковато, возьми с собой кондиционер'}

translator = {'city not found': 'Упс, такого города нет...',
              'clear': 'без облаков',
              'clouds': 'облачно',
              'snow': 'снег',
              'rain': 'дождь',
              'drizzle': 'изморозь'}

description = {'clear sky': 'чистое небо',
               'few clouds': 'мало облаков',
               'scattered clouds': 'рассеяные облака',
               'broken clouds': 'тучные облака',
               'overcast clouds': 'пасмурно',
               'light intensity shower rain': 'легкий дождь',
               'light intensity drizzle': 'легкий дождь',
               'light rain': 'легкий дождь',
               'moderate rain': 'умеренный дождь',
               'heavy shower snow': 'метель'}


degree_sign = u'\N{DEGREE SIGN}'


def take_umbrella(data):
    if data == 'дождь':
        return ' и не забудь взять зонт! Потом скажешь спасибо'
    else:
        return ''


def get_windy(data):
    if data < 2:
        return 'без ветра'
    elif data < 5:
        return 'ветренно'
    else:
        return 'сильный ветер'


def get_opinion(temperature):
    for key in clothes_by_weather:
        if temperature < int(key):
            return clothes_by_weather[key]
    return clothes_by_weather['30']


def check_city(message):
    words = message.split(' в ')
    if len(words) == 2:
        if 'погод' in words[0]:
            ind = 1
        elif 'погод' in words[1]:
            ind = 0
        else:
            return 'city not found'
        return words[ind]
    words = message.split(' ')
    if len(words) == 2:
        if 'погод' in words[0]:
            ind = 1
        elif 'погод' in words[1]:
            ind = 0
        else:
            return 'city not found'
        return words[ind]
    return 'error'


def get_city(city):
    result = ''
    for i in cities:
        if city.find(i) != -1:
            result = cities[i]
    if result != '':
        return result
    for i in cities:
        if cities[i].find(city) != -1:
            result = cities[i]
    if result != '':
        return result

    return 'city not found'


def transform_data(data):
    temp = round(int(data['main']['feels_like']) - 273)
    desc = description[data['weather'][0]['description']] if data['weather'][0]['description'] in description else ''
    wind = get_windy(data['wind']['speed'])
    main_weather = translator[data['weather'][0]['main'].lower()]
    answer = 'На улице ' + str(temp) + degree_sign + 'C, ' + main_weather + ', ' + desc + ', '\
             + wind + '. ' + get_opinion(temp) + take_umbrella(main_weather)
    return answer


def get_weather(message):
    city = check_city(message)
    if city == 'city not found':
        return 'Прости, я не смог найти город, может введешь его иначе?'
    elif city == 'error':
        return 'Упс... ошибка, надо починить себя'

    city = get_city(city)
    if city == 'city not found':
        return 'Прости, я не смог найти город, может введешь его иначе?'

    answer = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'
                          .format(city=city, token=config.TOKEN_WEATHER))
    res = answer.json()
    if res['cod'] == '404':
        return translator[res['message']]
    return transform_data(res)


def is_weather(message):
    return True if 'погод' in message or 'weather' in message else False
