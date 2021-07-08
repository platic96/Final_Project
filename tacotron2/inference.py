import sys
import numpy as np
import torch
import os
import argparse

## WaveGlow 프로젝트 위치 설정
sys.path.append("C:/Users/User/Final")
sys.path.append("C:/Users/User/Final/Final_project/tacotron2")
sys.path.append("C:/Users/User/Final/Final_project/tacotron2/waveglow")
                 
## 프로젝트 라이브러리 Import
from hparams import defaults
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from tacotron2.train import load_model
from text import text_to_sequence
from scipy.io.wavfile import write
import IPython.display as ipd
import json
import sys
from waveglow.glow import WaveGlow
from waveglow.denoiser import Denoiser
from tqdm.notebook import tqdm
#import soundfile as sf

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)      
       
class Synthesizer_Tacotron:
    def __init__(self):
        #tacotron2, waveglow 경로 설정.
        tacotron2_checkpoint = 'C:/Users/User/Inference/tacotron2/checkpoint.pt'
        waveglow_checkpoint = 'C:/Users/User/Inference/tacotron2/waveglow/checkpoints/waveglow.pt'
        hparams = Struct(**defaults)
        hparams.n_mel_channels=80
        hparams.sampling_rate = 22050
        
        self.hparams = hparams
        
        model = load_model(hparams)
        model.load_state_dict(torch.load(tacotron2_checkpoint)['state_dict'])
        model.cuda().eval()#.half()
        
        self.tacotron = model
        
        # waveglow config파일 경로 설정
        with open('C:/Users/User/Inference/tacotron2/waveglow/config.json') as f:
            data = f.read()
        config = json.loads(data)
        waveglow_config = config["waveglow_config"]
        
        waveglow = WaveGlow(**waveglow_config)
        waveglow = self.load_checkpoint(waveglow_checkpoint, waveglow)
        waveglow.cuda().eval()
        
        self.denoiser = Denoiser(waveglow)
        self.waveglow = waveglow
        
    def load_checkpoint(self, checkpoint_path, model):
        assert os.path.isfile(checkpoint_path)
        checkpoint_dict = torch.load(checkpoint_path, map_location='cpu')
        model_for_loading = checkpoint_dict['model']
        model.load_state_dict(model_for_loading.state_dict())
        return model

    def Final(self, text):
        assert type(text)==str, "텍스트 하나만 지원합니다."
        sequence = np.array(text_to_sequence(text, ['korean_cleaners']))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

        mel_outputs, mel_outputs_postnet, _, alignments = self.tacotron.inference(sequence)
        
        
        with torch.no_grad():
            audio = self.waveglow.infer(mel_outputs_postnet, sigma=0.666)
        audio = audio[0].data.cpu().numpy()
        return audio, self.hparams.sampling_rate
    
    ## \n으로 구성된 여러개의 문장 Final 하는 코드
    def Final_phrase(self, phrase, sep_length=4000):
        texts = phrase.split('\n')
        audios = []
        for text in texts:
            if text == '':
                audios.append(np.array([0]*sep_length))
                continue
            audio, sampling_rate = self.Final(text)
            audios.append(audio)
            audios.append(np.array([0]*sep_length))
        return np.hstack(audios[:-1]), sampling_rate
            
    
    def denoise_Final(self, text, sigma=0.666):
        assert type(text)==str, "텍스트 하나만 지원합니다."
        sequence = np.array(text_to_sequence(text, ['korean_cleaners']))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

        mel_outputs, mel_outputs_postnet, _, alignments = self.tacotron.inference(sequence)
               
        with torch.no_grad():
            audio = self.waveglow.infer(mel_outputs_postnet, sigma=0.666)
            
        
        audio_denoised = self.denoiser(audio, strength=0.01)[:, 0].cpu().numpy()
        return audio_denoised.reshape(-1), self.hparams.sampling_rate