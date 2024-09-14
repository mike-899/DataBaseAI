import pyaudio
import threading
import wave
import pyaudio
import whisper
from TTS.api import TTS

# Configuración de parámetros de grabación
formato = pyaudio.paInt16  # Formato de la señal
canales = 1  # Canales mono
frecuencia_muestreo = 44100  # Frecuencia de muestreo
tamaño_bloque = 1024  # Tamaño de cada bloque de audio
nombre_archivo = "pregunta.wav"  # Nombre del archivo de salida
respuesta_archivo = "respuesta.wav"  # Nombre del archivo de respuesta
indice_microfono = 2  # Cambia este índice al que corresponda a tu micrófono

model = whisper.load_model("small")

tts = TTS(model_name="tts_models/es/css10/vits")

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'