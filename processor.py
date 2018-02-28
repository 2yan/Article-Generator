import os
import glob
import pandas as pd
import json
import shutil



def process_and_move():
    max_length = 0
    unique_characters = set()
    
    
    os.mkdir('cleaned')
    
    os.chdir('data')
    file_list = glob.glob('*.txt')
    os.chdir('..')
    for file_name in file_list:
        os.chdir('data')
        with open(file_name, 'r') as f:
            text = f.read()
        max_length = max(max_length, len(text))
        
        replacements = {'\xa0':'',
                        '\xad':'',
                        '®':' TM ',
                        '°':' degrees', 
                        '²':' squared ',
                        'º':'',
                        '½':'half' ,
                        '»':'',
                        '–':'-',
                        '—':'-',
                        '•':'',
                        '…':'...',
                        '\'':'\'',
                        '‘':'\'',
                        '’':'\'',
                        '“':'\'',
                        '”':'\'',
                        
                        }
    
        for key in replacements.keys():
            text = text.replace(key, replacements[key])
        text = text.lower()
        unique_characters = set(unique_characters).union(set(text))
        os.chdir('..')
        os.chdir('cleaned')
        
        with open(file_name, 'w') as f:
            f.write(text)
        
        os.chdir('..')
    return unique_characters
  
    
def get_dictionaries(text):
    unique = set(text)
    id_char = dict(zip(range(0, len(unique)), unique))
    char_id = dict(zip(id_char.values(), id_char.keys()))
    return id_char, char_id

if os.path.exists('cleaned'):
    shutil.rmtree('cleaned')
unique_characters = process_and_move()
id_char,char_id = get_dictionaries(unique_characters)
final = {'id_char':id_char,
 'char_id':char_id}

with open('text_number_mapping.json', 'w') as f:
    json.dump(final, f)