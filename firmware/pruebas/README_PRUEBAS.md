# Pruebas de hardware del Control G7 (PCB D4.4)

**Grupo 7 (G7) · IND474 · 16/11/2026**

El profesor indicó probar por partes: primero botones, después joystick y al final pantalla. Cada sketch de esta carpeta prueba una sola parte. Todas se cargaron en la placa con la placa **Waveshare RP2350 Plus** (Arduino-Pico 6.3.2), y las lecturas se tomaron por el puerto serie a 115200.

## Antes de las pruebas

- **Módulo RP2350-Plus-M:** primero se soldó por la cara frontal. Así quedaba espejado: cada agujero recibía el pin opuesto, por ejemplo DOWN caía en la salida de 3,3 V. Se desoldó y se volvió a soldar por la **cara trasera**, según la serigrafía "PIN 1 / PIN 40 / USB-C" de atrás.
- **Continuidad:** se revisó que no hubiera continuidad entre 3V3 y GND. **BLK (J4.7)** no tiene continuidad, y es intencional: en el diseño queda sin conectar porque la pantalla enciende su luz de fondo por defecto.
- **Módulo solo:** se cargó un parpadeo del LED (GPIO25) y funcionó. Con eso se confirmó que el módulo ejecuta código y se comunica por USB.

## Resultados

| # | Sketch | Qué prueba | Resultado |
|---|---|---|---|
| 1 | `prueba_1_botones` | UP, DOWN, LEFT, RIGHT, A, B y MENU (GP2–GP8) | ✅ Los 7 responden con su nombre correcto, sin pulsaciones fantasma |
| 2 | `prueba_2_joystick` | KY-023: X (GP26), Y (GP27), SW (GP9) | ✅ X e Y en reposo ~2080, recorrido 0–4095, ruido ±30. SW detectado. Ver nota del cable |
| 3 | `prueba_3_pantalla` | TFT ST7789 1,3" 240×240 (SPI modo 3, sin CS) | ✅ Inicializa, muestra rojo, verde, azul y blanco, texto, y botones y joystick en vivo. `setRotation(1)` deja el texto horizontal. El panel tiene algunos píxeles muertos (defecto de la pantalla, no del circuito) |
| 4 | `prueba_4_rebote` | Rebote de MENU (GP8) y A (GP6) | 9 de 11 pulsaciones de MENU limpias; una soltada rebotó 31,7 ms y otra 0,3 ms. Se resuelve por firmware (bloqueo de 40 ms) |

## Nota: cable del joystick

El cable XH (J3) ↔ Dupont (KY-023) está armado a mano y tiene falsos contactos:

- **Primera lectura** (`lecturas\joystick_1_falla_VRy.txt`): Y nunca se movió sola y solo seguía a X. Es el síntoma de VRy desconectado: el pin queda al aire y toma algo de los pines vecinos.
- **Segunda lectura** (`lecturas\joystick_2_ejes_OK.txt`): los dos ejes ya se mueven por separado.
- **Lecturas posteriores:** los dos ejes saltan juntos al máximo o a cero al mover el cable. Eso indica que se pierde GND o 3V3. También se vio el centro de Y corrido (1558 en reposo).

Arreglo previsto: rehacer o fijar el cable (viernes 20/11). Orden en J3: GND, 3V3, VRx, VRy, SW. Colores en el KY: SW amarillo, VRy naranja, VRx rojo, +5V café, GND verde agua.

## Pinout verificado

| Función | GPIO | Pin del módulo |
|---|---|---|
| UP, DOWN, LEFT, RIGHT | GP2–GP5 | 4–7 |
| A, B, MENU, JOY_SW | GP6–GP9 | 9–12 |
| Joystick X / Y | GP26 / GP27 | 31 / 32 |
| TFT SCK, MOSI, DC, RST | GP18, GP19, GP20, GP21 | 24–27 |
| 3V3 | — | 36 |
| LED integrado | GP25 | — |
