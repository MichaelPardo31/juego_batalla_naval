from src.btn.tablero import Tablero


def test_tablero_grande():
    """
    Prueba la creación de un tablero de gran tamaño.

    Crea un tablero de 100x100 y verifica que la matriz generada tenga las dimensiones correctas.
    
    Se espera que `tablero.matriz` tenga 100 filas y cada fila contenga 100 columnas.
    """
    tablero = Tablero(100, 100)
    assert len(tablero.matriz) == 100
    assert len(tablero.matriz[0]) == 100

def test_barco_maximo_tamano():
    """
    Prueba la creación de un tablero de gran tamaño.

    Crea un tablero de 100x100 y verifica que la matriz generada tenga las dimensiones correctas.
    
    Se espera que `tablero.matriz` tenga 100 filas y cada fila contenga 100 columnas.
    """
    tablero = Tablero(10, 10)
    assert tablero.colocar_barco(0, 0, 10, "H") is True

def test_barco_ocupa_toda_columna():
    """
    Prueba la colocación de un barco que ocupa toda una columna.

    Crea un tablero de 10x10 e intenta colocar un barco de tamaño 10 en la primera columna
    con orientación vertical.

    Se espera que `colocar_barco` retorne True.
    """
    tablero = Tablero(10, 10)
    assert tablero.colocar_barco(0, 0, 10, "V") is True
