from flask.globals import session
from tacotron2.inference import Synthesizer_Tacotron
import soundfile as sf

# 음성합성
def tts(text, sessionId, count: int = 0):
   tacotronModel = Synthesizer_Tacotron()
   audio, sampling_rate = tacotronModel.Final(text)
   path = f'static/audio/wav_{sessionId}_{count}.wav'
   sf.write(path, audio, sampling_rate)
   return path

