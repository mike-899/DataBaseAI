from VARS import *

def grabar_audio():
    """
    Función para grabar audio desde el micrófono y guardarlo en un archivo WAV.
    """
    global grabando
    grabando = True
    audio = pyaudio.PyAudio()

    # Crear flujo de entrada especificando el índice del dispositivo de entrada
    flujo = audio.open(format=formato,
                       channels=canales,
                       rate=frecuencia_muestreo,
                       input=True,
                       input_device_index=indice_microfono,
                       frames_per_buffer=tamaño_bloque)

    frames = []

    # Función para detener la grabación

    def detener_grabacion():
        global grabando, fin
        fin = input("\nPresiona 'Enter' para detener la grabación...\n")
        grabando = False

    # Hilo para esperar la tecla 'Enter'
    hilo = threading.Thread(target=detener_grabacion)
    hilo.start()

    print("Grabando...")

    while grabando:
        data = flujo.read(tamaño_bloque)
        frames.append(data)

    print("Grabación detenida.")

    # Detener y cerrar el flujo de entrada
    flujo.stop_stream()
    flujo.close()
    audio.terminate()

    # Guardar los datos grabados en un archivo WAV
    with wave.open(nombre_archivo, 'wb') as wf:
        wf.setnchannels(canales)
        wf.setsampwidth(audio.get_sample_size(formato))
        wf.setframerate(frecuencia_muestreo)
        wf.writeframes(b''.join(frames))

    print(f"Archivo de audio guardado como '{nombre_archivo}'.")


def transcribir_audio():
    """
    Función para transcribir el audio grabado utilizando Whisper.
    """
    result = model.transcribe(nombre_archivo)
    print("Transcripción:", result["text"])
    return result["text"]