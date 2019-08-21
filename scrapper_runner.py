import sys
import scrapper_preprocessor
import logical_operations
import completion_status_scrapper
import os_operations
import unit_testing
import time

month_names = None
requested_url = sys.argv[1:]

def find_the_required_params(init_dict, text, index, iterable, requested_name):
    if(logical_operations.check_word_exists(text, requested_name)):
        logical_operations.update_requested_word_index(init_dict)
        return
    if(logical_operations.check_if_month(text, update=True, update_dict=init_dict)):
        return
    if(logical_operations.check_if_year(text, index, iterable, update=True, update_dicts=init_dict)):
        return
    text = logical_operations.day_text_extraction(text)
    if text.isdigit():
        if(logical_operations.check_if_day(text, index, iterable)):
            logical_operations.update_day(init_dict, text)
        
def retrieve_information(init_dict, iterable, requested_name):
    length_of_corpus = len(iterable)
    for index, text in enumerate(iterable):
        find_the_required_params(init_dict, text, index, iterable, requested_name)
        completion_status_scrapper.completion_status(length_of_corpus-1, index)
    init_dict['total_number_of_words_occur'] = length_of_corpus
    init_dict['total_month_year_day_occurence'] = sum(init_dict['month_year_day_occurence']['year'].values()) + sum(init_dict['month_year_day_occurence']['month'].values()) +sum(init_dict['month_year_day_occurence']['day'].values()) 
    return init_dict

def runner_run(url_name, requested_name = 'trump'):
    global month_names
    print('scrapping initiated for the website', str(url_name).split('.')[1])
    month_names = logical_operations.init_month_names()
    scrapped_text = scrapper_preprocessor.scrap_it(url_name)
    init_dict = scrapper_preprocessor.init_scrapper_info()
    init_dict = retrieve_information(init_dict, scrapper_preprocessor.clean_text(scrapped_text.lower()), requested_name)
    print('scraping completed for the website', str(url_name).split('.')[1])
    return init_dict
    
if __name__=='__main__':
    final_dict = {}
    start = time.time()
    unit_testing.run_tests()
    for url_name in requested_url:
        init_dict = runner_run(url_name)
        final_dict[url_name] = init_dict.copy()
    os_operations.save_to_json('results', final_dict)
    print('time taken to execute the  runner', time.time() - start, 'seconds')
