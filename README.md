Juego Batalla Naval

Este proyecto consiste en desarrollar una versión del clásico juego Batalla Naval, inspirado en la
versión que utilizaban los radioperadores militares antes de la invención de los computadores.
La aplicación debe tener las siguientes funcionalidades:
1. Iniciar el campo de juego: Dado un ancho y un alto, la aplicación debe iniciar un campo de
juego con esa dimensiones y naves ubicadas aleatoriamente en él.
2. Acción de disparar: Dada una fila y una columna ingresadas por el usuario, el juego debe
calcular si en esa posición del campo había una nave, debe actualizar el campo de juego y
el puntaje, como también notificar al usuario si ganó el juego o debe continuar.
3. Iniciar sesión: La aplicación debe permitir a los jugadores iniciar sesión en el sistema con
un usuario ya existente
4. Crear cuenta: Los jugadores deben poder darse de alta en el sistema
5. Cambiar contraseña: El sistema debe permitir a los jugadores cambiar sus contraseñas
cuando ellos lo deseen.
6. Visualizar puntuaciones: Los jugadores deben poder ver la tabla de puntuaciones donde
vean su puntaje comparado con el puntaje de los demás jugadores.

---------------------

==caracteristicas y objetivos del juego:==

	-objetivo adivinar las posiciones de todos los barcos de la flota contraria y hundirlos con disparos a todas sus casillas
	
	-preparacion: se necesitan 2 jugadores con: 2 tableros(matrices) que tengan dos ejes x,y cada uno. / piezas de anotaciones para cada acierto(amarillo), otros de otro color para los fallos(blanco), piezas de barcos de diferentes longitudes ( 5 para cada jugador) no es necesario tener muchos barcos pero es necesario que los dos jugadores tengan flotas iguales en numero y longitud
	
	- no es necesario poner los nombres de los barcos pero:
	- portaaviones 5 casillas
	- acorazado 4 casillas
	- destructor & submarino (3casillas)
	- crucero o lancha 2 casillas
	- Restricciones: los barcos deben de ir posicionados en posicion vertical o horizontal (NO diagonal) y no sobrevalen de la cuadricula, los barcos no se pueden poner encima de otros

	- los contricantes no pueden ver los tableros del otro
	-fichas anotadores iguales pa cada uno(sirven para dar aciertos y fallos) 
	inicio (aleatorio)
	
	- DISPAROS:
		se indica la casilla a la que se dirije el ataque por una letra y numero cuadricula.
		el otro jugador responde con la verdad(si la casilla esta ocupada por un barco es acierto) (si no hay nada ocupando el espacio dira AGUA)

==lógica del sistema y modo contra la computadora:==

	- Sistema de IA para la computadora:
		* Algoritmo de colocación de barcos:
			- Distribución aleatoria pero inteligente
			- Evita agrupar barcos en zonas específicas
			- Mantiene distancia mínima entre barcos
		
		* Estrategia de disparos:
			- Modo de búsqueda:
				* Patrón de cuadrícula para cubrir el tablero
				* Disparos sistemáticos por zonas
			- Modo de persecución:
				* Cuando acierta, analiza las casillas adyacentes
				* Determina la dirección del barco
				* Sigue el patrón del barco hasta hundirlo
			- Modo de eliminación:
				* Rodea el barco identificado
				* Verifica casillas adyacentes no disparadas

	- Sistema de juego:
		* Turnos alternados con validación
		* Registro de disparos y aciertos
		* Sistema de puntuación simple
		* Guardado de partidas
		* Estadísticas básicas de juego
	