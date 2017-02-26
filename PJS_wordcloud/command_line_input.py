import re
import os
import sys
import getopt


class CommandLine():
    @staticmethod
    # this function is only for text processing assignment1
    def CommandLineInputInfo():
        # default_values
        LOWER_CASE = True
        STEMMING = False
        FILTER_STOP_WORDS = False
        TEST_INVERTED_INDEX = False
        DEFAULT_PATH = True
        mode = "tfidf"
        basic_path = "result.txt"
        result_path = "default_my_result.txt"
        
        inverted_index_s_arguments_string = ""
        inverted_index_l_arguments_list = ["stopwords", "stem", "name=",  "test_inv", "mode="]
        
        
        # TODO bug fix
        try:
            opts, args = getopt.getopt(sys.argv[1:], inverted_index_s_arguments_string, inverted_index_l_arguments_list)
        except getopt.GetoptError:
            print ('sys arguments error, check help')
            sys.exit()
            
        #create validation list
        for i,string in enumerate(inverted_index_l_arguments_list):
            if string[-1] == "=":
                string = string[:len(string)-1]
            inverted_index_l_arguments_list[i] = "".join(["--", string])
            
        print("opts:{}".format(opts))
        for o, a in opts:
            #"stopwords"
            if o == inverted_index_l_arguments_list[0]:
                FILTER_STOP_WORDS = True
            #"stem"    
            elif o == inverted_index_l_arguments_list[1]:
                STEMMING = True
            elif o == inverted_index_l_arguments_list[4]:
                if a == "binary":
                    mode = "binary"
                elif a == "tfidf":
                    mode = "tfidf"
                elif a == "tf":
                    mode = "term_frequency"
                else:
                    print("invalid parameter!!")
                    sys.exit()
            elif o == "--name":
                DEFAULT_PATH = False
                a = a + '.txt'
                # handle exception
                if (a in os.listdir()):
                    print(result_path)
                    print('File name already exist! Please choose another name.')
                    sys.exit()
                try:
                    with open(a,'w') as f:
                        pass
                except OSError:
                    print('Invalid file name!')
                    sys.exit()
                result_path = a
                # detect the validation of custom file direction
            # inverted_index start
            elif o == inverted_index_l_arguments_list[3]:
                TEST_INVERTED_INDEX = True

                
        cmdline_dict = {}
        cmdline_dict['LOWER_CASE'] = LOWER_CASE
        cmdline_dict['STEMMING'] = STEMMING
        cmdline_dict['FILTER_STOP_WORDS'] = FILTER_STOP_WORDS
        cmdline_dict['TEST_INVERTED_INDEX'] = TEST_INVERTED_INDEX
        cmdline_dict['mode'] = mode
        #construct_path
        if DEFAULT_PATH:
            result_path = basic_path
            if STEMMING:
                result_path = 'STEMMING+' + result_path
            if FILTER_STOP_WORDS:
                result_path = 'FILTER_STOP_WORDS+' + result_path
            if mode:
                result_path = mode + '+' + result_path
            else:
                result_path = "+tfidf" + result_path
            

        cmdline_dict['result_path'] = result_path
        print("---------------------------------------------")
        print("IR system parameter chosen: \n")
        print ("Weight chosen: {}".format(mode))
        print ("TEST_INVERTED_INDEX: {}".format(TEST_INVERTED_INDEX))
        print ("convert to lower case: {}".format(LOWER_CASE))
        print ("stem: {}".format(STEMMING))
        print ("filter stop words: {}".format(FILTER_STOP_WORDS))
        return cmdline_dict
    
    @staticmethod
    def CreateCommandLinePath(path, cmdline_dict):
        # #create corresponding path according to different command line input, using sorted to make sure same order
        for key, value in sorted(cmdline_dict.items(), key = lambda x: x[0]):
            if value == True:
                path = path + '+' + key
        path += '.txt'
        return path
        