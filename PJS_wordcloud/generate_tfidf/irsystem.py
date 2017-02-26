from FilterStopWords import FilterStopWords
import os
import re
import os
import jieba
"""CHINESE VERSION"""

class IRSystem(object):
    
    def __init__(self, cmdline_dict, parameter_dict):
        self.FILTER_STOP_WORDS = cmdline_dict['FILTER_STOP_WORDS']
        self.language = parameter_dict['language']
        stop_words_chinese_name = 'chinese_stopwords.txt'
        stop_words_english_name = 'english_stopwords.txt'
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.stop_words_path_chinese = os.path.join(current_path, stop_words_chinese_name)
        self.stop_words_path_english = os.path.join(current_path, stop_words_english_name)
        #self.stop_words_set = set()
    @staticmethod
    def cut_chinese_words(raw_word_list):
        word_string = ''.join(raw_word_list)
        processed_word_list = list(jieba.cut(word_string, cut_all=False))
        return processed_word_list
        
    @staticmethod
    def get_english_words(raw_word_list):
        parttern = r'[A-Za-z]+'
        word_string = ''.join(raw_word_list)
        processed_word_list = re.findall(parttern, word_string)
        return processed_word_list
        
    def Normalized_words_list(self, sentence_list):
        #-----inner function
            
        def filter_none_chinese_words(cut_chinese_words_list):
            pure_chinese_words_list = []
            for word in cut_chinese_words_list:
                if word >= '\u4e00' and word <= '\u9fff':
                    pure_chinese_words_list.append(word)
            return pure_chinese_words_list
        
        def filter_stop_words(words_list, stop_words_path):
            word_list_without_stopwords = []
            with open (stop_words_path, 'r') as f:
                stop_word_set = set()
                for line in f:
                    word = line.strip()
                    stop_word_set.add(word)
            for word in words_list:
                if (not word in stop_word_set):
                    word_list_without_stopwords.append(word)
            return word_list_without_stopwords
        
        def WordListNormalization(document_word_list):
            NeedModification = self.FILTER_STOP_WORDS
            if NeedModification:
                new_single_word_list = []
                if not self.stop_words_set:
                    stop_list_path = self.stop_words_path
                    self.stop_words_set = FilterStopWords.FilterStopWords(stop_list_path)
                for word in document_word_list:
                    if self.FILTER_STOP_WORDS:
                        if word in self.stop_words_set:
                            continue
                    new_single_word_list.append(word)
                return new_single_word_list
            else:
                return document_word_list
                    
        #--------------------end
        
        #<.><.><.>:::MainCode For FUNCTION Normalized_words_list:::<.><.><.>
        
        # raw sentence_list
        # sort the sentence_list
        sentence_list = sorted(sentence_list)
        # cut whole words string using jiaba
        chinese_final_words_list = []
        english_final_words_list = []
        if self.language == "chinese" or self.language == "bilingual":
            cut_chinese_words_list = IRSystem.cut_chinese_words(sentence_list)
            # filter none chinese words
            pure_chinese_words_list = filter_none_chinese_words(cut_chinese_words_list)
            # filter chinese stopwords
            chinese_stop_words_path = self.stop_words_path_chinese
            chinese_final_words_list = filter_stop_words(pure_chinese_words_list, chinese_stop_words_path)
        # get english words using reg
        if self.language == "english" or self.language == "bilingual":
            english_words_list = IRSystem.get_english_words(sentence_list)
            # convert to lower case
            english_words_list = [x.lower() for x in english_words_list]
            # filter english stopwords
            english_stopwords_path = self.stop_words_path_english
            english_final_words_list = filter_stop_words(english_words_list, english_stopwords_path)
            
        # get final words_list
        final_words_list = chinese_final_words_list
        final_words_list.extend(english_final_words_list)
        # normalize every word in document
        # return normalized_word_list
        return final_words_list
        #<.><.><.>:::END:::<.><.><.>
