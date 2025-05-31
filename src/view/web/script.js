document.addEventListener('DOMContentLoaded', () => {
    const loginSection = document.getElementById('login-section');
    const gameSetupSection = document.getElementById('game-setup-section');
    const gameSection = document.getElementById('game-section');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('login-btn');
    const createAccountBtn = document.getElementById('create-account-btn');
    const messageDiv = document.getElementById('message');
    const filasInput = document.getElementById('filas');
    const columnasInput = document.getElementById('columnas');
    const numBarcosInput = document.getElementById('num_barcos');
    const startGameBtn = document.getElementById('start-game-btn');
    const playerBoardDiv = document.getElementById('player-board');
    const computerBoardDiv = document.getElementById('computer-board');
    const gameMessageDiv = document.getElementById('game-message');
    const placementControlsDiv = document.getElementById('placement-controls');
    const placementMessageDiv = document.getElementById('placement-message');
    const orientationSelect = document.getElementById('orientation');
    const confirmPlacementBtn = document.getElementById('confirm-placement-btn');

    // Nuevos elementos para colocación por input
    const placementRowInput = document.getElementById('placement-row');
    const placementColInput = document.getElementById('placement-col');
    const placeShipBtn = document.getElementById('place-ship-btn');

    // Nuevos elementos para disparo por input
    const shootingControlsDiv = document.getElementById('shooting-controls');
    const shootRowInput = document.getElementById('shoot-row');
    const shootColInput = document.getElementById('shoot-col');
    const shootBtn = document.getElementById('shoot-btn');

    let currentUser = null;
    let placingShip = false;
    let currentShipSize = 3;
    let selectedPlacement = null;
    let shipsToPlaceCount = 0;

    function showMessage(msg, sectionId = 'message') {
        const targetElement = document.getElementById(sectionId);
        if (targetElement) {
            targetElement.textContent = msg;
        }
    }

    function showGameMessage(msg) {
        gameMessageDiv.textContent = msg;
    }

    function showSection(sectionToShow) {
        loginSection.style.display = 'none';
        gameSetupSection.style.display = 'none';
        gameSection.style.display = 'none';
        sectionToShow.style.display = 'flex';
    }

    loginBtn.addEventListener('click', async () => {
        const username = usernameInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                currentUser = username;
                showMessage(data.message);
                showSection(gameSetupSection);
                showMessage('', 'setup-message');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            console.error('Error en inicio de sesión:', error);
            showMessage('Error al intentar iniciar sesión.');
        }
    });

    createAccountBtn.addEventListener('click', async () => {
        const username = usernameInput.value;
        const password = passwordInput.value;

        try {
            const response = await fetch('/create_account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                showMessage(data.message + ' Ahora puedes iniciar sesión.');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            console.error('Error en creación de cuenta:', error);
            showMessage('Error al intentar crear la cuenta.');
        }
    });

    startGameBtn.addEventListener('click', async () => {
        const filas = parseInt(filasInput.value);
        const columnas = parseInt(columnasInput.value);
        const numBarcos = parseInt(numBarcosInput.value);

        if (!currentUser) {
             showMessage("Debes iniciar sesión primero.");
             return;
        }

        if (isNaN(filas) || isNaN(columnas) || isNaN(numBarcos) || filas < 10 || columnas < 10 || numBarcos < 3) {
            showMessage("Por favor ingresa valores válidos para filas (mínimo 10), columnas (mínimo 10) y número de barcos (mínimo 3).", 'setup-message');
            return;
        }

        // Añadir impresiones para depuración
        console.log(`Datos a enviar a /start_game: filas=${filas}, columnas=${columnas}, num_barcos=${numBarcos}, username=${currentUser}`);
        console.log(`Tipos de datos a enviar: filas=${typeof filas}, columnas=${typeof columnas}, num_barcos=${typeof numBarcos}`);

        try {
            // Ocultar el botón de confirmar colocación si aún existe (del modo anterior)
            if (confirmPlacementBtn) confirmPlacementBtn.style.display = 'none';

            const response = await fetch('/start_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filas, columnas, num_barcos: numBarcos, username: currentUser })
            });

            const data = await response.json();

            if (response.ok) {
                showGameMessage("¡Juego iniciado! Coloca tus barcos.");
                showSection(gameSection);
                buildBoard(playerBoardDiv, filas, columnas, true, data.player_board);
                buildBoard(computerBoardDiv, filas, columnas, false, null);

                placingShip = true;
                shipsToPlaceCount = data.ships_to_place;
                placementControlsDiv.style.display = 'flex';
                placementMessageDiv.textContent = `Barcos pendientes: ${shipsToPlaceCount}. Haz click en tu tablero para colocar un barco de tamaño ${currentShipSize}.`;
                computerBoardDiv.style.pointerEvents = 'none';

                // Mostrar los controles de colocación por input
                placementControlsDiv.style.display = 'flex';

            } else {
                 showMessage(data.message || 'Error al iniciar el juego.', 'setup-message');
            }
        } catch (error) {
            console.error('Error en inicio de juego:', error);
            showMessage('Error al intentar iniciar el juego.', 'setup-message');
        }
    });

    function addPlacementListeners(){
        playerBoardDiv.querySelectorAll('.cell').forEach(cell => {
            cell.removeEventListener('click', handlePlacementClick);
            cell.addEventListener('click', handlePlacementClick);
        });
         confirmPlacementBtn.removeEventListener('click', confirmPlacement);
         confirmPlacementBtn.addEventListener('click', confirmPlacement);
         orientationSelect.removeEventListener('change', handleOrientationChange);
         orientationSelect.addEventListener('change', handleOrientationChange);
    }

    function handleOrientationChange() {
         if(selectedPlacement) {
              handlePlacementClick(null, selectedPlacement.row, selectedPlacement.col);
          } else {
               clearPlacementPreview();
          }
    }

    function handlePlacementClick(event, clickedRow = null, clickedCol = null) {
         console.log("handlePlacementClick called");
         if (!placingShip || !currentUser) {
              console.log("Placement click ignored: placingShip or currentUser check failed");
              return;
         }

         const row = clickedRow !== null ? clickedRow : parseInt(event.target.dataset.row);
         const col = clickedCol !== null ? clickedCol : parseInt(event.target.dataset.col);
         const orientation = orientationSelect.value;
         const filas = parseInt(playerBoardDiv.style.getPropertyValue('--row-count'));
         const columnas = parseInt(playerBoardDiv.style.getPropertyValue('--column-count'));

         clearPlacementPreview();

         if (isNaN(row) || isNaN(col) || row < 0 || row >= filas || col < 0 || col >= columnas) {
              showGameMessage("Posición inicial inválida.");
              selectedPlacement = null;
              confirmPlacementBtn.style.display = 'none';
              return;
         }

         let canPlace = true;
         const previewCells = [];

         for(let i = 0; i < currentShipSize; i++){
             let targetRow = row;
             let targetCol = col;
             if (orientation === 'H'){
                 targetCol += i;
             } else {
                 targetRow += i;
             }

             if (targetRow >= filas || targetCol >= columnas || targetRow < 0 || targetCol < 0) {
                 canPlace = false;
                 break;
             }

             const cellElement = playerBoardDiv.querySelector(`[data-row='${targetRow}'][data-col='${targetCol}']`);
             if (cellElement && cellElement.classList.contains('ship')){
                  canPlace = false;
                  break;
             }
             previewCells.push(cellElement);
         }

         if (canPlace) {
             previewCells.forEach(cell => cell.classList.add('preview'));
             selectedPlacement = {row, col, orientation};
             confirmPlacementBtn.style.display = 'inline-block';
             showGameMessage("Posición válida. Confirma la colocación.");
         } else {
             selectedPlacement = null;
             confirmPlacementBtn.style.display = 'none';
              showGameMessage("El barco no cabe o se superpone aquí.");
         }
    }

    function clearPlacementPreview(){
        playerBoardDiv.querySelectorAll('.cell.preview').forEach(cell => {
            cell.classList.remove('preview');
        });
    }

    async function confirmPlacement(){
         if (!selectedPlacement || !currentUser) return;

         const {row, col, orientation} = selectedPlacement;

         try {
            const response = await fetch('/place_ship', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ fila: row, columna: col, orientacion, username: currentUser })
            });

            const data = await response.json();

            if (response.ok) {
                 const filas = parseInt(playerBoardDiv.style.getPropertyValue('--row-count'));
                 const columnas = parseInt(playerBoardDiv.style.getPropertyValue('--column-count'));
                 buildBoard(playerBoardDiv, filas, columnas, true, data.player_board);

                 shipsToPlaceCount = data.ships_remaining;
                 placementMessageDiv.textContent = `Barcos pendientes: ${shipsToPlaceCount}. Haz click en tu tablero para colocar un barco de tamaño ${currentShipSize}.`;
                 showGameMessage(data.message);

                 clearPlacementPreview();
                 selectedPlacement = null;
                 confirmPlacementBtn.style.display = 'none';

                 if (shipsToPlaceCount === 0) {
                     placingShip = false;
                     placementControlsDiv.style.display = 'none';
                     showGameMessage("¡Todos tus barcos están colocados! Ahora es tu turno de disparar en el tablero enemigo.");
                      computerBoardDiv.style.pointerEvents = 'auto';
                 }

            } else {
                 showGameMessage(data.message || 'Error al colocar el barco.');
                 clearPlacementPreview();
                 selectedPlacement = null;
                 confirmPlacementBtn.style.display = 'none';
            }
        } catch (error) {
            console.error('Error al colocar barco:', error);
            showGameMessage('Error al intentar colocar el barco.');
            clearPlacementPreview();
            selectedPlacement = null;
            confirmPlacementBtn.style.display = 'none';
        }
    }

    function buildBoard(boardElement, filas, columnas, isPlayerBoard, boardState) {
        const numFilas = parseInt(filas);
        const numColumnas = parseInt(columnas);

        if (isNaN(numFilas) || isNaN(numColumnas) || numFilas <= 0 || numColumnas <= 0) {
            console.error("Dimensiones del tablero inválidas:", filas, columnas);
            return;
        }

        boardElement.style.setProperty('--row-count', numFilas);
        boardElement.style.setProperty('--column-count', numColumnas);
        boardElement.innerHTML = '';

        for (let i = 0; i < numFilas; i++) {
            for (let j = 0; j < numColumnas; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = i;
                cell.dataset.col = j;
                
                if (boardState && boardState[i] && boardState[i][j]) {
                    const cellState = boardState[i][j];
                    if (cellState === 'O' && isPlayerBoard) {
                        cell.classList.add('ship');
                    }
                    if (cellState === 'X') {
                        cell.classList.add('hit');
                        cell.textContent = '✕';
                    }
                    if (cellState === '/') {
                        cell.classList.add('miss');
                        cell.textContent = '○';
                    }
                }

                boardElement.appendChild(cell);
            }
        }
        
        // Controlar pointer events basado en si es el tablero de la computadora o el del jugador en fase de colocación
        if (!isPlayerBoard) {
            boardElement.style.pointerEvents = 'none'; // Tablero enemigo no clickeable inicialmente
        } else if (isPlayerBoard && placingShip) {
            boardElement.style.pointerEvents = 'auto';
        } else if (isPlayerBoard && !placingShip) {
            boardElement.style.pointerEvents = 'none';
        }
    }

    // Nueva función para colocar barco desde inputs (será asociada al botón)
    async function placeShipFromInputs() {
        if (!placingShip || !currentUser) return; // Solo si estamos en fase de colocación

        // Obtener valores de los nuevos inputs (aún no creados en HTML)
        const filaInputElem = document.getElementById('placement-row');
        const colInputElem = document.getElementById('placement-col');

        const fila = parseInt(filaInputElem.value); // Convertir a entero
        const columna = parseInt(colInputElem.value); // Convertir a entero
        const orientacion = orientationSelect.value;

        // Validar inputs básicos
        if (isNaN(fila) || isNaN(columna)) {
             showGameMessage("Por favor, ingresa números válidos para fila y columna.");
             return;
        }

        // Las validaciones más complejas (límites, superposición) se harán en el backend

        // Llamar a la ruta del backend para colocar el barco
        try {
            const response = await fetch('/place_ship', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ fila, columna, orientacion, username: currentUser })
            });

            const data = await response.json();

            if (response.ok) {
                 // Actualizar el tablero visualmente
                 const filas = parseInt(playerBoardDiv.style.getPropertyValue('--row-count'));
                 const columnas = parseInt(playerBoardDiv.style.getPropertyValue('--column-count'));
                 buildBoard(playerBoardDiv, filas, columnas, true, data.player_board); // Reconstruir el tablero del jugador

                 shipsToPlaceCount = data.ships_remaining;
                 placementMessageDiv.textContent = `Barcos pendientes: ${shipsToPlaceCount}. Ingresa las coordenadas y orientación para colocar un barco de tamaño ${currentShipSize}.`; // Actualizar mensaje
                 showGameMessage(data.message); // Mostrar mensaje de éxito del backend

                 // Limpiar inputs después de colocar
                 filaInputElem.value = '';
                 colInputElem.value = '';

                 // Si ya no hay barcos pendientes, pasar a la fase de disparo
                 if (shipsToPlaceCount === 0) {
                     placingShip = false;
                     placementControlsDiv.style.display = 'none'; // Ocultar controles de colocación
                     shootingControlsDiv.style.display = 'flex'; // Mostrar controles de disparo
                     showGameMessage("¡Todos tus barcos están colocados! Ahora es tu turno de disparar en el tablero enemigo.");

                     // Hacer el tablero enemigo clickeable/interactivo para disparar (aunque usemos inputs, la visualización de aciertos/fallos es en este tablero)
                     computerBoardDiv.style.pointerEvents = 'auto'; // Permitir interacción (para futuras mejoras o visualización), aunque el disparo sea por input

                 }

            } else {
                 // Mostrar mensaje de error del backend
                 showGameMessage(data.message || 'Error al colocar el barco.');
            }
        } catch (error) {
            console.error('Error al colocar barco:', error);
            showGameMessage('Error al intentar colocar el barco.');
        }
    }

    // Nueva función para manejar el disparo desde inputs
    async function handleShootFromInputs() {
        if (placingShip || !currentUser) return;

        const filaStr = shootRowInput.value;
        const columnaStr = shootColInput.value;

        const fila = parseInt(filaStr) - 1;
        const columna = parseInt(columnaStr) - 1;

        if (isNaN(fila) || isNaN(columna) || fila < 0 || columna < 0) {
            showGameMessage("Por favor, ingresa números válidos y positivos para fila y columna.");
            return;
        }

        const filasTablero = parseInt(computerBoardDiv.style.getPropertyValue('--row-count'));
        const columnasTablero = parseInt(computerBoardDiv.style.getPropertyValue('--column-count'));

        if (fila >= filasTablero || columna >= columnasTablero) {
             showGameMessage(`Las coordenadas deben estar dentro del rango del tablero (${1}-${filasTablero}, ${1}-${columnasTablero}).`);
             return;
        }

        shootBtn.disabled = true;

        try {
            const response = await fetch('/shoot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ fila, columna, username: currentUser })
            });

            const data = await response.json();
            shootBtn.disabled = false;

            if (response.ok) {
                const filas = parseInt(playerBoardDiv.style.getPropertyValue('--row-count'));
                const columnas = parseInt(playerBoardDiv.style.getPropertyValue('--column-count'));

                // Actualizar ambos tableros con el estado después del turno del jugador y la computadora
                buildBoard(playerBoardDiv, filas, columnas, true, data.player_board);
                buildBoard(computerBoardDiv, filas, columnas, false, data.computer_board);

                shootRowInput.value = '';
                shootColInput.value = '';

                if (data.game_over) {
                     if (data.result === 'jugador') {
                         showGameMessage('¡Felicidades! ¡Has ganado!');
                     } else {
                         showGameMessage('¡Derrota! La computadora ha ganado.');
                     }
                     shootingControlsDiv.style.display = 'none';
                     return;
                }

                // Construir mensaje del turno del jugador
                let playerShotMessage = `Tu disparo en (${fila + 1}, ${columna + 1}): `;
                if (data.result === 'agua') playerShotMessage += '¡Agua!';
                else if (data.result === 'impacto') playerShotMessage += '¡Impacto!';
                else if (data.result === 'hundido') playerShotMessage += '¡Barco Hundido!';
                else if (data.result === 'ya_disparado') {
                    showGameMessage(data.message || 'Ya habías disparado aquí.');
                    return;
                }

                // Construir mensaje del turno de la computadora
                let compShotMessage = '';
                if (data.computer_shot) {
                    compShotMessage = `\nLa computadora disparó en (${data.computer_shot.fila + 1}, ${data.computer_shot.columna + 1}): `;
                    if (data.computer_shot.resultado === 'agua') compShotMessage += '¡Agua!';
                    else if (data.computer_shot.resultado === 'impacto') compShotMessage += '¡Impacto en tu barco!';
                    else if (data.computer_shot.resultado === 'hundido') compShotMessage += '¡Tu barco ha sido hundido!';
                }

                // Mostrar mensaje combinado
                showGameMessage(playerShotMessage + compShotMessage);

            } else {
                showGameMessage(data.message || 'Error al realizar el disparo.');
            }
        } catch (error) {
            console.error('Error en disparo:', error);
            showGameMessage('Error al intentar realizar el disparo.');
            shootBtn.disabled = false;
        }
    }

    showSection(loginSection);

    // Añadir event listener para el botón de colocar barco
    if (placeShipBtn) {
        placeShipBtn.addEventListener('click', placeShipFromInputs);
    }

    // Añadir event listener para el botón de disparo (nuevo)
    if (shootBtn) {
        shootBtn.addEventListener('click', handleShootFromInputs);
    }
}); 