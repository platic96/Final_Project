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

@bp.route('/bitdetail', methods=['GET'])
def bitdetail():
    coinname= request.args.get("market")
    openprice = request.args.get("openprice")
    print(coinname+","+openprice)

    return render_template("bitdetail.html")

@bp.route('/')
def index():

    return render_template("index.html")


# --------------------------------------------------------------------------- #