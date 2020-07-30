from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests


def get_group(message):
    ls = message.split(' ')
    if len(ls) < 2:
        return 'Введите корректный запрос!'
    if 'расписан' in ls[0]:
        return ls[1]
    elif 'расписан' in ls[1]:
        return ls[0]
    return 'Введите корректный запрос!'


def get_path(group):
    page = requests.get("https://students.bmstu.ru/schedule/list")
    if page.status_code != 200:
        return 'проблемы с соединением'
    soup = BeautifulSoup(page.text, "html.parser")
    groups = soup.findAll(attrs={"class": "btn btn-sm btn-default text-nowrap"})
    for gr in groups:
        val = ''.join(gr.string.split())
        if val in group:
            return 'https://students.bmstu.ru' + gr['href']
    return 'группа не найдена'


def get_schedule(message):
    group = get_group(message.lower())
    if group == 'Введите корректный запрос!':
        return group
    source = get_path(group.upper())
    if source == 'проблемы с соединением' or source == 'группа не найдена':
        return source
    response = requests.get('https://mini.s-shot.ru/1920x0/PNG/1920/Z100/?' + source)
    if response.status_code != 200:
        return 'проблемы с соединением'
    img = Image.open(BytesIO(response.content))
    area = (300, 150, 1650, 1500)
    img = img.crop(area)
    bio = BytesIO()
    bio.name = message
    img.save(bio, 'PNG')
    bio.seek(0)
    # img.show()
    return bio


def is_schedule(message):
    return True if 'расписан' in message.lower() else False
