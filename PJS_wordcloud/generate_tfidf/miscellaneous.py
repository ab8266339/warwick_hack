import re
import numpy as np
import json
import os
''' put this class in the main dir'''
class Miscellaneous(object):
    
    @staticmethod
    def ConvertStrToBagOfWords(reg, reg_exclude, document_in_a_sentence):
        document_word_list = []
        # find all words match regular expression
        word_list_before_filter = re.findall(reg, document_in_a_sentence)
        #exclude all invalid words
        word_list = []
        for i,word in enumerate(word_list_before_filter):
            try:
                find_excluded = re.findall(reg_exclude, word)
            # if the reg is invalid, print the details 
            except TypeError:
                print ("error word: ", word)
            #not found means the word should not be excluded and should be added to list
            if not find_excluded:
                word_list.append(word)
            
        document_word_list.extend(word_list)
        return document_word_list
    
    @staticmethod
    #input word_dict = {'word1':2, 'word2': 9}, converted to ndarray in order
    def DictToNdarray(word_dict):
        sorted_value_list = [word_dict[x] for x in sorted(word_dict)]
        word_array = np.array([sorted_value_list])
        return word_array
    @staticmethod
    def find_upper_level_folder_path(num, path = ''):
        if not path:
            path = os.path.dirname(os.path.abspath(__file__))
        else:
            path = os.path.dirname(path)
        num -= 1
        if num > 0:
            return Miscellaneous.find_upper_level_folder_path(num, path = path)
        else:
            return path
    @staticmethod
    def find_singer(id):
        with open ('id_to_singer_dict.json', 'r', encoding = 'utf-8') as f:
            id_to_singer_dict = json.load(f)
            singer = id_to_singer_dict[id]
        return singer
        
    @staticmethod
    def singer_or_id(singer, song_id):
        with open ('id_to_singer_dict.json', 'r', encoding = 'utf-8') as f:
            id_to_singer_dict = json.load(f)
            id_set = set(id_to_singer_dict.keys())
            singer_set = set(id_to_singer_dict.values())
            if song_id in id_set:
                return 'id'
            elif song_id and (not song_id in id_set):
                print ("The song id ({}) you type is not in the database".format(song_id))
                return None
            elif singer in singer_set:
                return 'singer'
            elif singer and (not singer in singer_set):
                print ("The singer ({}) you type is not in the database".format(singer))
                return None
            else:
                print('Invalid, please check your input!! ')
                return None
        
    @staticmethod
    def get_parameter_dict_from_json(file_abs_path):
        with open(file_abs_path, 'r', encoding = 'utf-8') as f:
            parameter_dict = json.load(f)
        return parameter_dict
        
        
        
        
        
        
        
        
        
        
        
        
        