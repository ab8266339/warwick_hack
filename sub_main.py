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
       
# import subprocess
import os
import sys
import subprocess

def run_python(path):
    cwd = os.path.dirname(os.path.realpath(path))
    subprocess.call("python {}".format(path), shell=True, cwd = cwd)
        
        
# create path for python folder and files
current_folder = find_upper_level_folder_path(1)
# (1.) main
code_main_folder = find_upper_level_folder_path(1)
main__path = os.path.join(code_main_folder, 'main.py')
# (2.) generate tf-idf
generate_tf_idf_folder = os.path.join(current_folder, 'PJS_wordcloud', 'generate_tfidf')
generate_tf_idf__path = os.path.join(generate_tf_idf_folder, 'generate_tf_idf.py')
# (3.) create word cloud
word_cloud_folder = os.path.join(current_folder, 'PJS_wordcloud')
word_cloud__path = os.path.join(word_cloud_folder, 'simple_wordcloud.py')



#:::RUN:::
#(1.) formatter
run_python(main__path)
# run_python(generate_tf_idf__path)
# run_python(word_cloud__path)


