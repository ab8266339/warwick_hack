import json

#bilingual
parameter_dict = {
                    'file_name' : 'inverted_index_for_twocold',
                    'language' : 'english',
                    'sentence_num' : 99,
                }
                          
with open('wordcloud_parameters.json' ,'w') as f:
    json.dump(parameter_dict, f, ensure_ascii=False, indent=4)