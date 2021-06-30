from flask import Blueprint,render_template,request

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append('E:\Final_project\KoSpeech\\bin')
sys.path.append('E:\Final_project\KoSpeech\wavelet_denoiser\src')

from denoiser_argument import denoises
from inference import sinfer
from TalkBot.Call_talkBot import CTalkBot
from Global import Global_veriable
import pprint

bp = Blueprint('main', __name__, url_prefix='/')
# --------------------------------- [edit] ---------------------------------- #
@bp.route('/record',methods = ['POST'])
def record():
    data = request.form["result"]
    show = Global_veriable.CTB_v.call_talkbot(query=data)
    # pprint.pprint(show)
    show_message=show["replies"]
    for i in range(len(show_message)):
        print(show_message[i]["message"])
    return render_template("index.html")

@bp.route('/upload', methods=['POST'])
def upload():

    imd = request.form
    tmp = imd.getlist('base64')[0]
    blob = imd.getlist('audio')
    print(imd)
    print(blob)
    
    tmp = tmp.split(',')
    # print(tmp)
    wav_file = open("temp.webm", "wb")   
    decode_string = base64.b64decode(tmp[1])
    # print(decode_string)
    wav_file.write(decode_string)
        
    return render_template('question/test.html')

@bp.route('/')
def index():
    Global_veriable.CTB_v=CTalkBot('02927ec8-57aa-4d20-b468-b06c18dfa8df')
    return render_template("index.html")
# --------------------------------------------------------------------------- #