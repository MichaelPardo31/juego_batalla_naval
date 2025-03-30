import getpass
from src.btn.jugador import Jugador
from src.btn.batalla_naval import BatallaNaval
from src.btn.seguridad import cifrar

class Menu:
    def __init__(self):
        self.juego = None

    def mostrar_menu(self):
        print("\n🌊 Bienvenido a Batalla Naval 🌊")
        print("1. Ingresar al juego")
        print("2. Salir")
    
    def obtener_opcion(self):
        return input("Seleccione una opción: ")

    def iniciar(self):
        nombre = input("Ingrese su nombre de usuario: ")
        password_ingresada = getpass.getpass("Ingrese su contraseña: ")
        contrasenia = cifrar(password_ingresada)

        if not Jugador.autenticar(nombre, contrasenia):
            print("🚫 Acceso denegado")
            return
        
        print("✅ Inicio de sesión exitoso.")
        
        while True:
            self.mostrar_menu()
            opcion = self.obtener_opcion()
            
            if opcion == "1":
                self.iniciar_juego()
                break
            elif opcion == "2":
                print("👋 Saliendo del juego. ¡Hasta pronto!")
                break
            else:
                print("⚠️ Opción no válida, intenta de nuevo.")

    def iniciar_juego(self):
        filas = int(input("Ingrese número de filas del tablero: "))
        columnas = int(input("Ingrese número de columnas del tablero: "))

        self.juego = BatallaNaval(filas, columnas)
        self.juego.tablero.mostrar()

        cantidad_barcos = int(input("¿Cuántos barcos quiere colocar? "))
        self.juego.colocar_barcos(cantidad_barcos)
