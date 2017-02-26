import re
import datetime
import time
import os
import collections

trump_date_dict = collections.defaultdict(lambda :'')
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

def read_trump():
    path1 = 'trump/trump1.txt'
    path2 = 'trump/trump2.txt'
    path_tuple = (path1, path2)
    for path in path_tuple:
        with open(path, 'r', encoding = 'utf-8') as f:
            for line in f:
                if line.startswith(u'\ufeff'):
                    line = line[1:]
                # convert date to date object
                date_str = line[0:12].strip()
                other_str = line[24:]

                date_object_temp = time.strptime(date_str, '%b %d, %Y')
                date_object = datetime.datetime(*date_object_temp[:3])

                other_str = re.subn(r'(@[A-Za-z_0-9:]+)?','', other_str)[0]
                other_str = re.subn(r'(\[[A-Za-z ]+\])?','', other_str)[0]
                other_str = re.subn(r'(http[:\/\.A-Za-z0-9]+ )?','', other_str)[0]
                other_str = re.subn(r'(http[:\/\.A-Za-z0-9]+\")?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+ )?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+\")?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+\.)?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+\!)?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+\?)?', '', other_str)[0]
                other_str = re.subn(r'(#[A-Za-z0-9]+\,)?', '', other_str)[0]
                other_str = re.subn(r'AM', '', other_str)[0]
                other_str = re.subn(r'PM', '', other_str)[0]
                trump_date_dict[date_object] += other_str

    for date, trump_twitter in trump_date_dict.items():
        date_str_file_name = date.strftime('%Y-%m-%d#twitter.txt')
        current_path = find_upper_level_folder_path(1)
        file_folder_path = os.path.join(current_path, 'text')
        file_path = os.path.join(file_folder_path, date_str_file_name)
        with open (file_path, 'w', encoding = 'utf-8') as f:
            f.write(trump_twitter)
            print ("Clean data succesful, write new data to file: {}".format(date_str_file_name))

read_trump()