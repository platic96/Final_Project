from flask import Blueprint, render_template, request, jsonify
from flask.globals import session
from TalkBot.Call_talkBot import CTalkBot
from views.login import login, logout
from .tts import tts
from .stt import stt
from .webm2wav import webm2wav

from TalkBot.talkBotObject import TalkBot

bp = Blueprint('talkBot', __name__, url_prefix='/talkBot')

# 톡봇 시작
@bp.route('/', methods=['POST'])
def initTalkBot() :

    # ajax 데이터 가져오기
    params = request.get_json()

    # ajax 데이터에 톡봇아이디가 존재하면 해당 아이디로 톡봇객체생성
    # ajax 데이터에 톡봇아이디가 존재하지 않으면 Call_talkBot.py에 있는 default value로 톡봇객체 생성
    if params['talkBotId'] == "noTalkBotId" :
        TalkBot.talkBot = CTalkBot()
    else :
        TalkBot.talkBot = CTalkBot(params['talkBotId'])

    # 시작메시지 출력
    conv_id, start_message = TalkBot.talkBot.start_conversation()

    outmessage = []
    for i in range(len(start_message['replies'])) :
        outmessage.append(start_message['replies'][i]['message'])

    #시작메시지 wavPath 전달 필요
    data = {'message': outmessage}

    return jsonify(data)

# 톡봇 대화
@bp.route('/conv', methods=['POST'])
def conversationTalkBot() :

    # ajax 데이터(입력메세지) 가져오기
    params = request.get_json()

    #로그인일경우
    if params['message'] == "허윤석" :
        session['user'] = "허윤석"
        session['user_en'] = "yunsockHuh"

    #로그아웃 일경우
    if params['message'] == "로그아웃" :
        return jsonify(logout())

    # 톡봇에 입력메시지 전달
    message = TalkBot.talkBot.conversation(params['message'])

    #로그인을 안했을경우 session 처리
    if session.get('user_en') is None :
        wavFileName = 'nologin'
    else :
        wavFileName = session.get('user_en') 
        
    # 메시지 만들어서 출력
    outpath = []
    outmessage = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], wavFileName, i))
    
    data = {'message': outmessage,'path': outpath}

    return jsonify(data)

@bp.route('/convwav', methods=['POST'])
def conversationTalkBot2Wav() :
    # blob(음성) 데이터 받기
    base64data = request.form
    prebase64 = base64data.getlist('base64')[0]
    
    # webm to wav 변환 및 
    #path = webm2wav(prebase64)
    webm2wav(prebase64)

    # 음성인식 결과 도출
    #text = stt(path)
    text = stt()

    #톡봇에 음성인식 결과 전달 (텍스트 전달)
    message = TalkBot.talkBot.conversation(text[0])

    #로그인을 안했을경우 session 처리
    if session.get('user_en') is None :
        wavFileName = 'nologin'
    else :
        wavFileName = session.get('user_en') 

    #톡봇 답변 출력 및 음성합성
    outmessage = []
    outpath = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], wavFileName, i))

    data = {'message': outmessage,'inputmessage':text,'path': outpath}

    return jsonify(data)
    

    
