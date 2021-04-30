# -*- coding: utf-8 -*-

import random
from janome.tokenizer import Tokenizer
import streamlit as st
# Janomeを使用してテキストデータを単語に分割する
def wakati(text):
    text = text.replace('\n','') #改行を削除
    text = text.replace('\r','') #スペースを削除
    t = Tokenizer()
    result =t.tokenize(text, wakati=True)
    return result

#デフォルトの文の数は5
def generate_text(string, num_sentence):
    src = string
    wordlist = wakati(src)
  
    #マルコフ連鎖用のテーブルを作成
    markov = {}
    w1 = ""
    w2 = ""
    for word in wordlist:
        if w1 and w2:
            if (w1, w2) not in markov:
                markov[(w1, w2)] = []
            markov[(w1, w2)].append(word)
        w1, w2 = w2, word
  
    #文章の自動生成
    count_kuten = 0 #句点「。」の数
    num_sentence= num_sentence
    sentence = ""
    w1, w2  = random.choice(list(markov.keys()))
    while count_kuten < num_sentence:
        tmp = random.choice(markov[(w1, w2)])
        sentence += tmp
        if(tmp=='。'):
            count_kuten += 1
            sentence += '\n' #1文ごとに改行
        w1, w2 = w2, tmp
     
    return  sentence

'''
__ 文章生成機 __
'''
'''
 このアプリの使い方

もとにしたい文章をtextファイルをアップするとそれっぽい文章を作ってくれます。
'''

st.write('''
## uploadfile
''')

string_num = st.slider('文章数', 1, 100, 10)
st.write('文章数', string_num)
upload_file = st.file_uploader(label='', type='txt')

if upload_file is not None:
    st.write('ファイル情報:', upload_file)
    string = upload_file.getvalue().decode("utf-8")
    st.write(generate_text(string, string_num))

