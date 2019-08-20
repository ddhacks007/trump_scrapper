import urllib.request
from inscriptis import get_text
import calendar
import re
import math
import numpy as np
import datetime

def scrap_it(url_name):
    url = url_name
    html = urllib.request.urlopen(url).read().decode('utf-8')
    return ' '.join(get_text(html).split())

def init_scrapper_info():
    return {'no_of_times_the_requested_word_occurs':0, 'no_of_times_year_month_day': {'day':{}, 'month': {}, 'year': {}}, 'number_of_words_occur': {'total_number_of_word_count': 0, 'word_frequency': {} } }

def clean_text(text):
    text = (re.sub(r"[^a-zA-Z0-9.]+", ' ', re.sub(r'\[.*?\]', '', text)))
    iterable = text.split(' ')
    while(True):
        if '' in iterable:
            iterable.remove('')
        elif '.' in iterable:
            iterable.remove('.')
        else:
            break
    return iterable

def check_word_exists(text, requested_word):
    return True if text.find(requested_word)>=0 else False

def update_requested_word_index(init_dict):
    init_dict['no_of_times_the_requested_word_occurs'] = init_dict['no_of_times_the_requested_word_occurs'] + 1
    
def update_word_count_index(init_dict, text):
    if text in init_dict['number_of_words_occur']['word_frequency'].keys():
        init_dict['number_of_words_occur']['word_frequency'][text] = init_dict['number_of_words_occur']['word_frequency'][text] + 1
        return 
    init_dict['number_of_words_occur']['word_frequency'][text] = 1

def init_month_names(number_of_months = 12):
    global month_names
    month_names = []
    for month in range(1, number_of_months+1):
        month_names.append([calendar.month_abbr[month].lower(), calendar.month_name[month].lower()])
    
def check_if_month(text):  
    global month_names
    for  month in month_names:
        if text in month:
            return True
    return False

def update_month_names(init_dict, month_name):
    if(month_name in init_dict['no_of_times_year_month_day']['month'].keys()):
        init_dict['no_of_times_year_month_day']['month'][month_name] = init_dict['no_of_times_year_month_day']['month'][month_name] + 1
        return
    init_dict['no_of_times_year_month_day']['month'][month_name] = 1
def number_of_digits(num):
    return math.floor(math.log(int(num), 10) + 1) if num>0 else 0
    
def check_if_year(text, min_year_threshold= 1000, max_year_threshold = datetime.datetime.now().year + 100):
    if text.isdigit():
        if (int(text)>=min_year_threshold and int(text) <= max_year_threshold):
            return True
    return False

def update_year(init_dict, year):
    if(year in init_dict['no_of_times_year_month_day']['year'].keys()):
        init_dict['no_of_times_year_month_day']['year'][year] = init_dict['no_of_times_year_month_day']['year'][year] + 1
        return
    init_dict['no_of_times_year_month_day']['year'][year] = 1

def check_if_day(day, previous_ptr, next_ptr):
    if day > 0 and day<=31:
        return True if(check_if_year(next_ptr) | check_if_year(previous_ptr) | check_if_month(next_ptr) | check_if_month(previous_ptr)) else False
    return False

def update_day(init_dict, day):
    if(day in init_dict['no_of_times_year_month_day']['day'].keys()):
        init_dict['no_of_times_year_month_day']['day'][day] = init_dict['no_of_times_year_month_day']['day'][day] + 1
        return
    init_dict['no_of_times_year_month_day']['day'][day] = 1

def calculate_params(init_dict, text, index, iterable):
    is_day_flag = 0
    if(check_word_exists(text, 'trump')):
        update_requested_word_index(init_dict)
    update_word_count_index(init_dict, text)
    if(check_if_month(text)):
            update_month_names(init_dict, text)
    if text.isdigit():
        if(check_if_year(text)):
            update_year(init_dict, int(text))
            return
        if(index == 0):
            if(check_if_day(int(text), iterable[index+1], iterable[index+2])):
                is_day_flag = 1   
        elif(index == len(iterable) -1):
            if(check_if_day(int(text), iterable[index-1], iterable[index-2])):
                is_day_flag = 1
        else:
            if(check_if_day(int(text), iterable[index-1], iterable[index+1])):
                is_day_flag = 1
        if(is_day_flag == 1):
            update_day(init_dict, int(text))
        
def find_the_required_params(init_dict, iterable):
    length_of_corpus = len(iterable)
    j=0
    for index, text in enumerate(iterable):
        text = text.replace('.', '') if (text[-1] == '.' or text[0] == '.') else text
        calculate_params(init_dict, text, index, iterable)
    init_dict['number_of_words_occur']['total_number_of_word_count'] = sum(init_dict['number_of_words_occur']['word_frequency'].values())
    return init_dict 

month_names = None
def runner_run(url_name):
    scrapped_text = scrap_it(url_name)
    init_dict = init_scrapper_info()
    month_names = init_month_names()
    return find_the_required_params(init_dict, clean_text(scrapped_text.lower()))

init_dict = runner_run('https://en.wikipedia.org/wiki/Donald_Trump')