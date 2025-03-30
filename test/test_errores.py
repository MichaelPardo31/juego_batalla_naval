from src.btn.tablero import Tablero


def test_barco_fuera_limites():
    """
    Prueba que un barco no pueda colocarse si excede los límites del tablero.

    Crea un tablero de 5x5 y trata de colocar un barco de tamaño 5 en la posición (0,3) 
    con orientación horizontal, lo que lo haría salir del tablero.
    
    Se espera que `colocar_barco` retorne False.
    """
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 3, 5, "H") is False

def test_barco_tamano_cero():
    """
    Prueba que un barco de tamaño 0 no pueda colocarse en el tablero.

    Crea un tablero de 5x5 e intenta colocar un barco con tamaño 0 en la posición (0,0). 
    
    Se espera que `colocar_barco` retorne False.
    """
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 0, 0, "H") is False  

def test_barco_negativo():
    """
    Prueba que un barco con tamaño negativo no pueda colocarse en el tablero.

    intenta colocar un barco de tamaño -3 en la posición (0,0).
    
    Se espera que `colocar_barco` retorne False.
    """
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 0, -3, "H") is False 
