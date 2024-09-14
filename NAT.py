import re
from num2words import num2words  # Asegúrate de importar la función correcta

def mover_simbolo_dinero(texto):
    # Expresión regular para encontrar los casos de $ seguido de números
    return re.sub(r'\$(\d+)', r'\1 $', texto)

def numATex(texto):
    texto = mover_simbolo_dinero(texto)
    # Función para reemplazar un número por su palabra en español
    def convertir_a_palabra(coincidencia):
        numero = int(coincidencia.group())
        return num2words(numero, lang='es')

    # Primero, reemplazamos los números por palabras
    texto = re.sub(r'\d+', convertir_a_palabra, texto)
    
    # Luego, reemplazamos el símbolo $ por la palabra "pesos"
    texto = re.sub(r'\$', 'pesos', texto)
    
    return texto