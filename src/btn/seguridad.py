import hashlib

def cifrar(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# resultado = cifrar("dddd")
# print(resultado)