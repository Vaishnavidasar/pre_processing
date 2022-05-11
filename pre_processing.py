import os
os.getcwd()
import requests
from bs4 import BeautifulSoup
import re
import nltk
import html2text
import pandas as pd
from nltk import word_tokenize, pos_tag
from self_functions import *

def func(url):
    
    ## Data extraction in the text format
    r2 = requests.get(url).text
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = True
    result = h.handle(r2)
    #result
    result =result.replace(".","")
    
    ### Data cleanning and preprocessing
    r=[]
    from nltk.tokenize import sent_tokenize
    sent_tokenize=sent_tokenize(result)
    for i in range(len(sent_tokenize)):
            sent_tokenize[i] = sent_tokenize[i].lower() 
            sent_tokenize[i] = re.sub(r'[^a-zA-Z0-9\n/]+'," ",sent_tokenize[i])
            #sent_tokenize[i] = re.sub(r"[▢,#,*,%,!,$,),},?,-,@,:,{,;,=,&,+,_,[,x,(,',<,>,~,`,^,|,▼]","",sent_tokenize[i])
            #sent_tokenize[i] = re.sub(r"['»']","",sent_tokenize[i])
            #sent_tokenize[i] = re.sub(r"-","",sent_tokenize[i])
            #sent_tokenize[i] = re.sub(r"]","",sent_tokenize[i])
            #sent_tokenize[i] = re.sub(r"['\']","",sent_tokenize[i])

    ### remove the additional spaces         
    for i in sent_tokenize:
        r.append(i.strip())
    fr = list(filter(lambda item: item.strip(), r))
    #fr
    
    ###splitting the sentence on the basis of \n
    w=[]
    for n in range(len(fr)):
        w.append(fr[n].splitlines(True))

    ##flattening the list
    f = [item for sublist in w for item in sublist]
    #f
    
    ###condition checking for retaining all the \n in the respective sentences
    o=[]
    for i in range(len(f)):
        if i != len(f)-1:
            if (f[i] != '\n' and f[i+1] == '\n' and f[i+2] == '\n' and f[i+3] == '\n'):
                s1=f[i]
                s2=f[i+1]
                s3=f[i+2]
                s4=f[i+3]
                tu=s1+s2+s3+s4
                tu=tu.lstrip()
                o.append(tu)
            elif (f[i] != '\n' and f[i+1] == '\n' and f[i+2] == '\n'):
                s1=f[i]
                s2=f[i+1]
                s3=f[i+2]
                tu=s1+s2+s3
                tu=tu.lstrip()
                o.append(tu)
            elif (f[i] != '\n' and f[i+1] == '\n'):
                s1=f[i]
                s2=f[i+1]
                tu=s1+s2
                tu=tu.lstrip()
                o.append(tu)
            elif f[i] != '\n':
                f[i] = f[i].lstrip()
                o.append(f[i])
       
    ##remove all the empty strings
    while("" in o) :
        o.remove("")
  
    with open ('sample_dish.txt', 'w', encoding="utf-8") as f:
        for i in o:
            f.write(i)
    
    cleanned_string = o
    
    ## creating a list of no of \n after each sentence
    length=[]
    for i in range(len(cleanned_string)):
         length.append(len(re.findall('\n',cleanned_string[i])))
    
    ## creating list of of no of \n before each sentence
    l2=[0]
    for i in range(len(length)):
        l2.append(length[i])
    l2.pop(-1)

    for i in range(len(cleanned_string)):
            cleanned_string[i] = re.sub(r'\n'," ",cleanned_string[i])
            cleanned_string[i] = cleanned_string[i].strip()
        
    ## list of the sentence and the count 
    monk = []
    count= 0
    for data in cleanned_string:
        monk.append(  [data,length[count]]  )
        count = count + 1
        
    ##creating dataframe with 3 columns
    df = pd.DataFrame(monk)
    df['Sentence']=df[0]
    df['newline_after'] = df[1]
    df['newline_before'] = l2
    
    df['nwords'] = word_count(cleanned_string)
    df['numbers'] =digit_present(cleanned_string)
    df['nnumbers'] = digit_count(cleanned_string)
    df['nnouns'] = n_count(cleanned_string)
    df['nverbs'] = v_count(cleanned_string)
    df['nunits '] = unit_count(cleanned_string)
    df['nwords'] = df['nwords'].astype(int)
    
    df1 = df.drop([0,1], axis = 1)

    df1.to_csv('monk.csv',index = False)
    ## creating the csv file
    return(df1)

