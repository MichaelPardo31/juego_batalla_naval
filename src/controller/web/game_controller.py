from flask import Blueprint, request, jsonify
from src.model.db import Database
from src.model.batalla_naval import BatallaNaval
from src.model.barco import Barco
from src.model.tablero import Tablero

# Crear un Blueprint para las rutas del juego
game_bp = Blueprint('game', __name__)

# Diccionario para almacenar las instancias del juego por usuario (simplificado para demostración)
# CONSIDERAR: Mover esto a un lugar más apropiado para manejar sesiones de juego de manera más robusta
game_instances = {}

# Obtener la instancia de la base de datos (asumimos que ya está conectada en app_web.py)
# Esto podría necesitar un ajuste en cómo se pasa la instancia de DB
# Por ahora, asumimos que Database puede manejar múltiples conexiones o es accesible globalmente (no ideal)
# Una mejor práctica sería pasar la instancia de db a este controlador o usar un patrón de inyección de dependencias
# db = Database(dbname="batallaa-navaal", user="postgres", password="root") # No inicializar aquí, usar la de app_web
db = None # Placeholder - la instancia real se pasará o importará de alguna manera

def init_game_controller(database_instance):
    global db
    db = database_instance

# Ruta para iniciar sesión
@game_bp.route('/login', methods=['POST'])
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
@game_bp.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if db.create_user(username, password):
        return jsonify({'success': True, 'message': 'Cuenta creada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'El usuario ya existe'}), 400

# Ruta para iniciar el juego
@game_bp.route('/start_game', methods=['POST'])
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
    if filas < 10 or columnas < 10 or num_barcos < 1: # Ajustar mínimo de barcos a 1 para pasar validación simple
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

        game.colocar_barcos_computadora(num_barcos, barco_size_computadora) # Modificar esta llamada si la función acepta tamaño
        game.barcos_jugador_pendientes = num_barcos # Guardar cuántos barcos le faltan al jugador
        game.barcos_jugador = [] # Inicializar lista de barcos del jugador (para colocación manual)

        game_instances[username] = game # Almacenar la instancia del juego

        # Devolver el estado inicial del tablero del jugador (vacío) y la cantidad de barcos a colocar
        # Es mejor devolver solo la estructura o un estado vacío para la colocación inicial
        player_board_state = game.tablero_jugador.matriz # Devuelve la matriz inicial con agua

        return jsonify({'success': True, 'player_board': player_board_state, 'ships_to_place': num_barcos})

    except Exception as e:
        print(f"Error al iniciar el juego para el usuario {username}: {e}")
        return jsonify({'success': False, 'message': f'Error interno al iniciar el juego: {e}'}), 500

# Ruta para manejar la colocación de barcos del jugador
@game_bp.route('/place_ship', methods=['POST'])
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
    # Asegurarse de que la colocación sea dentro de los límites del tablero antes de llamar a colocar_barco
    if not (0 <= fila < game.filas and 0 <= columna < game.columnas): # Validar límites antes de llamar a colocar_barco
         return jsonify({'success': False, 'message': 'Posición inicial fuera de los límites del tablero.'}), 400

    # La lógica de verificar_posicion en tablero.py puede usarse si es necesaria una validación adicional de posición única (no solo superposición)

    barco = Barco(ship_size)
    if game.tablero_jugador.colocar_barco(fila, columna, ship_size, orientacion): # colocar_barco ya verifica superposición y límites
        # Si la colocación fue exitosa, añadir el barco a la lista del jugador y decrementar el contador
        # Nota: colocar_barco en Tablero solo actualiza la matriz. Aquí es donde se maneja la lista de barcos del jugador
        # y el contador pendiente.

        # Encontrar el barco recién colocado en la matriz y agregarlo a la lista del jugador
        # Esto requiere que colocar_barco devuelva las posiciones o iterar sobre el tablero. O modificar Tablero.colocar_barco
        # para que devuelva el objeto barco o sus posiciones. O crear el barco *antes* de llamar a colocar_barco
        # y pasar el objeto barco a colocar_barco.
        # Opción 1 (simple): Asumir que colocar_barco tuvo éxito y crear el objeto Barco aquí.
        # Esto no es ideal porque el objeto Barco no está realmente vinculado a la matriz del tablero en esta lógica.
        # La matriz del tablero (`tablero_jugador.matriz`) tiene los 'O', pero el objeto Barco tiene las posiciones lógicas.
        # La lógica de verificar_barco_hundido depende de que los objetos Barco tengan las posiciones correctas.

        # Vamos a ajustar la lógica: crear el objeto Barco *antes* y pasarlo, o hacer que colocar_barco lo maneje.
        # Ajustando colocar_barco para que reciba el objeto Barco es una mejor abstracción.
        # Por ahora, sigamos con la lógica actual y ajustemos la adición a la lista de barcos del jugador.
        # Podemos encontrar las posiciones 'O' recién colocadas para el tamaño y orientación dados.

        # Simplificación: Asumir que si colocar_barco regresa True, el barco de tamaño ship_size fue colocado
        # a partir de (fila, columna) con la orientación dada. Crear el objeto Barco con esas posiciones.
        nuevo_barco = Barco(ship_size)
        for i in range(ship_size):
            r, c = (fila + i, columna) if orientacion == "V" else (fila, columna + i)
            nuevo_barco.agregar_posicion(r, c)

        game.barcos_jugador.append(nuevo_barco)
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
@game_bp.route('/shoot', methods=['POST'])
def shoot():
    data = request.json
    fila = data.get('fila')
    columna = data.get('columna')
    username = data.get('username') # Asumimos que el frontend envía el usuario logueado

    # Añadir impresiones para depuración de disparo
    print(f"JSON recibido en /shoot: {data}")
    print(f"Datos recibidos en /shoot: fila={fila}, columna={columna}, username={username}")
    print(f"Tipos de datos recibidos: fila={type(fila)}, columna={type(columna)}")

    if username not in game_instances or game_instances[username] is None:
         return jsonify({'success': False, 'message': 'Juego no iniciado o sesión expirada'}), 400

    game = game_instances[username]

    if game.barcos_jugador_pendientes > 0:
         return jsonify({'success': False, 'message': 'Aún debes colocar tus barcos antes de disparar.'}), 400

    # Convertir a enteros
    try:
        # fila y columna ya deberían ser 0-indexed desde el frontend
        fila = int(fila)
        columna = int(columna)
    except (ValueError, TypeError):
        # Esto no debería ocurrir si el frontend valida, pero es una red de seguridad
        return jsonify({'success': False, 'message': 'Las coordenadas de fila o columna del disparo no son números válidos.'}), 400

    # Validar disparo (asegurarse de que la posición esté dentro de los límites y no haya sido disparada)
    # La función disparo_jugador en BatallaNaval debería manejar la validación si ya fue disparada y límites
    # Re-validar límites aquí por seguridad antes de llamar a disparo_jugador

    # Añadir impresiones para depurar la validación de límites
    print(f"Validando disparo en backend: fila={fila}, columna={columna}")
    print(f"Límites del tablero en backend: filas={game.filas}, columnas={game.columnas}")

    if not (0 <= fila < game.filas and 0 <= columna < game.columnas): # Validar límites
         return jsonify({'success': False, 'message': 'Posición de disparo fuera de los límites.'}), 400

    # Realizar disparo del jugador
    # La lógica del backend ya maneja el turno de la computadora después del disparo del jugador
    disparo_resultado_jugador, juego_terminado_jugador = game.disparo_jugador(fila, columna)

    if disparo_resultado_jugador == 'ya_disparado':
         # Si el backend detecta que ya se disparó, devuelve un mensaje específico
         return jsonify({'success': False, 'message': 'Ya habías disparado en esta posición.'}), 400 # Usar 400 Bad Request

    # Verificar si el juego ha terminado después del disparo del jugador
    if juego_terminado_jugador:
        # Limpiar la instancia del juego al finalizar (opcional, depende de la lógica de sesiones)
        # del game_instances[username] # Considerar si esto es deseable
        return jsonify({
            'success': True,
            'result': 'jugador',
            'game_over': True,
            'message': '¡Felicidades! ¡Has ganado!',
            'player_board': game.tablero_jugador.matriz, # Enviar el estado final de los tableros
            'computer_board': game.tablero_computadora.matriz
            })

    # Turno de la computadora (solo si el jugador no ganó)
    comp_fila, comp_col, disparo_resultado_comp, juego_terminado_comp = game.disparo_computadora()

    # Devolver el estado actualizado de ambos tableros y detalles del turno de la computadora
    response_data = {
        'success': True,
        'game_over': juego_terminado_comp is not None, # Verificar si el juego terminó después del disparo de la compu
        'result': disparo_resultado_jugador, # Resultado del disparo del jugador
        'player_board': game.tablero_jugador.matriz, # Enviar el estado actualizado de los tableros
        'computer_board': game.tablero_computadora.matriz,
        'computer_shot': {
            'fila': comp_fila,
            'columna': comp_col,
            'resultado': disparo_resultado_comp
            },
        'message': 'Turno completado.' # Mensaje general
    }

    if juego_terminado_comp:
         response_data['message'] = '¡Derrota! La computadora ha ganado.'
    elif disparo_resultado_jugador == 'hundido':
         response_data['message'] = '¡Barco enemigo hundido!\n'
    elif disparo_resultado_jugador == 'impacto':
         response_data['message'] = '¡Impacto en barco enemigo!\n'
    else:
         response_data['message'] = '¡Agua!\n'

    return jsonify(response_data) 