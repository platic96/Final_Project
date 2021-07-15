import os
import base64


def webm2wav(base64data) :

    # blob(음성) 데이터 쓰레기데이터 분리
    prebase64 = base64data.split(',')

    #webm 파일 생성
    wav_file = open("SpeechRecognition/Record_sample/temp.webm", "wb")
    decode_string = base64.b64decode(prebase64[1])
    wav_file.write(decode_string)
    
    # webm to wav 변환 
    os.system('ffmpeg -i "/usr/test/Final_project/SpeechRecognition/Record_sample/temp.webm" -vn -acodec copy "/usr/test/Final_project/SpeechRecognition/Record_sample/file.opus" -y')
    os.system('ffmpeg -i "/usr/test/Final_project/SpeechRecognition/Record_sample/file.opus" "/usr/test/Final_project/SpeechRecognition/Record_sample/file.wav" -y')

    #return 
