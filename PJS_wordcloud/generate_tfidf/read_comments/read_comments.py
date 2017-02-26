
import json
import math
import re, sys
import os
import math
'''read txt files into object, for computing tfidf'''


class Document:
    def __init__(self):
        self.docid = '0'
        self.name = ''
        self.author = ''
        self.lines = []

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


class ReadDocuments:
    # default : read the whole netease music database
    def __init__(self, tfidf_parameter_dict, raw_doc_folder_name = 'raw_doc_for_tfidf'):
        self.raw_doc_folder_name = raw_doc_folder_name
        #granularity
        self.sentence_num_threshold = tfidf_parameter_dict['sentence_num']
        self.CUT_ARTICLE = tfidf_parameter_dict['CUT_DOC']
    def collect_json_list(self, raw_doc_folder_name):
        #-----------------collect_json_list------------------MAIN
        raw_doc_folder_path = os.path.join(find_upper_level_folder_path(2), raw_doc_folder_name)
        doc_name_list = os.listdir(raw_doc_folder_path)
        doc_path_list = map(lambda x: os.path.join(raw_doc_folder_path, x), doc_name_list)
        #  
        return doc_path_list
        
    #def test1(self):
    #    print('aaaa')
        

            
    def __iter__(self):
        # get json_list for all music, one element is a json path for one song
        doc_list = self.collect_json_list(self.raw_doc_folder_name)
        # cut the target article into even sections, and create corresponding object
        def create_even_doc_object(sentence_num_threshold, article_sentence_list):
            if len(article_sentence_list) > sentence_num_threshold and self.CUT_ARTICLE == True:
                doc_num = math.ceil(len(article_sentence_list) / sentence_num_threshold)
                for i in range(doc_num):
                    doc = Document()
                    doc.lines = article_sentence_list[i*sentence_num_threshold:(i+1)*sentence_num_threshold]
                    doc.docid = os.path.basename(f.name)
                    doc.docid = doc.docid[:len(doc.docid)-4] + '_' + str(i)
                    yield doc
            else:
                doc = Document()
                doc.lines = article_sentence_list
                doc.docid = os.path.basename(f.name)
                doc.docid = doc.docid[:len(doc.docid)-4] + '_0'
                yield doc

        for i, doc_path in enumerate(doc_list):
            with open(doc_path, encoding = 'utf-8') as f:
                # meta_info
                article_sentence_list = f.readlines()
                
                # add "." to the end of every sentence, to distinguish title and the main content body
                article_sentence_list = list(map(lambda x: x + '.',article_sentence_list))
                sentence_num_threshold = self.sentence_num_threshold
                for doc in create_even_doc_object(sentence_num_threshold, article_sentence_list):
                    yield doc
                
# r = ReadDocuments(raw_doc_folder_name = "raw_doc_for_tfidf")
# for doc in r:
    # print ("----------------------")
    # print (doc.docid)
    # print ("doc.lines: ", len(doc.lines))