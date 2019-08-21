import urllib.request
from inscriptis import get_text
import re

def scrap_it(url_name):
    try:
        url = url_name
        html = urllib.request.urlopen(url).read().decode('utf-8')
        return ' '.join(get_text(html).split())
    except:
        print('Network inavailable please check yoour connection !!!')

def init_scrapper_info():
    return {'no_of_times_the_requested_word_occurs':0, 'no_of_times_year_month_day': {'day':{}, 'month': {}, 'year': {}}, 'number_of_words_occur': {'total_number_of_word_count': 0, 'word_frequency': {} } }

def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9.:]+", ' ', re.sub(r'\[[A-Z]+\]', '', re.sub(r'\[[0-9]+\]', '', text)))
    iterable = text.split(' ')
    for index, element in enumerate(iterable):
        x = re.sub(r"[^a-zA-Z0-9:]+", '', element)
        if len(x) <= 0:
            iterable.remove(element)
        else:
            iterable[index] = element.replace('.', '') if (element[-1] == '.' or element[0] == '.') else element
    return iterable
