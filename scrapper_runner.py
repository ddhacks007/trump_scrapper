import sys
import scrapper_text
import logical_operations
import loader_information
import os_operations

month_names = None
json_filename = sys.argv[1]
requested_url = sys.argv[2:][0]

def calculate_params(init_dict, text, index, iterable, requested_name):
    logical_operations.update_word_count_index(init_dict, text)
    if(logical_operations.check_word_exists(text, requested_name)):
        logical_operations.update_requested_word_index(init_dict)
    if(logical_operations.check_if_month(text, update=True, update_dict=init_dict)):
        return
    if(logical_operations.check_if_year(text, index, iterable, update=True, update_dicts=init_dict)):
        return
    if text.isdigit():
        if(logical_operations.check_if_day(int(text), index, iterable)):
            logical_operations.update_day(init_dict, int(text))
        
def find_the_required_params(init_dict, iterable, requested_name):
    length_of_corpus = len(iterable)
    j=0
    for index, text in enumerate(iterable):
        calculate_params(init_dict, text, index, iterable, requested_name)
        loader_information.info_about_lodder(len(iterable)-1, index)
    init_dict['number_of_words_occur']['total_number_of_word_count'] = sum(init_dict['number_of_words_occur']['word_frequency'].values())
    return init_dict

def runner_run(url_name, requested_name = 'trump'):
    global month_names
    print('**************initating_runner*****************')
    scrapped_text = scrapper_text.scrap_it(url_name)
    init_dict = scrapper_text.init_scrapper_info()
    logical_operations.init_month_names()
    init_dict = find_the_required_params(init_dict, scrapper_text.clean_text(scrapped_text.lower()), requested_name)
    os_operations.save_to_json(json_filename, init_dict)
    return init_dict

init_dict = runner_run(requested_url)
