# Firmware del Control G7 (v1.2)

**Grupo 7 (G7) · IND474 Desarrollo de Productos Físicos · PCB D4.4 · 16/11/2026**

Firmware definitivo del control. Reemplaza al borrador `Control_proyecto_2.ino` que iba en `01_PCB_D4.4_entregada\4_Anexos\firmware`, que nunca se probó en la placa y arrancaba con el USB desactivado hasta recibir una "h" por el Monitor Serie.

Archivo: `G7_Gamepad\G7_Gamepad.ino`

## Qué hace

- Windows lo reconoce como **"Control G7"**: un dispositivo USB compuesto con gamepad HID, teclado HID y puerto serie.
- **Modo GAMEPAD** (por defecto) y **modo TECLADO** (respaldo para juegos que no aceptan gamepad).
- La pantalla TFT muestra el modo, la posición del stick y los botones presionados en vivo.
- Usa los dos núcleos del RP2350:
  - **núcleo 0:** lee las entradas y las envía por USB a 1 kHz;
  - **núcleo 1:** dibuja la pantalla, así el dibujo nunca retrasa el USB.

## Asignación de controles

| Control físico | GPIO | Modo GAMEPAD | Modo TECLADO |
|---|---|---|---|
| Stick X / Y (KY-023) | GP26 / GP27 | Ejes X / Y (16 bit) | Flechas (al inclinar más del 50 %) |
| Cruceta UP/DOWN/LEFT/RIGHT | GP2 / GP3 / GP4 / GP5 | Hat (POV), con diagonales | Flechas |
| A | GP6 | Botón 1 | Z |
| B | GP7 | Botón 2 | X |
| MENU | GP8 | Botón 8 (Start) | Enter |
| Clic del stick (JOY_SW) | GP9 | Botón 9 (L3) | Espacio |

La numeración de botones coincide con la de un control de Xbox en modo genérico (A = 1, B = 2, Start = 8, L3 = 9). Los juegos y Steam la interpretan de forma natural.

## Atajos

| Atajo | Mantener | Acción |
|---|---|---|
| **MENU + B** | 1,5 s | Cambia entre GAMEPAD y TECLADO. El modo se guarda en memoria y se mantiene al desenchufar. |
| **MENU + A** | 1,5 s, con el stick suelto | Recalibra el centro del stick. La pantalla muestra "CENTRO OK". (Provisorio: se pensó como MENU + clic del stick; se cambió mientras el cable del joystick tenga falsos contactos.) |

El centro del stick también se calibra solo cada vez que se enchufa el USB, por lo que hay que enchufar con el stick suelto.

## Parámetros principales (inicio del archivo)

| Parámetro | Valor | Por qué |
|---|---|---|
| `BLOQUEO_MS` (antirrebote) | 20 ms; MENU 40 ms; JOY 30 ms | MENU rebotó hasta 31,7 ms al soltarlo (prueba 4). El cambio se acepta al instante y se ignoran los rebotes siguientes, así que no agrega retraso. |
| `ZONA_MUERTA` | 160 cuentas (~4 %) | El ruido medido en reposo es ±30 cuentas. |
| `INTERCAMBIAR_XY`, `INVERTIR_X`, `INVERTIR_Y` | false | Calibrado el 16/11: arriba = Y negativo, derecha = X positivo, con el KY-023 orientado con su conector hacia J3. |
| `UMBRAL_TECLA` | 16000 (~50 %) | Inclinación del stick que equivale a apretar una flecha en modo teclado. |
| Pantalla | `setRotation(1)` | Texto horizontal con la placa en su posición de uso. |

## Cómo cargarlo

**Requisitos (ya instalados en el PC de Vicente):**

- Arduino IDE 2.3.11.
- Núcleo **Raspberry Pi Pico/RP2040/RP2350** de Earle Philhower, versión **6.3.2**. URL del gestor de placas: `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json`
- Librerías **Adafruit ST7735 and ST7789 Library** y **Adafruit GFX Library**. Joystick, Keyboard y EEPROM vienen con el núcleo.
- Nombre USB "Control G7": archivo `boards.local.txt` en `%LOCALAPPDATA%\Arduino15\packages\rp2040\hardware\rp2040\6.3.2\` con:
  ```
  waveshare_rp2350_plus.build.usb_manufacturer="Grupo 7 IND474"
  waveshare_rp2350_plus.build.usb_product="Control G7"
  ```
  Sin ese archivo el firmware funciona igual, pero el control aparece como "RP2350 Plus".

**Pasos:**

1. Abrir `G7_Gamepad\G7_Gamepad.ino`.
2. Placa: **Waveshare RP2350 Plus**.
3. Puerto: **COM7** con este firmware cargado. Con sketches simples la placa aparece como COM6, porque el control usa un dispositivo compuesto y Windows le asigna otro número. Si no aparece ningún puerto, mantener **BOOT** al enchufar y elegir "UF2 Board".
4. Presionar Upload.

Por línea de comandos, con el arduino-cli que trae el IDE:
```
arduino-cli compile --fqbn rp2040:rp2040:waveshare_rp2350_plus -u -p COM7 G7_Gamepad
```

Puede aparecer un aviso de PowerShell sobre `Microsoft.PowerShell_profile.ps1`. No afecta la carga.

## Diagnóstico

- **Monitor Serie a 115200:** cada 250 ms imprime el modo, los valores crudos y procesados del stick y el estado de los 8 botones. Ejemplo: `GAMEPAD rawX=2070 rawY=2075 X=0 Y=0 btn=00000000`.
- **Pantalla:** abajo muestra los valores crudos X/Y y el centro calibrado.
- **Windows:** Win + R → `joy.cpl` → Propiedades. También sirve gamepad-tester.com en Chrome: el hat aparece como AXIS 9 (arriba −1; derecha −0,43; abajo 0,14; izquierda 0,71; sin presionar, un número fuera de rango, que es lo normal).

## Resultados de las pruebas (16/11/2026)

| Prueba | Resultado |
|---|---|
| Reconocimiento USB | ✅ "Dispositivo de juego compatible con HID" + teclado HID + COM; nombre "Control G7" |
| Botones en gamepad-tester | ✅ A = B0, B = B1, MENU = B7; cruceta = hat con las 4 direcciones |
| Stick en gamepad-tester | ✅ −1 a 1, centro 0 (con el cable firme) |
| Modo teclado | ✅ cambio con MENU + B; B escribe "x"; juego del dinosaurio de Chrome |
| Juego real (SuperTux 0.7.0, no Steam) | ✅ botones, cruceta y stick, tras asignarlos una vez en Opciones → Configurar joystick |
| Antirrebote MENU | ✅ filtra el rebote de hasta 31,7 ms |

## Limitaciones y pendientes

- **Gamepad genérico (DirectInput/HID), no control de Xbox.** Los juegos no lo traen en su lista de controles conocidos, así que la primera vez hay que asignar los botones en el juego (pasó en SuperTux). En Steam, "Compatibilidad con mandos genéricos" lo convierte en un control de Xbox. Para juegos que solo aceptan Xbox fuera de Steam: modo TECLADO. Que se presente como control de Xbox (XInput) requiere otro firmware, fuera de Arduino. Queda como mejora futura.
- **Cable del joystick:** el cable XH armado a mano tiene falsos contactos (VRy, GND y 3V3). Síntomas: los dos ejes saltan juntos, o el centro de Y se corre (se vio Y = 1558 en reposo). Arreglo previsto para el viernes 20/11. Después:
  1. repetir la lectura del stick;
  2. decidir si la recalibración vuelve a MENU + clic del stick.
- **Con el joystick desconectado,** GP26/GP27 quedan al aire y leen valores al azar (por ejemplo 3120/2355). Es normal. Conectar el joystick siempre con el USB desenchufado, o recalibrar con MENU + A.

## Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 16/11/2026 | Gamepad + teclado, antirrebote, zona muerta, calibración al enchufar, pantalla en el núcleo 1 |
| 1.1 | 16/11/2026 | Recalibración con MENU + JOY; textos de ayuda en pantalla; nombre USB "Control G7" |
| 1.2 | 16/11/2026 | Recalibración pasa a MENU + A; en modo teclado MENU + A no envía Enter |
