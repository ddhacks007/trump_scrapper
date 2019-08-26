import time
import sys
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import scrapper_preprocessor
import os_operations
import json
import numpy as np

nlp = en_core_web_sm.load()
requested_url = sys.argv[1:][0].split(' ')
    
def runner(url):
    global nlp
    init_dict = {}
    scrapped_text = scrapper_preprocessor.scrap_it(url).lower()
    doc = nlp(scrapped_text)
    init_dict['number_of_times_day_year_month_occurs'] = int(sum(np.array(([X.label_ for X in doc.ents])) == 'DATE'))
    init_dict['number_of_times_the_word_trump_occurs'] = int(sum(list(map(lambda x: x.find('trump')>=0,  scrapped_text.split(' ')))))
    init_dict['total_number_of_words'] = int(len(scrapper_preprocessor.clean_text(scrapped_text)))
    return init_dict

if __name__ == '__main__':
    start = time.time()
    final_dict = {}
    start = time.time()
    for url in requested_url:
        final_dict[url] = runner(url)
    print(final_dict)
    os_operations.save_to_json('prod_results', final_dict)
    print('time taken to execute the  runner', time.time() - start, 'seconds')
