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
	
	-preparacion: se necesitan 2 jugadores con: 2 tableros(matrices) que tengan dos ejes x,y que tengan numeros(10) y letras(10 a-j) cada uno. / piezas de anotaciones para cada acierto(amarillo), otros de otro color para los fallos(blanco), piezas de barcos de diferentes longitudes ( 5 para cada jugador) no es necesario tener muchos barcos pero es necesario que los dos jugadores tengan flotas iguales en numero y longitud
	
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

implementacion:

	se veran por pantalla 2 matrices (1) la nuestra de barcos y (2) del juego(maquina) donde solo veremos donde tiramos nuestros disparos y se veran los aciertos o fallas
	marcando con (🌊)fallos, (🟠)aciertos . Gana el primer jugador que hunda todos los barcos del otro.
	