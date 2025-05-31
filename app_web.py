from flask import Flask, request, jsonify, send_from_directory
import os
from src.model.db import Database
from src.model.batalla_naval import BatallaNaval
from src.model.barco import Barco
from src.model.tablero import Tablero

app = Flask(__name__, static_folder='src/view/web')

# Configuración de la base de datos (reemplaza 'your_db_name')
db = Database(dbname="batallaa-navaal", user="postgres", password="root") # <-- Asegúrate de usar el nombre correcto de tu BD
db.connect()

# Diccionario para almacenar las instancias del juego por usuario (simplificado para demostración)
game_instances = {}

# Ruta para servir la página principal
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Rutas para servir otros archivos estáticos (CSS, JS)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if db.login_user(username, password):
        # Aquí podrías establecer una sesión para el usuario si usas Flask-Login u otro método
        game_instances[username] = None # Inicializar instancia de juego para el usuario
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

# Ruta para crear cuenta
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if db.create_user(username, password):
        return jsonify({'success': True, 'message': 'Cuenta creada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'El usuario ya existe'}), 400

# Ruta para iniciar el juego
@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json

    # Añadir impresión para depurar el JSON recibido
    print(f"JSON recibido en /start_game: {data}")

    filas = data.get('filas')
    columnas = data.get('columnas')
    num_barcos = data.get('num_barcos')
    username = data.get('username') # Asumimos que el frontend envía el usuario logueado

    # Añadir impresiones para depuración
    print(f"Datos recibidos en /start_game: filas={filas}, columnas={columnas}, num_barcos={num_barcos}, username={username}")
    print(f"Tipos de datos: filas={type(filas)}, columnas={type(columnas)}, num_barcos={type(num_barcos)}")

    if username not in game_instances:
         return jsonify({'success': False, 'message': 'Usuario no autenticado o sesión expirada'}), 401

    # Convertir a enteros y validar
    try:
        filas = int(filas)
        columnas = int(columnas)
        num_barcos = int(num_barcos)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Los valores de filas, columnas o número de barcos no son números válidos.'}), 400

    # Validar datos - Añadir validación básica de coherencia
    if filas < 10 or columnas < 10 or num_barcos < 1:
         return jsonify({'success': False, 'message': 'Datos de configuración del juego inválidos (mínimos no cumplidos).'}), 400

    # Validación básica de si el número de barcos es excesivo para el tablero
    # Consideramos excesivo si ocupa más del 50% del tablero con barcos de tamaño mínimo 1
    # Esto es una heurística simple, puede ser necesario ajustarla según el tamaño real de los barcos
    max_posible_barcos = (filas * columnas) // 2 # Estimación simple
    if num_barcos > max_posible_barcos:
         return jsonify({'success': False, 'message': f'El número de barcos es excesivo para el tamaño del tablero. Máximo recomendado: {max_posible_barcos}.'}), 400

    try:
        # Crear instancia del juego para el usuario
        game = BatallaNaval(filas, columnas)

        # Asumiendo que los barcos del jugador son de tamaño fijo 3 como se usó en el frontend
        # Modificar para que la computadora coloque 'num_barcos' de tamaño 3
        barco_size_computadora = 3 # Tamaño fijo para los barcos de la computadora
        # Esta validación ya no es estrictamente necesaria si limitamos el número de barcos por el tamaño del tablero
        # if num_barcos * barco_size_computadora > filas * columnas:
        #      return jsonify({'success': False, 'message': 'El número y tamaño de barcos de la computadora excede el tamaño del tablero.'}), 400

        game.colocar_barcos_computadora(num_barcos, barco_size_computadora) # Modificar esta llamada si la función acepta tamaño
        game.barcos_jugador_pendientes = num_barcos # Guardar cuántos barcos le faltan al jugador
        game.barcos_jugador = [] # Inicializar lista de barcos del jugador (para colocación manual)

        game_instances[username] = game # Almacenar la instancia del juego

        # Devolver el estado inicial del tablero del jugador (vacío) y la cantidad de barcos a colocar
        player_board_state = game.tablero_jugador.matriz

        return jsonify({'success': True, 'player_board': player_board_state, 'ships_to_place': num_barcos})

    except Exception as e:
        print(f"Error al iniciar el juego para el usuario {username}: {e}")
        return jsonify({'success': False, 'message': f'Error interno al iniciar el juego: {e}'}), 500

# Ruta para manejar la colocación de barcos del jugador
@app.route('/place_ship', methods=['POST'])
def place_ship():
    data = request.json
    fila = data.get('fila')
    columna = data.get('columna')
    orientacion = data.get('orientacion')
    username = data.get('username') # Asumimos que el frontend envía el usuario logueado

    if username not in game_instances or game_instances[username] is None:
         return jsonify({'success': False, 'message': 'Juego no iniciado o sesión expirada'}), 400

    game = game_instances[username]

    if game.barcos_jugador_pendientes <= 0:
        return jsonify({'success': False, 'message': 'Todos los barcos ya han sido colocados.'}), 400

    # Convertir a enteros
    try:
        fila = int(fila)
        columna = int(columna)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Las coordenadas de fila o columna no son números válidos.'}), 400

    ship_size = 3 # Tamaño fijo del barco

    # Validar y colocar el barco en el tablero del jugador en el backend
    barco = Barco(ship_size)
    # Asegurarse de que la colocación sea dentro de los límites del tablero antes de llamar a colocar_barco
    if not game.tablero_jugador.verificar_posicion(fila, columna):
         return jsonify({'success': False, 'message': 'Posición inicial fuera de los límites del tablero.'}), 400

    # La lógica de verificar_posicion en tablero.py debería manejar también si ya hay un barco. Si no, se necesitaría otra verificación aquí.

    if game.tablero_jugador.colocar_barco(fila, columna, ship_size, orientacion):
        # Si la colocación fue exitosa, añadir el barco a la lista del jugador y decrementar el contador
        game.barcos_jugador.append(barco)
        game.barcos_jugador_pendientes -= 1

        # Devolver el estado actualizado del tablero del jugador y barcos pendientes
        return jsonify({
            'success': True,
            'player_board': game.tablero_jugador.matriz,
            'ships_remaining': game.barcos_jugador_pendientes,
            'message': 'Barco colocado exitosamente.'
        })
    else:
        # Si la colocación es inválida (por superposición o fuera de límites según la lógica de colocar_barco)
        return jsonify({'success': False, 'message': 'Posición inválida o el barco no cabe/se superpone.'}), 400

# Ruta para manejar el disparo del jugador
@app.route('/shoot', methods=['POST'])
def shoot():
    data = request.json
    fila = data.get('fila')
    columna = data.get('columna')
    username = data.get('username') # Asumimos que el frontend envía el usuario logueado

    if username not in game_instances or game_instances[username] is None:
         return jsonify({'success': False, 'message': 'Juego no iniciado o sesión expirada'}), 400

    game = game_instances[username]

    if game.barcos_jugador_pendientes > 0:
         return jsonify({'success': False, 'message': 'Aún debes colocar tus barcos antes de disparar.'}), 400

    # Convertir a enteros
    try:
        fila = int(fila)
        columna = int(columna)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Las coordenadas de fila o columna del disparo no son números válidos.'}), 400

    # Validar disparo (asegurarse de que la posición esté dentro de los límites y no haya sido disparada)
    # La función disparo_jugador debería manejar la validación si ya fue disparada
    if not game.tablero_computadora.verificar_posicion(fila, columna):
         return jsonify({'success': False, 'message': 'Posición de disparo fuera de los límites o inválida.'}), 400

    # Realizar disparo del jugador
    disparo_exitoso = game.disparo_jugador(fila, columna)

    # Verificar si el juego ha terminado después del disparo del jugador
    resultado = game.verificar_fin_juego()
    if resultado:
        # Limpiar la instancia del juego al finalizar (opcional, depende de la lógica de sesiones)
        # del game_instances[username]
        return jsonify({'success': True, 'result': resultado, 'game_over': True, 'player_board': game.tablero_jugador.matriz, 'computer_board': game.tablero_computadora.matriz})

    # Turno de la computadora
    # Asegurarse de que la computadora realiza un disparo válido
    comp_fila, comp_col = game.disparo_computadora()

    # Verificar si el juego ha terminado después del disparo de la computadora
    resultado_comp = game.verificar_fin_juego()

    # Devolver el estado actualizado de ambos tableros y detalles del turno de la computadora
    response_data = {
        'success': True,
        'game_over': resultado_comp is not None,
        'result': resultado_comp if resultado_comp else ('jugador_continua' if resultado is None else resultado), # Indicar si el jugador ganó o continúa
        'player_board': game.tablero_jugador.matriz,
        'computer_board': game.tablero_computadora.matriz,
        'computer_shot': {'fila': comp_fila, 'columna': comp_col, 'resultado': game.tablero_jugador.obtener_estado_celda(comp_fila, comp_col)} # Añadir resultado del disparo de la compu
    }

    # if resultado_comp:
    #     del game_instances[username]

    return jsonify(response_data)


if __name__ == '__main__':
    # Desconectar de la base de datos al cerrar la aplicación
    import atexit
    atexit.register(lambda: db.disconnect() if db.conn else None)

    # Considerar usar Waitress u otro servidor de producción en lugar de debug=True para producción
    # Para desarrollo, debug=True es útil
    app.run(debug=True) 