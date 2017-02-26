''' 
main function for assigenment1 of COM 6115
Author: JIASHU PU
Last update: 20 Nov 2016
'''

"""\
--------------------------------------------------------------------------------
stop word files are fixed, DO NOT CHANGE:
'chinese_stopwords.txt'
'english_stopwords.txt'

folder for raw doc is fixed:
raw_doc_for_tfidf 
--------------------------------------------------------------------------------
"""
import sys
import os
import re
import numpy as np
import collections
from read_comments.read_comments import ReadDocuments
from ReadWriteIndex import WriteIndexToJson, ReadIndexFromJson
from command_line_input import CommandLine
from inverted_index import InvertedIndex
from miscellaneous import Miscellaneous





# ------------main start----------------
if __name__ == "__main__":
    #-----------------------get the abs path for tf_idf_parameter_dict
    current_path = os.path.dirname(os.path.abspath(__file__))
    folder_name = "tf_idf_parameters"
    file_name = 'tf_idf_parameters' + '.json'
    tf_idf_file_abs_path = os.path.join(current_path, folder_name, file_name)
    tfidf_parameter_dict = Miscellaneous.get_parameter_dict_from_json(tf_idf_file_abs_path)
    tf_idf_file_name = tfidf_parameter_dict['file_name']
    #--------------------------------------------------------------------------------------
    #--------------raw_doc_folder_name
    raw_doc_folder_name = 'raw_doc_for_tfidf'
    
    # regular expression for extracting and excluding words for both query and documents
    # (1) create corresponding inverted index path(read and write) according to different command line input
    cmdline_dict= CommandLine.CommandLineInputInfo()
    #inverted_index_path = CommandLine.CreateCommandLinePath(inverted_index_path_prefix, cmdline_dict)
    inverted_index_path = os.path.join(Miscellaneous.find_upper_level_folder_path(2), tf_idf_file_name + '.json')
    # (2) create inverted_index and detect whether the inverted index has already been created based on path name
    # temp parameter_dict
    
    
    invertedindex = InvertedIndex(cmdline_dict, tfidf_parameter_dict)
    #corpus = ReadDocuments(singer_name = '佐橋俊彦')
    corpus = ReadDocuments(tfidf_parameter_dict, raw_doc_folder_name = raw_doc_folder_name)
    #temp_write(corpus, name = 'corpus')
    #print ("----------------", os.listdir(inverted_index_folder))
    # (3) create new inverted_index 
    inverted_index_dict = invertedindex.CreateInvertedIndexFromDocumentCollection(corpus)
    print("---------------------------------------------")
    print("Writing new inverted_index...")
    print ('inverted_index_path--------- ', inverted_index_path)
    WriteIndexToJson(inverted_index_dict, inverted_index_path) 
    print("Writing new inverted_index completed!")
    # else:
    # # (4) read inverted_index from existed file
    # print("---------------------------------------------")
    # print("Found the available inverted_index, start reading...")
    # inverted_index_dict = ReadIndexFromJson(inverted_index_path)
    # print("Reading inverted_index completed!")