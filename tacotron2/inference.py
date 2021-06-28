import sys
sys.path.append('E:\Final_project\waveglow')
import numpy as np
import torch

from plotting_utils import plot_spectrogram_to_numpy,save_figure_to_numpy

import soundfile as sf

from hparams import param
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence
import argparse
from text import symbols
# from denoiser import Denoiser

hparams=param()
hparams.sampling_rate = 22050

checkpoint_path = "E:/Final_project/tacotron2/checkpoint_0/checkpoint"

model = Tacotron2(hparams)
model.load_state_dict(torch.load(checkpoint_path)['state_dict'])
_ = model.cuda().eval().half()

waveglow_path = 'E:/Final_project/tacotron2/waveglow/checkpoints/waveglow'
waveglow = torch.load(waveglow_path)['model']
waveglow.cuda().eval().half()
for k in waveglow.convinv:
    k.float()

text = "좀 더 깊이 파라."
sequence = np.array(text_to_sequence(text, ['korean_cleaners']))[None, :]
sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)

audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)

sf.write('문장.wav', audio, hparams.sampling_rate)