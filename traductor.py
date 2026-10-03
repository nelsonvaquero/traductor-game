import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator 

duration = 5 
samplerate = 44100
translator = Translator()

print("habla ahora...")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()

wav.write('output.wav', samplerate, recording)
print("Grabación completada. Procesando...")

idioma = input("A que idioma quieres traducir? (ejemplo 'fr' para francés, 'de' para alemán): ")

recognizer = sr.Recognizer()
with sr.AudioFile('output.wav') as source:
    audio = recognizer.record(source)
    

try:
    text = recognizer.recognize_google(audio, language='es-ES')
    print("Texto reconocido: " + text)
    traduccion = translator.translate(text, src='es', dest=idioma)
    print("Traducción: " + traduccion.text)
except sr.UnknownValueError:
    print("No se pudo entender el audio.")
except sr.RequestError as e:
    print("Error al solicitar resultados; {0}".format(e))