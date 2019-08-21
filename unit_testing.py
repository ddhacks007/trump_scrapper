import unittest
import logical_operations
import scrapper_preprocessor
import json
import uuid

#testing is done with lowercase letters (all the capital letters are converted to small leters )
def test_whether_the_word_trump_exists(test_data):
    curr_test = test_data['test_whether_the_word_trump_exists']
    number_of_tests_passed = 0
    for t_data in curr_test.keys():
        if logical_operations.check_word_exists(t_data, 'trump') == curr_test[t_data]:
            number_of_tests_passed = number_of_tests_passed + 1
    print('the number of tests passed for the word_trump_exists is ', str(number_of_tests_passed)+'/'+str(len(curr_test.keys())) )
    return(number_of_tests_passed, len(curr_test.keys()))

def test_whether_month_exists(test_data):
    curr_test = test_data['test_whether_month_exists']
    number_of_tests_passed = 0
    for t_data in curr_test.keys():
        if logical_operations.check_if_month(t_data) == curr_test[t_data]:
            number_of_tests_passed = number_of_tests_passed + 1
    print('the number of tests passed for the context month exists ', str(number_of_tests_passed)+'/'+ str(len(curr_test.keys()) ))
    return (number_of_tests_passed, len(curr_test.keys()))

def test_whether_year_exists(test_data):
    curr_test = test_data['test_whether_year_exists']
    number_of_tests_passed = 0
    for t_data in curr_test:
        temp = t_data[-1]
        t_data = t_data[:-1]
        if(logical_operations.check_if_year(temp['text'], temp['index'], t_data) == temp['result']):
            number_of_tests_passed = number_of_tests_passed + 1

    print('the number of tests passed for the context year exists ', str(number_of_tests_passed)+'/'+ str(len(curr_test) ))
    return(number_of_tests_passed, len(curr_test))

def test_whether_day_exists(test_data):
    curr_test = test_data['test_whether_day_exists']
    number_of_tests_passed = 0
    for t_data in curr_test:
        temp = t_data[-1]
        t_data = t_data[:-1]
        day = logical_operations.day_text_extraction(temp['text'])
        if(logical_operations.check_if_day(day, temp['index'], t_data) == temp['result']):
            number_of_tests_passed = number_of_tests_passed + 1
    print('the number of tests passed for the context day exists ', str(number_of_tests_passed)+'/'+ str(len(curr_test) ))
    return (number_of_tests_passed, len(curr_test))

def check_the_word_count_service(test_data):
    curr_test = test_data['test_whether_the_words_are_counted']
    number_of_tests_passed = 0
    for sentence in curr_test.keys():
        if(len(scrapper_preprocessor.clean_text(sentence)) == curr_test[sentence]):
            number_of_tests_passed = number_of_tests_passed + 1
    print('the number of tests passed for the word count service ', str(number_of_tests_passed)+'/'+ str(len(curr_test.keys()) ))
    return (number_of_tests_passed, len(curr_test.keys()))

def run_tests():
    print('*******************test-initiated********************')
    month_names = logical_operations.init_month_names()
    total_number_of_test_passed = 0
    total_number_of_tests = 0
    with open('test_data.json') as json_file:
        test_data = json.load(json_file)
    for func in [check_the_word_count_service, test_whether_day_exists, test_whether_year_exists, test_whether_month_exists, test_whether_the_word_trump_exists]:
        results = func(test_data)
        total_number_of_test_passed = total_number_of_test_passed + results[0]
        total_number_of_tests = total_number_of_tests + results[1]
    print('test pass percentage rate is', str(int((total_number_of_tests/total_number_of_test_passed)*100)), '%')

if __name__=='__main__':
    run_tests()
    