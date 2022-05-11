import os
os.getcwd()
import requests
from bs4 import BeautifulSoup
import re
import nltk
import html2text
import pandas as pd
from nltk import word_tokenize, pos_tag

def word_count(list):
    word_count=[]
    for i in list:
        word_count.append(str(len(i.split())))
    return  word_count
def hasNumber(stringVal):
    re_numbers = re.compile('\d')
    return 0 if (re_numbers.search(stringVal) == None) else 1
def digit_present(list):
    digit_present=[]
    for i in list:
        digit_present.append(hasNumber(i))
    return digit_present
def digit_count(list):
    digit_count=[]
    for i in list:
        digit_count.append(sum(c.isdigit() for c in i))
    return digit_count
def n_count(list):
    n_count=[]
    for i in list:
        n_count.append(sum(1 for word, pos in pos_tag(word_tokenize(i)) if pos.startswith("NN")))
    return  n_count
def v_count(list):
    v_count=[]
    for i in list:
        v_count.append(sum(1 for word, pos in pos_tag(word_tokenize(i)) if pos.startswith("VB")))
    return  v_count
def unit_count(list):
    unit_count=[]
    measure_dict  = ["teaspoon","tablespoon","tablespoons","tblspn","inch","cups","cup","tbsps","tbsp","tsp","slices","slice","grams","litre","litres","medium","small"]
    for data in list:
        for sent in measure_dict :
            c =  0
            if sent in data:
                c = 1
                break
        unit_count.append(c)
    return unit_count