from django.contrib.auth.models import User
import re

def validar_existencia_usuario(usuario):
    if User.objects.filter(username=usuario).exists():
        return False
    return True

def limpiar_telefono(telefono):
    telefono_limpio = re.sub(r'[^\d]', '', telefono)
    return telefono_limpio

def validar_formato_telefono(telefono):
    telefono_limpio = limpiar_telefono(telefono)

    if len(telefono_limpio) >= 10 and len(telefono_limpio) <= 15:
        return True
    else:
        return False

def validar_formato_correo(correo):
    correo_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(correo_regex, correo):
        return True
    else:
        return False

def validar_formato_password(password):
    print(password)
    if password is None:
        return False
    return len(password) >= 8

def validar_formato_edad(edad):
    try:
        edad = int(edad)
        if edad < 18 or edad > 100:
            return False
    except ValueError:
        return False
    return True