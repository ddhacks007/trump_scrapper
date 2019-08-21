import urllib.request
from inscriptis import get_text
import calendar
import re
import math
import numpy as np
import datetime
import sys
import os
import json

month_names = None

json_filename = sys.argv[1]
requested_url = sys.argv[2:][0]
print(json_filename)
print(requested_url)

def make_dir(folder_name):
    try:
        if folder_name not in os.listdir('.'):
            os.makedirs(folder_name+'/')
    except OSError as e:
            return 

def save_to_json(json_filename, init_dict, directory_name = 'json_results'):
    make_dir(directory_name)
    with open(directory_name +'/'+json_filename+'.json', 'w') as fp:
        json.dump(init_dict, fp)
        print('your requested_data is successfully_stored in ', directory_name +'/'+json_filename+'.json')
    
def scrap_it(url_name):
    url = url_name
    html = urllib.request.urlopen(url).read().decode('utf-8')
    return ' '.join(get_text(html).split())

def init_scrapper_info():
    return {'no_of_times_the_requested_word_occurs':0, 'no_of_times_year_month_day': {'day':{}, 'month': {}, 'year': {}}, 'number_of_words_occur': {'total_number_of_word_count': 0, 'word_frequency': {} } }

def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9.]+", ' ', re.sub(r'\[[A-Z]+\]', '', re.sub(r'\[[0-9]+\]', '', text)))
    iterable = text.split(' ')
    for index, element in enumerate(iterable):
        x = re.sub(r"[^a-zA-Z0-9]+", '', element)
        if len(x) <= 0:
            iterable.remove(element)
        else:
            iterable[index] = element.replace('.', '') if (element[-1] == '.' or element[0] == '.') else element
    return iterable


#requested word is trump
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

def get_month_abbr(text):
    global month_names
    for month in month_names:
        if text in month:
            return month[0]
        
    
def month_exists(iterable, index, threshold = 2):
    for i in range(index-1, index-threshold-1, -1):
        if(i>=0 and check_if_month(iterable[i])):
            return True
    for i in range(index+1, index+threshold+1):
        if(i<= len(iterable)-1 and check_if_month(iterable[i])):
            return True
    return False

def year_exists(iterable, index, threshold = 2):
    for i in range(index-1, index-threshold-1, -1):
        if(i>=0 and check_if_year(iterable[i], i, iterable)):
            return True
    for i in range(index+1, index+threshold+1):
        if(i<= len(iterable)-1 and check_if_year(iterable[i], i, iterable)):
            return True
    return False

def update_month_names(init_dict, month_name):
    if(month_name in init_dict['no_of_times_year_month_day']['month'].keys()):
        init_dict['no_of_times_year_month_day']['month'][month_name] = init_dict['no_of_times_year_month_day']['month'][month_name] + 1
        return
    init_dict['no_of_times_year_month_day']['month'][month_name] = 1
def number_of_digits(num):
    return math.floor(math.log(int(num), 10) + 1) if num>0 else 0
    
def check_if_year(text, index, iterable, min_year_threshold = 1000, max_year_threshold = datetime.datetime.now().year + 100):
    try:
        if((text[-1] == 's' and text[:-1].isdigit())):
            text = text[:-1]
        if(text.isdigit() and int(text)>=min_year_threshold and int(text) <= max_year_threshold):
            if ((month_exists(iterable, index)) | ((iterable[index-1] in  ['the', 'in', 'year']) | (iterable[index + 1] == 'elections')) ) :
                return True
        return False
    except:
        print(text, 'index', index)
        return False

def update_year(init_dict, year):
    if(year in init_dict['no_of_times_year_month_day']['year'].keys()):
        init_dict['no_of_times_year_month_day']['year'][year] = init_dict['no_of_times_year_month_day']['year'][year] + 1
        return
    init_dict['no_of_times_year_month_day']['year'][year] = 1

def check_if_day(day, index, iterable):
    if day > 0 and day<=31:
        if year_exists(iterable, index) | month_exists(iterable, index): 
            return True
    return False

def update_day(init_dict, day):
    if(day in init_dict['no_of_times_year_month_day']['day'].keys()):
        init_dict['no_of_times_year_month_day']['day'][day] = init_dict['no_of_times_year_month_day']['day'][day] + 1
        return
    init_dict['no_of_times_year_month_day']['day'][day] = 1

def info_about_lodder(iterable_length, index):
    if ((index/iterable_length) * 100)%10 == 0:
        print('*******completed*****', str(int((index/iterable_length)*100)) + '%')
    
def calculate_params(init_dict, text, index, iterable, requested_name):
    update_word_count_index(init_dict, text)
    if(check_word_exists(text, requested_name)):
        update_requested_word_index(init_dict)
    if(check_if_month(text)):
        update_month_names(init_dict, get_month_abbr(text))
    if(check_if_year(text, index, iterable)):
        if(text[-1] == 's'):
            text = text[:-1]
        update_year(init_dict, int(text))
        return
    if text.isdigit():
        if(check_if_day(int(text), index, iterable)):
            update_day(init_dict, int(text))
        
def find_the_required_params(init_dict, iterable, requested_name):
    length_of_corpus = len(iterable)
    j=0
    for index, text in enumerate(iterable):
        calculate_params(init_dict, text, index, iterable, requested_name)
        info_about_lodder(len(iterable)-1, index)
    init_dict['number_of_words_occur']['total_number_of_word_count'] = sum(init_dict['number_of_words_occur']['word_frequency'].values())
    return init_dict 

def runner_run(url_name, requested_name = 'trump'):
    print('**************initating_runner*****************')
    scrapped_text = scrap_it(url_name)
    init_dict = init_scrapper_info()
    month_names = init_month_names()
    return find_the_required_params(init_dict, clean_text(scrapped_text.lower()), requested_name)

init_dict = runner_run(requested_url)
save_to_json(json_filename, init_dict)