#funciones extra para la app users
import re
import random
import string

def generador_cod(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def hay_numeros(string):
   return bool(re.search(r'\d', string))
