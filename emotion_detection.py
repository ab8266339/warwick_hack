import os,http, http.client, urllib.request, urllib.parse, urllib.error, base64
import pprint
import os
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

    def get_emotion_dict(self):
        pass
















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

file = open('face/recognition1.jpg', "rb").read()

try:
   conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
   conn.request("POST", "/emotion/v1.0/recognize?%s" % params, file, headers)
   print("send request")
   response = conn.getresponse()
   data = response.json()
   pp.pprint(data)
   conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))