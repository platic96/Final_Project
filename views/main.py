import base64
#import soundfile as sf
# from tacotron2.inference import Synthesizer_Tacotron
import pprint
from Global import Global_veriable
from TalkBot.Call_talkBot import CTalkBot
from SpeechRecognition.bin.inference import Synthesizer_Kospeech
from denoiser_argument import denoises
from flask import Blueprint, render_template, request
import sys, os
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('D:\Final_project\SpeechRecognition\\bin')
sys.path.append('D:\Final_project\SpeechRecognition\wavelet_denoiser\src')

bp = Blueprint('main', __name__, url_prefix='/')
# --------------------------------- [edit] ---------------------------------- #
#음성 message 출력
@bp.route('/sendmes', methods=['POST'])
def sendmes():
    data = request.form["result"]
    show = Global_veriable.CTB_v.call_talkbot(query=data)
    # pprint.pprint(show)
    #필요 없는 부분
    # show_message = show["replies"]
    # for i in range(len(show_message)):
    #     print(show_message[i]["message"])
    # return render_template("index.html")

@bp.route('/record', methods=['POST'])
def record():
    # blob(음성) 데이터 받기
    base64data = request.form
    prebase64 = base64data.getlist('base64')[0]
    prebase64 = prebase64.split(',')

    # webm 파일 생성
    wav_file = open("SpeechRecognition/Record_sample/temp.webm", "wb")
    decode_string = base64.b64decode(prebase64[1])
    wav_file.write(decode_string)

    # webm to wav 변환 및 음성인식 결과 도출
    data = stt()

    # 톡봇에 음성인식 결과 전달 (텍스트 전달)
    show = Global_veriable.CTB_v.call_talkbot(query=data[0])

    # 톡봇 답변 출력 및 음성합성
    show_message = show["replies"]
    for i in range(len(show_message)):
        print(show_message[i]["message"])
        tts(show_message[i]["message"], '아이디', i)

    # tts로 생성한 오디오파일 재생하는부분 필요 (미완성)

    return render_template("index.html")

# 음성합성
# def tts(text, sessionId, count):
#     tacotronModel = Synthesizer_Tacotron()
#     audio, sampling_rate = tacotronModel.inference(text)
#     sf.write('문장_{}_{}.wav'.format(sessionId, count), audio, sampling_rate)

# 음성인식
def stt():
    kospeechModel = Synthesizer_Kospeech()
    text = kospeechModel.sinfer()
    return text

# blob데이터를 음성파일로 변환
def convert_and_split(filename):
    # command = ['ffmpeg', '-y', '-i', filename, 'SpeechRecognition/Record_sample/3.wav']
    # subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    cmd = f'ffmpeg -y -i C:/Users/samsung/PycharmProjects/Final_Project2/SpeechRecognition/Record_sample/3.wav'
    process = subprocess.Popen(cmd, shell=True, stdout=sys.stdout)
    process.wait()

# 음성 인식.
@bp.route('/upload_test', methods=['POST'])
def upload_test():
    name = request.form['name']
    base64_audio = request.form['base64_audio']
    print(base64_audio)
    webm_file = open(f"temp.webm", "wb")
    decode_string = base64.b64decode(base64_audio.split(',')[1])
    webm_file.write(decode_string)

    convert_and_split("temp.webm")
    sinfer()
    return render_template("index.html")
    

@bp.route('/upload', methods=['POST'])
def upload():
    imd = request.form
    tmp = imd.getlist('base64')[0]
    blob = imd.getlist('audio')

    tmp = tmp.split(',')
    # print(tmp)
    wav_file = open("temp.webm", "wb")
    decode_string = base64.b64decode(tmp[1])
    # print(decode_string)
    wav_file.write(decode_string)

    return render_template('question/test.html')
    
@bp.route('/')
def index():
    Global_veriable.CTB_v = CTalkBot('02927ec8-57aa-4d20-b468-b06c18dfa8df')
    return render_template("index.html")
# --------------------------------------------------------------------------- #
