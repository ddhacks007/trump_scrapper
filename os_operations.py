import os
import json

def make_dir(folder_name):
    try:
        if folder_name not in os.listdir('.'):
            os.makedirs(folder_name+'/')
    except OSError as e:
            return 

def save_to_json(json_filename, init_dict, directory_name = 'json_results', json_format = '.json'):
    make_dir(directory_name)
    file_name = json_filename + '.json'
    with open(os.path.join(directory_name, file_name), 'w') as fp:
        json.dump(init_dict, fp)
        print('your requested_data is successfully_stored in ', os.path.join(directory_name, file_name))
