from flask import Blueprint, render_template, request, jsonify
from flask.globals import session
from TalkBot.Call_talkBot import CTalkBot
from .tts import tts

bp = Blueprint('talkBot', __name__, url_prefix='/talkBot')

talkBot = None

# 톡봇 시작
@bp.route('/', methods=['POST'])
def initTalkBot() :

    global talkBot
    # ajax 데이터 가져오기
    params = request.get_json()

    # ajax 데이터에 톡봇아이디가 존재하면 해당 아이디로 톡봇객체생성
    # ajax 데이터에 톡봇아이디가 존재하지 않으면 Call_talkBot.py에 있는 default value로 톡봇객체 생성
    if params['talkBotId'] == "noTalkBotId" :
        talkBot = CTalkBot()
    else :
        talkBot = CTalkBot(params['talkBotId'])

    # 시작메시지 출력
    conv_id, start_message = talkBot.start_conversation()

    outmessage = []
    for i in range(len(start_message['replies'])) :
        outmessage.append(start_message['replies'][i]['message'])

    data = {'message': outmessage}

    return jsonify(data)

# 톡봇 대화
@bp.route('/conv', methods=['POST'])
def conversationTalkBot() :
    global talkBot

    # ajax 데이터(입력메세지) 가져오기
    params = request.get_json()
    # 톡봇에 입력메시지 전달
    message = talkBot.conversation(params['message'])

    # 메시지 만들어서 출력
    outpath = []
    outmessage = []
    for i in range(len(message['replies'])) :
        outmessage.append(message['replies'][i]['message'])
        outpath.append(tts(message['replies'][i]['message'], '김민재'))
        #세션 추가필요
        #outpath.append(tts(message['replies'][i]['message'], session['user']))
    
    data = {'message': outmessage,'path': outpath}

    return jsonify(data)
    

    
