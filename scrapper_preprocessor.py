import urllib.request
from inscriptis import get_text
import re

def scrap_it(url_name):
    try:
        url = url_name
        html = urllib.request.urlopen(url).read().decode('utf-8')
        return ' '.join(get_text(html).split())
    except ConnectionError:
        raise Exception('check your network connection!!')
    except:
        raise Exception('invalid url !')

def init_scrapper_info():
    return {'no_of_times_the_word_trump_occurs':0, 'total_month_year_day_occurence':0, 'month_year_day_occurence': {'day':{}, 'month': {}, 'year': {}}, 'total_number_of_words_occur': 0 }

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
