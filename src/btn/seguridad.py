import hashlib

def cifrar(clave):
    """
    Cifra la clave utilizando SHA-256.

    Args:
        clave (str): La clave que se desea cifrar.
    """
    return hashlib.sha256(clave.encode()).hexdigest()

# resultado = cifrar("dddd")
# print(resultado)