# Copyright (c) 2020, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
#경로 수정
sys.path.append('/usr/test/Final_project/SpeechRecognition')
sys.path.append('/usr/test/Final_project/SpeechRecognition/wavelet_denoiser/src')
import torch
import torch.nn as nn
import numpy as np
import torchaudio
from torch import Tensor
import wave
import librosa
import soundfile as sf
import os
from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.data.audio.core import load_audio

from kospeech.models import (
    DeepSpeech2,
    ListenAttendSpell,
)

from wavelet_denoiser.src.denoiser_argument import *
from wavelet_denoiser.src.denoise import *
import wave
import librosa
import soundfile as sf


class Synthesizer_Kospeech:
    def __init__(self):
        parser = argparse.ArgumentParser(description='KoSpeech')
        parser.add_argument('--model_path', type=str, required=False, default='/usr/test/Final_project/modellocation/model.pt')
        parser.add_argument('--audio_path', type=str, required=False, default='SpeechRecognition/Record_sample/file.wav')
        parser.add_argument('--device', type=str, required=False, default='cpu')
        self.opt = parser.parse_args()

    def parse_audio(self, audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm') -> Tensor:
        signal = load_audio(audio_path, del_silence, extension=audio_extension)
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)

        return torch.FloatTensor(feature).transpose(0, 1)

    def sampling(self, input, resample_sr=16000):
        wav = wave.open(input, "rb")
        y, sr = librosa.load(input, sr=wav.getframerate())
        resample = librosa.resample(y, sr, resample_sr)
        sf.write(input, resample, 16000, format='WAV',  endian='LITTLE',subtype='PCM_16')
        print("샘플링 성공")

        


    #denoises()
    #sinfer()
    ############################샘플링코드##############################
    ###################################################################

    def sinfer(self):
        self.sampling(self.opt.audio_path, 16000)
        feature = self.parse_audio(self.opt.audio_path, del_silence=True)
        input_length = torch.LongTensor([len(feature)])
        vocab = KsponSpeechVocabulary('SpeechRecognition/data/vocab/aihub_character_vocabs.csv')

        model = torch.load(self.opt.model_path, map_location=lambda storage, loc: storage).to(self.opt.device)
        if isinstance(model, nn.DataParallel):
            model = model.module
        model.eval()

        if isinstance(model, ListenAttendSpell):
            model.encoder.device = self.opt.device
            model.decoder.device = self.opt.device

            y_hats = model.recognize(feature.unsqueeze(0).float().cuda(), input_length)
        elif isinstance(model, DeepSpeech2):
            model.device = self.opt.device
            y_hats = model.recognize(feature.unsqueeze(0), input_length)
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
        return sentence






