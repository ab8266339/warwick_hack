import json

def WriteIndexToJson(inverted_index, path):
    print ('path ', path)
    with open(path, 'w', encoding = 'utf-8') as f:
        json.dump(inverted_index, f, indent=4, ensure_ascii=False)
    
def ReadIndexFromJson(path):
    print ('path ', path)
    with open(path, 'r', encoding = 'utf-8') as f:
        inverted_index_dict = json.load(f)
    return inverted_index_dict
    
