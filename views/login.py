from flask import Blueprint, render_template, request, jsonify
from flask import Flask, session
from .stt import stt
from .tts import tts
from .webm2wav import webm2wav

from TalkBot.talkBotObject import TalkBot

# 아이디 매핑 ( Secretkey, AccessKey )

IDList = [
    {"ko_name":"김민재","en_name":"minjaeKim"},
    {"ko_name":"허윤석","en_name":"yunsockHuh"}
]


bp = Blueprint('login', __name__ , url_prefix='/login')


# 로그인/로그아웃 처리
@bp.route('/loginout', methods=['POST'])
def loginout() :
    if session.get('user') is None:
        data = login()
    else :
        data = logout()
    
    return jsonify(data)
        


def login() :
    # blob(음성) 데이터 받기
    base64data = request.form
    prebase64 = base64data.getlist('base64')[0]

    # webm to wav 변환 및 
    webm2wav(prebase64)

    # 음성인식 결과 도출
    text = stt()

    # 톡봇에 음성인식 결과 전달 (텍스트 전달)
    #message = TalkBot.talkBot.conversation(text[0])

    # 지우기 (테스트용)
    text = '허윤석'
    message = TalkBot.talkBot.conversation(text)
    

    session['user'] = message['replies'][0]['message'][:-7]
    
    #지우기 (테스트용)
    session['user'] = "허윤석"

    for i in range(len(IDList)) :
        if IDList[i]['ko_name'] == session['user'] :
            session['user_en'] = IDList[i]['en_name']
            print(session['user_en'])

    outmessage = []
    outpath = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], session["user_en"], i))


    #data = {'message': outmessage,'inputmessage':text,'path': outpath}
    #지우기 테스트용
    data = {'message': outmessage,'inputmessage':[text],'path': outpath}
    
    return data


def logout() :

    '''
    로그아웃 처리에는 두가지 방법이 있다.
    1. 로그아웃 음성을 음성인식해서 로그아웃 처리하는방식 (음성인식 인식률이 좋을경우)
    2. 로그인 요청이 들어왔을 때 세션을 체크해서 로그아웃 처리하는방식
    여기선 2번 방법으로 처리하였다.
    '''

    # 톡봇에 로그아웃 데이터 전달
    text = '로그아웃'
    message = TalkBot.talkBot.conversation(text)
    
    outmessage = []
    outpath = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], session["user_en"], i))

    # 세션 초기화
    session.clear()

    data = {'message': outmessage,'inputmessage':[text],'path': outpath}
    
    return data


@bp.route('/session', methods=['POST'])
def sessionCheck() :
    if 'user' not in session :
        data = {'session' : 'None'}
    else :
        data = {'session' : session['user']}

    return jsonify(data)

