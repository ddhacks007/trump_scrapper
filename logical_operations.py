import math
import calendar
import datetime

def check_word_exists(text, requested_word):
    return True if text.find(requested_word)>=0 else False

def update_requested_word_index(init_dict):
    init_dict['no_of_times_the_word_trump_occurs'] = init_dict['no_of_times_the_word_trump_occurs'] + 1

def init_month_names(number_of_months = 12):
    global month_names
    month_names = []
    for month in range(1, number_of_months+1):
        month_names.append([calendar.month_abbr[month].lower(), calendar.month_name[month].lower()])
    return month_names
    
def check_if_month(text, update = False, update_dict = {}):  
    global month_names
    for  month in month_names:
        if text in month:
            if update:
                update_month_names(update_dict, month[0])
            return True
    return False

  
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
    if(month_name in init_dict['month_year_day_occurence']['month'].keys()):
        init_dict['month_year_day_occurence']['month'][month_name] = init_dict['month_year_day_occurence']['month'][month_name] + 1
        return
    init_dict['month_year_day_occurence']['month'][month_name] = 1
    
def number_of_digits(num):
    return math.floor(math.log(int(num), 10) + 1) if num>0 else 0
    
def check_if_year(text, index, iterable, update=False, update_dicts={}, min_year_threshold=1000, max_year_threshold = datetime.datetime.now().year + 100):
    try:
        s_flag = 0
        if((text[-1] == 's' and text[:-1].isdigit())):
            text = text[:-1]
            s_flag = 1
        if(text.isdigit() and int(text)>=min_year_threshold and int(text) <= max_year_threshold):
            if  (s_flag == 1) or (month_exists(iterable, index)) or (index >0 and iterable[index-1] in  ['in', 'year', 'by']) or (index<len(iterable)-1 and iterable[index + 1].find('election')>=0 ) :
                if(update):
                    update_year(update_dicts, text)
                return True
        return False
    except:
        raise
        print(text, 'index', index)
        return False
    

def update_year(init_dict, year):
    if(year in init_dict['month_year_day_occurence']['year'].keys()):
        init_dict['month_year_day_occurence']['year'][year] = init_dict['month_year_day_occurence']['year'][year] + 1
        return
    init_dict['month_year_day_occurence']['year'][year] = 1
    
def day_text_extraction(text):
    if text.isdigit() :
        return text
    elif(text[-2:] in ['th', 'rd', 'nd', 'st']):
        return text[:-2]
    return ''

def check_if_day(day, index, iterable):
    day = int(day)
    if day > 0 and day<=31:
        if year_exists(iterable, index) | month_exists(iterable, index): 
            return True
    return False

def update_day(init_dict, day):
    if(day in init_dict['month_year_day_occurence']['day'].keys()):
        init_dict['month_year_day_occurence']['day'][day] = init_dict['month_year_day_occurence']['day'][day] + 1
        return
    init_dict['month_year_day_occurence']['day'][day] = 1