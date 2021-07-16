import base64
from pprint import pprint

from flask.globals import session
from flask.scaffold import F
#import soundfile as sf
#from tacotron2.inference import Synthesizer_Tacotron
from TalkBot.Call_talkBot import CTalkBot
#from SpeechRecognition.bin.inference import Synthesizer_Kospeech
#from denoiser_argument import denoises
from flask import Blueprint, render_template, request
import sys, os
import subprocess
import requests
from Upbit_api.upbit import coin
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append('C:/Users/User/inference_/Final_project/SpeechRecognition/bin')
# sys.path.append('C:/Users/User/inference_/Final_project/SpeechRecognition/wavelet_denoiser/src')

bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/candle', methods=['POST'])
def get_candle():

    params = request.get_json()

    if params['market'] == '':
        market = 'KRW-BTC'
    else :
        market = params['market']

    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": market, "count": "50"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": market, "count": "50"}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
@bp.route('/bitdetail', methods=['GET'])
def bitdetail():
    # print("호출")
    coinData = {
        "coinname":request.args.get("market"),
        "openprice":request.args.get("openprice"),
        "highprice":request.args.get("highprice"),
        "lowprice":request.args.get("lowprice"),
        "tradeprice":request.args.get("tradeprice"),
        }
    have = False
    # Test_my
    session['user'] = "허윤석"
    
     
    if 'user' in session :
        coin_ = coin(session['user'])
        userData = []
        userData = coin_.account()
        
        print(coinData["coinname"][4:])
        for i in range(len(userData)):
            if userData[i]["currency"] == coinData["coinname"][4:]:
                have = True
                percent =round(float(coinData['tradeprice'])/(float(userData[i]['avg_buy_price']))* 100, 2)
                total_price = round(float(coinData['tradeprice'])*(float(userData[i]["balance"])),2)
                return render_template("bitdetail.html", coinData=coinData, userData=userData[i],total_price=total_price,percent=percent,have=have)

    return render_template("bitdetail.html", coinData=coinData,have=have)

@bp.route('/')
def index():

    return render_template("index.html")
# --------------------------------------------------------------------------- #
