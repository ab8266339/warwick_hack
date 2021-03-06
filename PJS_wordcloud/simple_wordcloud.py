#!/usr/bin/env python2
def find_upper_level_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return find_upper_level_folder_path(num, path = path)
    else:
        return path

"""
Simple wordcloud generator with basic functions
Author: PJS
Update: 2016-12-20
"""
#from __future__ import unicode_literals
import os, sys
import re
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from command_line_input import CommandLine
# import irsystem
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, 'generate_tfidf'))
from irsystem import IRSystem
from PIL import Image
import jieba
import collections
import random
import json

class PJS_wordcloud():
    def __init__(self, cmdline_dict, parameter_path = 'wordcloud_parameters.json', doc_name=''):
        # future use
        self.cmdline_dict = cmdline_dict
        with open(parameter_path, 'r', encoding = 'utf-8') as f:
            main_parameter_dict = json.load(f)
        # Only accept txt，use ANSI decode?
        if not doc_name:
            doc_name = main_parameter_dict['general']['doc_name']
        pic_name = main_parameter_dict['general']['pic_name']
        language = main_parameter_dict['general']['language']
        self.language = main_parameter_dict['general']['language']
        tfidf = main_parameter_dict['general']['tfidf']
        self.parameter_dict = main_parameter_dict['wordcloud']
        
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.current_path = current_path
        self.doc_path = os.path.join(current_path, 'input_raw_txt', doc_name + '.txt')
        self.sorted_dic_output_path = os.path.join(current_path, 'output', 'sorted_output_' + doc_name + '.txt')
        #PIC
        if pic_name:
            self.PIC_MODE = True
            self.NORMAL_MODE = False
            self.pic_path = os.path.join(current_path, 'input_pic', pic_name)
        else: 
            self.PIC_MODE = False
            self.NORMAL_MODE = True
        self.output_pic_path = os.path.join(current_path, 'output', 'output_pic_' + doc_name + '.png')
        #LANGUAGE
        if language == 'chinese':
            self.isChinese = True
            self.isEnglish = False
        elif language == 'english':
            self.isChinese = False
            self.isEnglish = True
        elif language == 'bilingual':
            self.isChinese = True
            self.isEnglish = True
        #TFIDF
        if tfidf:
            self.TFIDF_MODE = True
            self.tfidf_path = os.path.join(current_path, tfidf + '.json')
            # load tfidf_dict
            with open(self.tfidf_path, 'r', encoding = 'utf-8') as f:
                self.tfidf_dict = json.load(f)
            
        else:
            self.TFIDF_MODE = False
           
        
    def output_pic(self, word_frequency_list, is_display = True):
        
        def create_wordcloud():
            margin = self.parameter_dict['margin']
            font_path = self.parameter_dict['font_path']
            width = self.parameter_dict['width']
            height = self.parameter_dict['height']
            max_font_size = self.parameter_dict['max_font_size']
            background_color = self.parameter_dict['background_color']
            max_words = self.parameter_dict['max_words']
            scale = self.parameter_dict['scale']
            if self.PIC_MODE:
                mask_pic = np.array(Image.open(self.pic_path))
                self.wordcloud = WordCloud(font_path = font_path,margin = margin, width = width, max_font_size = max_font_size, height = height, background_color = background_color, max_words = max_words, mask=mask_pic, scale = scale)
                self.wordcloud.generate_from_frequencies(word_frequency_list)
                image_colors = ImageColorGenerator(mask_pic)
                self.wordcloud.recolor(color_func=image_colors)
            elif self.NORMAL_MODE:
                self.wordcloud = WordCloud(font_path = font_path,margin = margin, width = width, max_font_size = max_font_size, height = height, background_color = background_color, max_words = max_words, scale = scale)
                self.wordcloud.generate_from_frequencies(word_frequency_list)
            
            
        def normal_pic_display(wordcloud):
            plt.title("Normal")
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            
        def mask_pic_display(wordcloud):
            plt.title("Mask")
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()

            
        def pic_output(wordcloud):
            #print ('self.output_pic_path: ', self.output_pic_path)
            wordcloud.to_file(self.output_pic_path)
            


        
        #::output_pic::
        # get parameters and create wordcloud
        create_wordcloud()
        # mask_pic initialize
        wordcloud = self.wordcloud
        if is_display:
            if self.PIC_MODE:
                mask_pic_display(wordcloud)
            elif self.NORMAL_MODE:
                normal_pic_display(wordcloud)
        # write pic to file
        pic_output(wordcloud)
        
        
    def get_word_frequency_dict(self, raw_word_list):
        def get_tf_dict(word_list):
            word_tf_dict = collections.defaultdict(lambda: 0)
            for word in word_list:
                word_tf_dict[word] += 1
            return word_tf_dict
            
        def get_tfidf_dict(word_tf_dict):
            for word, tf in word_tf_dict.items():
                word_tf_dict[word] = tf * self.tfidf_dict[word]['idf']
            word_dict = word_tf_dict
            return word_dict
        
    
        #------------:::get_word_frequency_dict:::-------------------------
        irsystem_dict = {'language': self.language}
        normalizer = IRSystem(self.cmdline_dict, irsystem_dict)
        cleaned_word_list = normalizer.Normalized_words_list(raw_word_list)
        word_dict = get_tf_dict(cleaned_word_list)
        if self.TFIDF_MODE:
            word_dict = get_tfidf_dict(word_dict)
        return word_dict
        
        
    def get_raw_word_list(self):
        with open(self.doc_path, 'r', encoding = 'utf-8') as f: 
            raw_word_list = f.readlines()
            raw_word_list = list(map(lambda x: x + '.',raw_word_list))
        return raw_word_list
        
    def write_sorted_tf_dict_to_file(self,word_tf_dict):
        with open (self.sorted_dic_output_path, 'w', encoding = 'utf-8') as f:
            for key, value in sorted(word_tf_dict.items(), key = lambda x:x[1], reverse = True):
                f.write(str((key, value)))
                f.write('\n')
    
        
# MAIN
# for future use 
cmdline_dict = CommandLine.CommandLineInputInfo()
parameter_path = 'wordcloud_parameters.json'


import shutil

def delete_folder_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


#
current_path = os.path.dirname(os.path.abspath(__file__))
month_list = ['_', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
input_folder = os.path.join(current_path, 'input_raw_txt')
file_name_list = os.listdir(input_folder)
# 


# delete everything in result folder
parent_folder = find_upper_level_folder_path(2)
output_pic_folder = os.path.join(parent_folder, 'result', 'word_cloud')
delete_folder_files(output_pic_folder)

for file_name in file_name_list:
    #print ("file_name_list: ", file_name_list)
    file_base_name_list = re.findall(r'([0-9]+-[0-9]+-[0-9]+)#', file_name)
    file_base_name = file_name
    if not file_base_name_list:
        continue
    else:
        file_base_name_str = file_base_name_list[0]

    file_base_name_list = file_base_name_str.split('-')
    month_order = int(file_base_name_list[1])
    month = month_list[month_order]
    day = file_base_name_list[2]
    year = file_base_name_list[0]
    file_name = month + '_' + year
    # reset the output path

    ## old code
    wordcloud1 = PJS_wordcloud(cmdline_dict, parameter_path = parameter_path, doc_name = file_base_name[:-4])
    
    
    wordcloud1.output_pic_path = os.path.join(output_pic_folder, file_name + '.png')
    wordcloud1.sorted_dic_output_path = os.path.join(output_pic_folder, 'sorted_output_' + file_name + '.txt')
    
    raw_word_list = wordcloud1.get_raw_word_list()
    word_frequency_dict = wordcloud1.get_word_frequency_dict(raw_word_list)
    wordcloud1.output_pic(word_frequency_dict.items(), is_display = False)
    wordcloud1.write_sorted_tf_dict_to_file(word_frequency_dict)
    print("----------------------------------------------------------------------------")
    print ("Built {} {} wordcloud successfully!".format(day, month))
    #old code end
#


        
        

