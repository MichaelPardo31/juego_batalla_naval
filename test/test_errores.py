from src.btn.tablero import Tablero


def test_barco_fuera_limites():
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 3, 5, "H") is False

def test_barco_tamano_cero():
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 0, 0, "H") is False  

def test_barco_negativo():
    tablero = Tablero(5, 5)
    assert tablero.colocar_barco(0, 0, -3, "H") is False 
