import base64
#import soundfile as sf
#from tacotron2.inference import Synthesizer_Tacotron
from TalkBot.Call_talkBot import CTalkBot
#from SpeechRecognition.bin.inference import Synthesizer_Kospeech
#from denoiser_argument import denoises
from flask import Blueprint, render_template, request
import sys, os
import subprocess
import requests
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
    temp1 = request.args.get("market")
    temp2 = request.args.get("openprice")
    temp3 = request.args.get("highprice")
    temp4 = request.args.get("lowprice")
    temp5 = request.args.get("tradeprice")

    print("coinname:"+ temp1+" openprice:"+temp2+" highprice:"+temp3+" lowprice:"+temp4+" tradeprice:"+ temp5)
    return render_template("bitdetail.html", coinname=temp1, openprice=temp2, highprice=temp3, lowprice=temp4, tradeprice=temp5)

@bp.route('/')
def index():

    return render_template("index.html")
# --------------------------------------------------------------------------- #