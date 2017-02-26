from pjslib.logger import logger1
#
import os,http, http.client, urllib.request, urllib.parse, urllib.error, base64
import pprint
import os
import json
import collections
import PIL.Image
import exifread
import datetime
import time
import re
import sys
import requests
import matplotlib.pyplot as plt
pp = pprint.PrettyPrinter(indent=4)

class EmotionDetection:

    def __init__(self):
        def set_all_paths():
             current_path = os.path.dirname(os.path.abspath(__file__))
             face_folder_name = 'face'
             text_folder_name = 'text'
             archives_name = 'archives'
             # face(input)
             self.face_folder_path = os.path.join(current_path, face_folder_name)
             self.face_archives_path = os.path.join(current_path, archives_name, face_folder_name)
             # text(input)
             self.text_folder_path = os.path.join(current_path, text_folder_name)
             self.text_archives_path = os.path.join(current_path, archives_name, text_folder_name)
             # text(output)
             self.text_output_folder_path = os.path.join(current_path, 'result', 'text')
             # pdf(output)
             self.pdf_output_folder_path = os.path.join(current_path, 'result', 'pdf')
             # image(output)
             self.image_output_folder_path = os.path.join(current_path, 'result', 'image')

        self.headers = {
             # Basic Authorization Sample
             'Content-type': 'application/octet-stream',
             'Ocp-Apim-Subscription-Key': '27e26524b06b41caa2ff561da9620b5c',
          }

        self.params = urllib.parse.urlencode({
             ## Specify your subscription key
             # 'subscription-key': '',
             ## Specify values for optional parameters, as needed
             # 'analyzesFaceLandmarks': 'false',
             # 'analyzesAge': 'false',
             # 'analyzesGender': 'false',
             # 'analyzesHeadPose': 'false',
          })

        # :::__init__:::
        set_all_paths()
        self.date_photo_emotion_dict = collections.defaultdict(lambda : collections.defaultdict(lambda :0))
        self.date_text_emotion_dict = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))



    def get_emotion_dict(self, file_path):

        headers = {
            # Basic Authorization Sample
            'Content-type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '27e26524b06b41caa2ff561da9620b5c',
        }

        params = urllib.parse.urlencode({
            ## Specify your subscription key
            # 'subscription-key': '',
            ## Specify values for optional parameters, as needed
            # 'analyzesFaceLandmarks': 'false',
            # 'analyzesAge': 'false',
            # 'analyzesGender': 'false',
            # 'analyzesHeadPose': 'false',
        })

        file = open(file_path, "rb").read()


        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, file, headers)
            print("send request")
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            json_obj = json.loads(data)[0]
            conn.close()
        except IndexError:
            logger1.info("{} does not contain any faces".format(file_path))
            return None
        except KeyError:
            logger1.info("{} key Error! Maybe too big or too small".format(file_path))
            return None
        except:
            logger1.error("Unexpected error:", sys.exc_info()[0])
            raise
            return None

        return json_obj


    def get_photo_emotion_dict(self):
        def add_dicts_value(dict1, dict2):
            if len(dict1) != len(dict2):
                logger1.error("Emotion list do not have the same length!")
                sys.exit()
            """Adding the values of the 2 dicts with the same key"""
            for key, value in dict2.items():
                dict1[key] += dict2[key]
            return dict1



        # ::: get_photo_emotion_dict
        photo_folder_list = os.listdir(self.face_folder_path)
        photo_folder_list = [os.path.join(self.face_folder_path, x) for x in photo_folder_list]
        print ("photo_folder_list", photo_folder_list)
        for photo_file_path in photo_folder_list:
            # days_ago =
            f = open(photo_file_path, 'rb')
            # Return Exif tags
            tags = exifread.process_file(f)
            print (type(tags))
            print(tags)
            print(tags.keys())
            try:
                date_of_photo = tags['EXIF DateTimeDigitized']
            except KeyError:
                logger1.error("photo in {} has no meta data of digitized time!".format(photo_file_path))
                continue
            # convert to str,
            date_of_photo = str(date_of_photo)
            # convert str to date object


            # date_of_photo = 2017:02:01
            date_of_photo = re.findall(r'([0-9]+:[0-9]+:[0-9]+)', date_of_photo)[0]
            date_of_photo_temp = time.strptime(date_of_photo, '%Y:%m:%d')
            date_of_photo = datetime.datetime(*date_of_photo_temp[:3])
            date_of_photo = datetime.date(year = date_of_photo.year, month = date_of_photo.month,
                                          day = date_of_photo.day)
            print("date_of_photo", date_of_photo, type(date_of_photo))

            photo_emotion_dict = self.get_emotion_dict(photo_file_path)
            if photo_emotion_dict:
                print ("photo_emotion_dict: ", photo_emotion_dict)
                photo_emotion_dict = photo_emotion_dict['scores']
            else:
                continue
            pp.pprint(photo_emotion_dict)
            pp.pprint(type(photo_emotion_dict))

            if self.date_photo_emotion_dict[date_of_photo]['dict']:
                self.date_photo_emotion_dict[date_of_photo]['dict'] = add_dicts_value(
                    self.date_photo_emotion_dict[date_of_photo]['dict'], photo_emotion_dict)
            else:
                self.date_photo_emotion_dict[date_of_photo]['dict'] = photo_emotion_dict

            self.date_photo_emotion_dict[date_of_photo]['dict_num'] += 1

        # compute the average of date_photo_emotion_dict
        for date, date_dict in self.date_photo_emotion_dict.items():
            dict_num = date_dict['dict_num']
            for emotion, emotion_value in self.date_photo_emotion_dict[date]['dict'].items():
                emotion_value /= dict_num
                self.date_photo_emotion_dict[date]['dict'][emotion] = float("{:.3f}".format(emotion_value))
        pp.pprint(self.date_photo_emotion_dict)




    def get_text_emotion_dict(self):

        texts_name_list = os.listdir(self.text_folder_path)
        texts_path_list = [os.path.join(self.text_folder_path, x) for x in texts_name_list]
        for text_file in texts_path_list:
            with open(text_file, 'r', encoding = 'utf-8') as f:
                date_str = re.findall(r'([0-9]+-[0-9]+-[0-9]+)#', f.name)[0]
                print ("date_str :", date_str)
                date_of_text_temp = time.strptime(date_str, '%Y-%m-%d')
                date_of_text = datetime.datetime(*date_of_text_temp[:3])
                date_object = datetime.date(year=date_of_text.year, month=date_of_text.month,
                                              day=date_of_text.day)
                text_content_list = f.readlines()
                text_content = '.'.join(text_content_list)
                text_content_re_list = re.findall(r'[A-Za-z]+', text_content)
                text_content = '.'.join(text_content_re_list)[0:80000]
                #print ('text_content: ', text_content)
                request_dict = {}
                request_dict['language'] = "english"
                request_dict['text'] = text_content
                response = requests.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                                        headers={
                                            "X-Mashape-Key": "muMV4DdXyqmsh6hEQIryzApEFo4bp14Nb8ojsnQZdTCaEAUMxo",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Accept": "application/json"
                                        },
                                        data = request_dict
                                        )
                print(response.status_code)
                response_dict = response.json()['probability']
                response_dict['emotion_value'] = response_dict['pos'] - response_dict['neg']
                print(response_dict)
                if self.date_text_emotion_dict[date_object]:
                    logger1.error("{} has mutilple copies".format(date_object))
                self.date_text_emotion_dict[date_object] = response_dict
        pp.pprint(self.date_text_emotion_dict)






    def plot_emotion_trend(self, mode = 'photo'):
        if mode == 'photo':
            sorted_date_photo_emotion_list = sorted(self.date_photo_emotion_dict.items(), key = lambda x:x[0])
            date_list = [x[0] for x in sorted_date_photo_emotion_list]
            anger_list = []
            contempt_list = []
            disgust_list = []
            fear_list = []
            happiness_list = []
            neutral_list = []
            sadness_list = []
            surprise_list = []
            # "anger"
            # "contempt"
            # "disgust"
            # "fear"
            # "happiness"
            # "neutral"
            # "sadness"
            # "surprise"
            for date, date_dict in sorted_date_photo_emotion_list:
                anger_list.append(date_dict['dict']['anger'])
                contempt_list.append(date_dict['dict']['contempt'])
                disgust_list.append(date_dict['dict']['disgust'])
                fear_list.append(date_dict['dict']['fear'])
                happiness_list.append(date_dict['dict']['happiness'])
                neutral_list.append(date_dict['dict']['neutral'])
                sadness_list.append(date_dict['dict']['sadness'])
                surprise_list.append(date_dict['dict']['surprise'])

            # plot
            plt.plot(date_list, anger_list, 'b-', label="anger")
            plt.plot(date_list, contempt_list, 'g-', label="contempt")
            plt.plot(date_list, disgust_list, 'r-', label="disgust")
            plt.plot(date_list, fear_list, 'c-', label="fear")
            plt.plot(date_list, happiness_list, 'm-', label="happiness")
            plt.plot(date_list, neutral_list, 'y-', label="neutral")
            plt.plot(date_list, sadness_list, 'k-', label="sadness")
            plt.plot(date_list, surprise_list, 'w-', label="surprise")
            plt.title('Photo Emotion Trend')
            plt.legend(loc=2)
            path = os.path.join("result", 'photo_emotion_trend.png')
            plt.savefig(path)
            plt.show()
        elif mode == 'text':
            sorted_date_text_emotion_list = sorted(self.date_text_emotion_dict.items(), key=lambda x: x[0])
            date_list = [x[0] for x in sorted_date_text_emotion_list]
            emotion_value_list = [x[1]['emotion_value'] for x in sorted_date_text_emotion_list]
            emotion_value_list = [float("{:.2f}".format(x)) for x in emotion_value_list]
            plt.plot(date_list, emotion_value_list, 'ro', label="anger")
            plt.title('Text Emotion Trend')
            plt.legend(loc=2)
            path = os.path.join("result", 'text_emotion_trend.png')
            plt.savefig(path)
            plt.show()










