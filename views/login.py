from flask import Blueprint, render_template, request, jsonify
from flask.globals import session
from .stt import stt
from .tts import tts
from TalkBot.Call_talkBot import CTalkBot
from .webm2wav import webm2wav

# 아이디 매핑 ( Secretkey, AccessKey )
minjae = {"secretkey":"", "accesskey":"", "name":"김민재"}
younsock = {"secretkey":"", "accesskey":"", "name":"허윤석"}


bp = Blueprint('login', __name__ , url_prefix='/login')

@bp.route('/', methods=['POST'])
def login() :
    # blob(음성) 데이터 받기
    base64data = request.form
    prebase64 = base64data.getlist('base64')[0]

    # webm to wav 변환 및 
    #path = webm2wav(prebase64)
    webm2wav(prebase64)

    # 음성인식 결과 도출
    #text = stt(path)
    text = stt()


    if (text == "허윤석") :
        # 톡봇에 음성인식 결과 전달 (텍스트 전달)
        session['user'] = text
        message = CTalkBot.conversation(younsock["secretkey"])
        message = CTalkBot.conversation(younsock["accesskey"])

    tts(message, session['user'])
    

    return jsonify(message['replies'])



