from src.model.batalla_naval import BatallaNaval
import os
import time
import sys
from src.model.db import Database

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_titulo():
    """Muestra el título del juego."""
    print("""
                -----BATALLA NAVAL-----""")

def terminar_partida():
    """Termina la partida actual."""
    limpiar_pantalla()
    print("\nHas terminado la partida.")
    print("Gracias por jugar!")
    sys.exit()

def iniciar_sesion():
    """Maneja el inicio de sesión o registro de usuarios con la base de datos."""
    db = Database(dbname="your_db_name", user="postgres", password="root") # Reemplaza 'your_db_name'
    db.connect()
    
    while True:
        print("\n1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")
            if db.login_user(usuario, contraseña):
                db.disconnect()
                print(f"\n¡Bienvenido, {usuario}!")
                return usuario
            else:
                print("\nIntente de nuevo.")
        
        elif opcion == "2":
            usuario = input("Nuevo usuario: ")
            contraseña = input("Nueva contraseña: ")
            if db.create_user(usuario, contraseña):
                 print("\n¡Cuenta creada exitosamente! Por favor, inicie sesión.")
            else:
                print("\nIntente de nuevo.")
        
        elif opcion == "3":
            db.disconnect()
            terminar_partida()
        
        else:
            print("\nOpción no válida.")

def main():
    """Función principal del juego."""
    limpiar_pantalla()
    mostrar_titulo()
    
    # Iniciar sesión
    usuario = iniciar_sesion()
    input("\nPresiona Enter para comenzar...")

    # Inicializar juego
    while True:
        try:
            filas = int(input("Ingrese el número de filas (mínimo 10) o 0 para salir: "))
            if filas == 0:
                terminar_partida()
            if filas < 10:
                print("El tablero debe tener al menos 10 filas.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")

    while True:
        try:
            columnas = int(input("Ingrese el número de columnas (mínimo 10) o 0 para salir: "))
            if columnas == 0:
                terminar_partida()
            if columnas < 10:
                print("El tablero debe tener al menos 10 columnas.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")

    while True:
        try:
            num_barcos = int(input("Ingrese el número de barcos (mínimo 3) o 0 para salir: "))
            if num_barcos == 0:
                terminar_partida()
            if num_barcos < 3:
                print("Debe haber al menos 3 barcos.")
                continue
            break
        except ValueError:
            print("Por favor ingrese un número válido.")

    # Crear juego
    juego = BatallaNaval(filas, columnas)

    # Colocar barcos
    print("\nColoca tus barcos:")
    print("(Ingresa 0 en cualquier momento para terminar la partida)")
    juego.colocar_barcos_jugador(num_barcos)
    print("\nLa computadora está colocando sus barcos...")
    juego.colocar_barcos_computadora(num_barcos)
    time.sleep(1)

    # Bucle principal del juego
    turno = 1
    while True:
        limpiar_pantalla()
        print(f"\nTurno {turno}")
        print("Ingresa 0 en cualquier momento para terminar la partida")
        
        if turno % 2 != 0:  # Turno del jugador
            print("\nTu turno:")
            print("\nTablero enemigo:")
            juego.tablero_computadora.mostrar()
            
            while True:
                try:
                    fila = int(input("\nIngrese fila para disparar (0 para terminar): ")) - 1
                    if fila == -1:
                        terminar_partida()
                    columna = int(input("Ingrese columna para disparar (0 para terminar): ")) - 1
                    if columna == -1:
                        terminar_partida()
                    
                    if not juego.tablero_computadora.verificar_posicion(fila, columna):
                        print("Posición inválida o ya disparada. Intente de nuevo.")
                        continue
                    
                    if juego.disparo_jugador(fila, columna):
                        break
                except ValueError:
                    print("Por favor ingrese números válidos.")
            
            respuesta = input("\nPresiona Enter para continuar o 0 para terminar: ")
            if respuesta == "0":
                terminar_partida()
        else:  # Turno de la computadora
            print("\nTurno de la computadora:")
            print("\nTu tablero:")
            juego.tablero_jugador.mostrar()
            
            fila, columna = juego.disparo_computadora()
            print(f"\nLa computadora disparó en ({fila + 1}, {columna + 1})")
            
            respuesta = input("\nPresiona Enter para continuar o 0 para terminar: ")
            if respuesta == "0":
                terminar_partida()

        # Verificar fin del juego
        resultado = juego.verificar_fin_juego()
        if resultado:
            limpiar_pantalla()
            if resultado == "jugador":
                print("""
                ¡Felicidades! ¡Has ganado!""")
            else:
                print("""
                ¡Derrota! La computadora ha ganado.""")
            break

        turno += 1

if __name__ == "__main__":
    main()
