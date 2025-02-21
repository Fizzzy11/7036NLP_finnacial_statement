#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:02:16 2025

@author: liyitong
"""

import os
import re
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
with open('stopwords.txt', 'w', encoding='utf-8') as file:
    for word in stop_words:
        file.write(word + '\n')
print("停用词已写入stopwords.txt")

if not os.path.exists('stopwords.txt'):
    open('stopwords.txt', encoding='utf8', mode='w')

stopwords = set([line.strip() for line in open('stopwords.txt', encoding='utf8').readlines()])

def get_num_words(text, stopwords):
    # Replace all English punctuation marks with spaces using regular expressions
    cleaned_text = re.sub(r'''[.,!?;:"\']''', ' ', text)  # Punctuation replaced with spaces
    # Use regular expressions \s+ to split cleaned up text into a list of words by whitespace characters such as spaces, tabs, line breaks, etc.
    list_word = re.split(r'\s+', cleaned_text)
    # Filter out words containing only English characters
    filtered_lst = [item for item in list_word if re.match(r'^[a-zA-Z]+$', item)]
    filtered_lst = [x for x in filtered_lst if x not in stopwords]
    return len(filtered_lst), filtered_lst

def process_directory(txt_folder):
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(txt_folder, filename)
            with open(file_path, "r", encoding='utf-8') as f:
                txt = f.read()
                word_count, filtered_words = get_num_words(txt, stopwords)
                
                # Output the text to the file after removing the stop words.
                filtered_text = ' '.join(filtered_words)
                output_file_path = os.path.join(txt_folder, f"filtered_{filename}")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(filtered_text)

                print(f"file: {filename} - wordsnumber: {word_count}")
                print(f"List of filtered words: {filtered_words[:10]}...")  # Show only the first 10 words

# main function
if __name__ == '__main__':
    base_dir = "txt"  # Annual Report Folder Path
    process_directory(base_dir)