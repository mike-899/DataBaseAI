from VARS import *
from NAT import *

def texto_voz(response):
    response = numATex(response)
    tts.tts_to_file(text=response, file_path=respuesta_archivo)

def reproducir_audio(archivo):
    """
    Función para reproducir un archivo de audio WAV.
    """
    with wave.open(archivo, 'rb') as wf:
        audio = pyaudio.PyAudio()
        flujo = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                           channels=wf.getnchannels(),
                           rate=wf.getframerate(),
                           output=True)

        data = wf.readframes(tamaño_bloque)
        while data:
            flujo.write(data)
            data = wf.readframes(tamaño_bloque)

        flujo.stop_stream()
        flujo.close()
        audio.terminate()
    print("Reproducción completada.")