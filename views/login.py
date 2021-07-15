from flask import Blueprint, render_template, request, jsonify
from flask import Flask, session
from .stt import stt
from .tts import tts
from TalkBot.Call_talkBot import CTalkBot
from .webm2wav import webm2wav

from TalkBot.talkBotObject import TalkBot

# 아이디 매핑 ( Secretkey, AccessKey )



login = [
    {"ko_name":"김민재","en_name":"minjaeKim"},
    {"ko_name":"허윤석","en_name":"yunsockHuh"}
]


bp = Blueprint('login', __name__ , url_prefix='/login')

@bp.route('/', methods=['POST'])
def login() :
    # blob(음성) 데이터 받기
    base64data = request.form
    prebase64 = base64data.getlist('base64')[0]

    # webm to wav 변환 및 
    webm2wav(prebase64)

    # 음성인식 결과 도출
    text = stt()

    # 톡봇에 음성인식 결과 전달 (텍스트 전달)
    message = TalkBot.talkBot.conversation(text[0])
    session['user'] = message['replies'][0]['message'][-7:]
    
    for i in range(len(login)) :
        if login[i]['ko_name'] == session['user'] :
            session['user_en'] = login[i]['en_name']

    #톡봇 답변 출력 및 음성합성
    outmessage = []
    outpath = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], session["en_name"]), i)

    data = {'message': outmessage,'inputmessage':text,'path': outpath}
    
    return jsonify(data)


@bp.route('/session', methods=['POST'])
def sessionCheck() :
    if 'user' not in session :
        data = {'session' : 'None'}
    else :
        data = {'session' : session['user']}

    return jsonify(data)

