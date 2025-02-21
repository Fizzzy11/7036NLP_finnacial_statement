#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:02:16 2025

@author: liyitong
"""

import os
import re
from nltk.corpus import stopwords

# 下载停用词列表（如果尚未下载）
import nltk
nltk.download('stopwords')

# 获取英语停用词
stop_words = set(stopwords.words('english'))

# 将停用词写入stopwords.txt文件
with open('stopwords.txt', 'w', encoding='utf-8') as file:
    for word in stop_words:
        file.write(word + '\n')
print("停用词已写入stopwords.txt")

# 读取停用词
if not os.path.exists('stopwords.txt'):
    open('stopwords.txt', encoding='utf8', mode='w')

stopwords = set([line.strip() for line in open('stopwords.txt', encoding='utf8').readlines()])

def get_num_words(text, stopwords):
    # 使用正则表达式替换所有英文标点符号为空格
    cleaned_text = re.sub(r'''[.,!?;:"\']''', ' ', text)  # 标点符号替换为空格
    # 使用正则表达式 \s+ 将清理后的文本按空格、制表符、换行符等空白字符分割成一个单词列表
    list_word = re.split(r'\s+', cleaned_text)
    # 过滤出只包含英文字符的单词
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
                
                # 输出去除停用词后的文本到文件
                filtered_text = ' '.join(filtered_words)
                output_file_path = os.path.join(txt_folder, f"filtered_{filename}")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(filtered_text)

                print(f"文件: {filename} - 单词数量: {word_count}")
                print(f"过滤后的词列表: {filtered_words[:10]}...")  # 只显示前10个词

# 主函数
if __name__ == '__main__':
    base_dir = "txt"  # 年报文件夹路径
    process_directory(base_dir)