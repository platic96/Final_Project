from flask import Blueprint, render_template, request, jsonify
from flask import Flask, session
from .stt import stt
from .tts import tts
from TalkBot.Call_talkBot import CTalkBot
from .webm2wav import webm2wav

from TalkBot.talkBotObject import TalkBot

# 아이디 매핑 ( Secretkey, AccessKey )
minjae = {"secretkey":"GW01NgJHYxx8VRRE4oVb5xcpm5rDcENJyEqKHsie", "accesskey":"Kjd7XuRjnwmHHMmaMHDjzNjUTjqwpFjHtw0C8Wjd", "name":"김민재"}
younsock = {"secretkey":"GW01NgJHYxx8VRRE4oVb5xcpm5rDcENJyEqKHsie", "accesskey":"Kjd7XuRjnwmHHMmaMHDjzNjUTjqwpFjHtw0C8Wjd", "name":"허윤석"}


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

    
    # 임시 데이터 처리
    text = ["허윤석"]


    #로그인 아이디가 정확히 들어왔을 경우
    message = []
    if (text[0] == "허윤석") :
        # 톡봇에 음성인식 결과 전달 (텍스트 전달)
        session['user'] = text[0]
        TalkBot.talkBot.conversation(younsock["accesskey"])
        message = TalkBot.talkBot.conversation(younsock["secretkey"])

    #톡봇 답변 출력 및 음성합성
    outmessage = []
    outpath = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], session['user']))

    data = {'message': outmessage,'inputmessage':text,'path': outpath}
    
    return jsonify(data)


@bp.route('/session', methods=['POST'])
def sessionCheck() :
    if 'user' not in session :
        data = {'session' : 'None'}
    else :
        data = {'session' : session['user']}

    return jsonify(data)

