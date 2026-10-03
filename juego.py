import sounddevice as sd
import numpy as np 
import speech_recognition as sr
import scipy.io.wavfile as wav
from googletrans import Translator

duration = 5
sample_rate = 44100
translator = Translator()

dif = {
    "easy" : ["verde", "manzana", "perro", "casa", "libro"],
    "medium" : ["elefante", "computadora", "bicicleta", "ventana", "refrigerador"],
    "difficult" : ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
    
}
    

def dificultad():
    nivel = input("elige un nivel de dificultad: easy, medium, difficult\n").strip().lower()
    if nivel in dif:
        palabra = np.random.choice(dif[nivel])
        print("Tu palabra es: " + palabra)
        return palabra
    else:
        print("Nivel de dificultad no válido. Intenta de nuevo.")
        return dificultad()


def traducir(palabra):
    resultado = translator.translate(palabra, src="es", dest="en")
    return resultado.text.lower().strip()
 
 
def grabar_audio():
    print("Grabando... habla ahora")
    grabacion = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("respuesta.wav", sample_rate, grabacion)
    print("Grabación terminada")
 
 
def reconocer_habla():
    reconocedor = sr.Recognizer()
    with sr.AudioFile("respuesta.wav") as fuente:
        audio = reconocedor.record(fuente)
 
    try:
        return reconocedor.recognize_google(audio, language="en-US").lower().strip()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("Error al conectar con el servicio de reconocimiento de voz.")
        return None
 
 
palabra = dificultad()
traduccion_correcta = traducir(palabra)
 
input("Presiona ENTER cuando estés listo para pronunciar la traducción en inglés...")
grabar_audio()
texto_reconocido = reconocer_habla()
 
if texto_reconocido is None:
    print("No se pudo reconocer lo que dijiste.")
    print("La traducción correcta era: " + traduccion_correcta)
else:
    print("Escuché: " + texto_reconocido)
    if texto_reconocido == traduccion_correcta:
        print("¡Correcto!")
    else:
        print("Incorrecto. La traducción correcta era: " + traduccion_correcta)