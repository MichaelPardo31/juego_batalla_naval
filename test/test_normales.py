from src.btn.jugador import Jugador
from src.btn.tablero import Tablero


def test_autenticacion_correcta():
    assert Jugador.autenticar("Arroz","agua123") is True

def test_autenticacion_incorrecta():
    assert Jugador.autenticar("Arroz","123agua") is False

def test_creacion_tablero():
    tablero = Tablero(5, 5)
    assert len(tablero.matriz) == 5
    assert len(tablero.matriz[0]) == 5
