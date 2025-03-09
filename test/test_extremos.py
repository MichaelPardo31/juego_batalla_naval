from src.btn.tablero import Tablero


def test_tablero_grande():
    tablero = Tablero(100, 100)
    assert len(tablero.matriz) == 100
    assert len(tablero.matriz[0]) == 100

def test_barco_maximo_tamano():
    tablero = Tablero(10, 10)
    assert tablero.colocar_barco(0, 0, 10, "H") is True

def test_barco_ocupa_toda_columna():
    tablero = Tablero(10, 10)
    assert tablero.colocar_barco(0, 0, 10, "V") is True
