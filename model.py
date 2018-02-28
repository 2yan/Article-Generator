import json
import os
import glob
import numpy as np
import keras as kr
def load_dictionaries():
    with open('text_number_mapping.json', 'r') as f:
        final = json.load(f)
    id_char = final['id_char']
    char_id = final['char_id']
    return id_char, char_id

def get_article_list():
    os.chdir('cleaned')
    file_list = glob.glob('*.txt')
    os.chdir('..')
    return file_list

def get_article(name):
    os.chdir('cleaned')
    with open(name, 'r') as f:
        text = f.read()
    os.chdir('..')
    return ' hello world ' * 500
    return text
    


def convert_data(text, sentence_length):
    
    text_references = []
    sentences = []
    next_letters = []
    i = 0
    sentence = []
    for char in text:
        current = char_id[char]
        #current = char
        text_references.append(current)
        if i > sentence_length:
            sentences.append(sentence)
            sentence = []
            i = 0
        if i < sentence_length:
            sentence.append(current)
        if i == sentence_length:
            next_letters.append(current)
        i = i + 1
    return sentences, next_letters

def one_hot_encode(sentences,next_letters, id_char ):
    X = np.zeros((len(sentences), len(sentences[0]), len(id_char)), dtype= np.bool)
    y = np.zeros((len(sentences), len(sentences[0])), dtype= np.bool)
    for sentence_index, sentence in enumerate(sentences):
        for char_index, char in enumerate(sentence):
            X[sentence_index, char_index, char ] = 1
        y[sentence_index, next_letters[sentence_index] ] = 1
    return X, y
        
def one_hot_to_text(onehot):
    result = list(onehot).index(max(onehot))
    return id_char[str(result)]




def get_X_y(article_name, sentence_length = 100):
    article = get_article(article_name)
    X, y= convert_data(article, sentence_length )
    X, y = one_hot_encode(X,y, id_char)
    return X, y
    
def get_sentence(sentence):
    result = ''
    for word in sentence:
        result = result + one_hot_to_text(word.astype(int))
    return result

def generate_model(X, y):
    model = kr.models.Sequential()
    model.add(kr.layers.LSTM(256, input_shape=X.shape[1:]))
    model.add(kr.layers.Dropout(0.2))
    #model.add(kr.layers.LSTM(input_shape=X.shape[1:]))
    model.add(kr.layers.Dense(X.shape[1]))
    model.add(kr.layers.Activation('softmax'))
    optimizer = kr.optimizers.RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model


def predect_letter_from_text(article):
    X, y= convert_data(article, sentence_length )
    X, y = one_hot_encode(X,y, id_char)
    X = X[0:1]
    
    predection = one_hot_to_text(model.predict(X)[0])
    result = get_sentence(X[0])
    return result  + predection


def predect_a_bunch(start_text, letter_count = 100):
    for num in range(0, letter_count):
        letter, start_text = predect_letter_from_text(start_text)
        start_text = start_text[1:] + letter
        print(letter, end = '')

sentence_length = 100
id_char, char_id = load_dictionaries()
article_list = get_article_list()

X, y = get_X_y(article_list[0], sentence_length)
model = generate_model(X,y)

for article_name in article_list:
    X, y = get_X_y(article_list[0], sentence_length)
    model.fit(X, y,epochs=20, verbose=1)
    predect_a_bunch(' hello world ' * 30, 300)