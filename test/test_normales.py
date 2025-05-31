from src.btn.jugador import Jugador
from src.model.tablero import Tablero


# Comentar tests de autenticación de Jugador ya que la lógica se movió a la base de datos
# def test_autenticacion_correcta():
#     """
#     Prueba la autenticación de un jugador con la contraseña correcta.
#
#     Se intenta autenticar un usuario llamado "Arroz" con la contraseña correcta ("agua123").
#     
#     Se espera que `autenticar` retorne True.
#     """
#     assert Jugador.autenticar("Arroz","agua123") is True

# def test_autenticacion_incorrecta():
#     """
#     Prueba la autenticación de un jugador con una contraseña incorrecta.
#
#     Se intenta autenticar un usuario llamado "Arroz" con una contraseña incorrecta ("123agua").
#     
#     Se espera que `autenticar` retorne False.
#     """
#     assert Jugador.autenticar("Arroz","123agua") is False

def test_creacion_tablero():
    """
    Prueba la correcta creación de un tablero con dimensiones específicas.

    Se crea un tablero de 5x5 y se verifica que la matriz tenga las dimensiones correctas.
    
    Se espera que `tablero.matriz` tenga 5 filas y cada fila contenga 5 columnas.
    """
    tablero = Tablero(5, 5)
    assert len(tablero.matriz) == 5
    assert len(tablero.matriz[0]) == 5
