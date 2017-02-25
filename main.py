import os,http, http.client, urllib.request, urllib.parse, urllib.error, base64
import pprint
pp = pprint.PrettyPrinter(indent=4)

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
   data = response.read()
   pp.pprint(data)
   conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))