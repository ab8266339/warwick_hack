import json


parameter_dict = {
                        'general': {
                                    'doc_name' : 'constitution.txt',
                                    'pic_name' : 'Gon.png',
                                    'language' : 'english',
                                    'tfidf' : 'inverted_index_for_twocold',
                                   },
                                   
                        'wordcloud':
                                   {
                                    'margin': 1,
                                    'font_path': "msyh.ttf",
                                    'width': 1024,
                                    'height': 768,
                                    'max_font_size': 78,
                                    'background_color': "black",
                                    'max_words': 2000,
                                   }
                }
                          
with open('wordcloud_parameters.json' ,'w') as f:
    json.dump(parameter_dict, f, ensure_ascii=False, indent=4)