from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import json
import os
from dotenv import load_dotenv
import urllib.request

load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
url = "https://openapi.naver.com/v1/papago/n2mt"

r = sr.Recognizer()
file_name = 'sample.mp3'

with sr.Microphone() as source:
  print('듣고 있어요')
  audio = r.listen(source)


try:
  text = r.recognize_google(audio, language='ko')
  print(text)
  encText = urllib.parse.quote(text)
  data = "source=ko&target=ja&text=" + encText  
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  response = urllib.request.urlopen(request, data=data.encode("utf-8"))
  rescode = response.getcode()
  if(rescode==200):
    response_body = response.read()
    result = response_body.decode('utf-8')
    d = json.loads(result)
    resultText = d['message']['result']['translatedText']
    print(resultText)
    tts_en = gTTS(text=resultText, lang='ja')
    tts_en.save(file_name)
    playsound(file_name)
    os.remove('sample.mp3')
  else:
    print("Error Code:" + rescode)
except sr.UnknownValueError:
  print('인식 실패')
except sr.RequestError as e:
  print('요청 실패 : ' + e)