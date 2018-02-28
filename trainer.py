import numpy as np
import os
import glob
import keras as kr
import ryan_tools as rt
import time
import json


class TextGetter():
    def get_article_list(self):
        os.chdir('cleaned')
        file_list = glob.glob('*.txt')
        os.chdir('..')
        return file_list

    def get_article(self, name):
        os.chdir('cleaned')
        with open(name, 'r') as f:
            text = f.read()
        os.chdir('..')
        return text
    
    def get_corpus(self):
        articles = self.get_article_list()
        result = ''
        bar = rt.progress_bar(len(articles))
        for art_name in articles:
            result = result + self.get_article(art_name)
            bar.progress()
        return result
    

def get_text():
    text_getter = TextGetter()
    text = text_getter.get_corpus()
    return text

def create_dictionaries(text):
    char_id = dict(zip(set(text), range(len(set(text)))))
    id_char = dict(zip(char_id.values(), char_id.keys()))
    return id_char, char_id


def load_dictionaries():
    with open('text_number_mapping.json', 'r') as f:
        final = json.load(f)
    str_id_char = final['id_char']
    char_id = final['char_id']
    
    id_char = {}
    for key in str_id_char.keys():
        id_char[int(key)] = str_id_char[key]
    
    return id_char, char_id



def sample(a, temperature=1.0):
    a = a**(1/temperature)
    sample_temp = a/(a.sum()*1.0001)
    sampled = np.random.multinomial(1, sample_temp, 1)
    return np.argmax(sampled)

def convert_char_id(text):
    result = []
    features = len(char_id)
    for i, char in enumerate(text):
        position = int(char_id[char])
        observation = np.zeros(( features))
        observation[position] = 1
        result.append(observation)
    return np.array(result)

def convert_id_char(onehot, temperature):
    result = ''
    for letter in onehot:
        l = sample(letter, temperature)
        result = result + id_char[l]
    return result

def get_X_y(list_of_one_hots, sentence_length, do_bar = True):
    y = []
    X = []
    if do_bar:
        bar = rt.progress_bar(len(list_of_one_hots), 100)
    for i, letter in enumerate(list_of_one_hots):
        if i > sentence_length:
            y.append(letter)

            x = list_of_one_hots[i- sentence_length:i]
            X.append(x)
        if do_bar:
            bar.progress()

    return np.array(X), np.array(y)


def predict(text, temperature):
    onehot = convert_char_id(text[-sentence_length:])
    return convert_id_char(model.predict(np.array([onehot]), 1), temperature)


def print_letters(seed_text, sentence_length, how_many, temperature= 1):
    while len(seed_text) < sentence_length:
        seed_text = ' ' + seed_text
        
    result = seed_text
    for num in range(0, how_many):
        prediction = predict(seed_text, temperature)
        seed_text = seed_text[1:] + prediction
        result = result + prediction
    return result

def test_sizes(batch_size, samples, epochs):
    global start_point
    start = time.time()
    X,y  = get_X_y(one_hots[start_point: start_point + samples], sentence_length, False)
    
    earlystop = kr.callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=10, \
                          verbose=1, mode='auto')
    
    callbacks_list = [earlystop]
    callback = model.fit(X, y, epochs = epochs,validation_split= 0.3, batch_size= batch_size, verbose =0, callbacks= callbacks_list )
    start_point = start_point + samples
    time_taken = time.time() - start
    print(start_point)
    print('Projected Time for 10000 samples {}'.format(time_taken * 10000/(samples* epochs)))
    return callback

def print_at_temperatures():
    seed_text = 'h1 : 5s examples in action: the good and the bad'.lower()
    for temperature in [0.1, 0.3, .5, .7, 1]:
        print(temperature)
        print(print_letters(seed_text, sentence_length, 100, temperature).capitalize()[len(seed_text):])
        
        
text = get_text()
id_char, char_id = load_dictionaries()
one_hots = convert_char_id(text)
start_point = 0
sentence_length = 100
model = kr.models.load_model('model.weights')


samples = 500

for num in range(start_point, len(one_hots)):
    if num%samples == 0:
        start = num
        rt.clear_output(True)
        callback = test_sizes(500, samples, 1000)
        print(min(callback.history['loss']))
        print_at_temperatures()
        model.save('model.weights')