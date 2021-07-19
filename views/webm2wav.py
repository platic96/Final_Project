import os
import base64
from datetime import datetime

def webm2wav(base64data) :

    # blob(음성) 데이터 쓰레기데이터 분리
    prebase64 = base64data.split(',')

    #webm 파일 생성
    wav_file = open("SpeechRecognition/Record_sample/temp.webm", "wb")
    decode_string = base64.b64decode(prebase64[1])
    wav_file.write(decode_string)
    s = datetime.now().strftime('%H_%M_%S')
    # webm to wav 변환 
    os.system(f'ffmeg -i "/usr/test/Final_project/SpeechRecognition/Record_sample/{s}.webm" -vn -acodec copy "/usr/test/Final_project/SpeechRecognition/Record_sample/{s}.opus" -y')
    os.system(f'ffmeg -i "/usr/test/Final_project/SpeechRecognition/Record_sample/{s}.opus" "/usr/test/Final_project/SpeechRecognition/Record_sample/{s}.wav" -y')
