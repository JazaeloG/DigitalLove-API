from django.contrib.auth.models import User
import re

def validar_existencia_usuario(usuario):
    if User.objects.filter(username=usuario).exists():
        return False
    return True

def validar_formato_telefono(telefono):
    if not telefono.isdigit() or len(telefono) < 10 or len(telefono) > 15:
        return False
    return True

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