import os 
#dirname=os.path.dirname

class FilterStopWords:
    @staticmethod
    def FilterStopWords(path):
        with open(path) as f:
            stop_word_set = set()
            for line in f:
                word = line.strip()
                stop_word_set.add(word)
            
            return stop_word_set

