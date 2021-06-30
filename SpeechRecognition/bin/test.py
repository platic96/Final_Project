import sys
sys.path.append('C:/Users/User/Speech/SpeechRecognition/wavelet_denoiser/src')
sys.path.append('C:/Users/User/Speech/SpeechRecognition')

from inference import sinfer

from wavelet_denoiser.src.denoiser_argument import *

from wavelet_denoiser.src.denoise import *

# print(sys.path)

denoises()

sinfer()

