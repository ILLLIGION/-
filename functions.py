import requests
from bs4 import BeautifulSoup
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

from config import OWM_TOKEN

config_dict = get_default_config()
config_dict['language'] = 'RU'


def getweather(city):
    owm = OWM(OWM_TOKEN, config_dict)

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather

    curr_weather = [int(w.temperature('celsius')['temp_min']), int(w.temperature('celsius')['temp_max']),
                    int(w.temperature('celsius')['temp']), w.detailed_status]
    return curr_weather


def get_time(place):
    page = requests.get('https://www.google.com/search?client=firefox-b-d&q=time+in+' + place)
    soup = BeautifulSoup(page.text, "html.parser")
    parsed_time = soup.find_all('div', {'class': 'BNeawe iBp4i AP7Wnd'})[1].find_all(text=True, recursive=True)
    time = f'Время в {place}: {parsed_time[0]}'
    return time


def get_article():
    bbc_request = requests.get('https://www.bbc.com/news')
    soup = BeautifulSoup(bbc_request.text, "html.parser")
    raw_article = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find_all(
        text=True, recursive=True)
    if raw_article[0].startswith(
            'Video'):  # Cheking if article has video and then moving index by 1 for proper display in message
        topic = raw_article[5]
        title = raw_article[1]
        description = raw_article[2]
        publish_time = raw_article[4]
    else:
        topic = raw_article[4]
        title = raw_article[0]
        description = raw_article[1]
        publish_time = raw_article[3]
    href = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find('a', {
        'class': 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'})['href']
    link = f' https://www.bbc.com{href}'
    article = f'<b>Тема</b>: {topic}\n<b>Заголовок</b>: {title}\n<b>Краткое содержние</b>: ' \
              f'{description}\n<b>Опубликовано' \
              f'</b>: {publish_time}\n<b>Статья полностью</b>: {link} '
    return article