# Decisiones de diseño

Registro de las decisiones del Control G7 y de lo que cambió desde la propuesta (presentación de la semana 8). Cada decisión indica por qué se tomó y cómo se va a verificar.

## Plataforma y funcionamiento

| # | Decisión | Antes | Por qué | Verificación |
|---|---|---|---|---|
| D1 | **Gamepad HID estándar + modo teclado** | Teclado para MakeCode Arcade | El profesor pidió que el control sirva para juegos de PC en general. El gamepad HID no necesita drivers; el modo teclado cubre juegos que no aceptan gamepad. | ✅ gamepad-tester, SuperTux 0.7.0, dinosaurio de Chrome |
| D2 | **Pantalla ST7789 1,3"** en vez de LED RGB | LED RGB (amarillo/verde) | Con dos modos y recalibración, un LED no alcanzaba para mostrar el estado. | ✅ muestra modo, stick, botones y "CENTRO OK" |
| D3 | Cambio de modo con **MENU + B 1,5 s**, guardado en EEPROM | — | Evita cambios accidentales y no requiere un botón extra. | ⏳ medir en la prueba con usuarios si lo descubren |
| D4 | Recalibración con **MENU + A 1,5 s** | MENU + clic del stick | Provisorio mientras el cable del joystick tenga falsos contactos. | ✅ funciona en la placa |
| D5 | Antirrebote por botón: 20 ms; MENU 40 ms; JOY 30 ms | — | MENU rebotó hasta 31,7 ms al soltarlo (prueba 4). | ✅ `firmware/pruebas/prueba_4_rebote` |
| D6 | Pantalla en el núcleo 1, USB en el núcleo 0 a 1 kHz | — | El dibujo nunca retrasa el envío por USB. | ✅ |

**Limitación conocida:** al ser HID genérico, algunos juegos piden mapear los botones la primera vez. XInput queda como mejora futura.

## Electrónica (PCB D4.4)

| # | Decisión | Por qué |
|---|---|---|
| E1 | Montaje 100 % THT, soldado a mano | Requisito del curso (revisión 2 del profesor). |
| E2 | RP2350-Plus **soldado directo** por la cara trasera, sin zócalos | Más delgado y sin contactos sueltos. Primero se soldó por la cara equivocada y se corrigió (ver `hardware/CAMBIOS_DESDE_D4.4.md`). |
| E3 | Joystick al centro, bajo la pantalla | Lo fijó la PCB rectangular D4.4. Probablemente queda fuera del radio cómodo del pulgar (44,5 mm); se deja como mejora para una v2. |

## Carcasa v6

| # | Decisión | Propuesta (sem 8) | Por qué | Verificación |
|---|---|---|---|---|
| C1 | **Pared sólida de 2,4 mm** (6 perímetros, sin relleno) | 3,2–3,6 mm | El primer control se deformó en la A1. Hipótesis: el problema eran las caras planas grandes, no el espesor; v6 es redondeada y sin caras planas grandes. | ⏳ probeta |
| C2 | **Partición tipo concha:** PCB atornillada a la tapa con 4 × M2×6; base a presión con 6 clips y un faldón interior | M3 con tuerca cautiva | Los agujeros de la PCB son M2; en el primer control los insertos y tornillos no ajustaron. | ⏳ abrir y cerrar 3 veces la carcasa impresa |
| C3 | **184 × 137 × 52 mm** con grips tipo DualSense que nacen de la cara superior | 165 × 110 × 43 mm | Agarre de palma completa; un solo movimiento entre grips y cara de botones. Cabe en la cama de 256 mm de la Bambu A1. | ⏳ prueba con 5 usuarios (manos chicas y grandes) |
| C4 | Perilla del joystick con **cúpula** que tapa el mecanismo | Perilla estándar del KY-023 | La original quedaba 22 mm sobre la cara y dejaba el mecanismo a la vista. Sin choques hasta 30°. | ✅ verificado en CAD |
| C5 | Capuchones impresos **huecos con nervios**; MENU macizo | — | Menos material sin perder rigidez; MENU es chico y se imprime mejor macizo. | ⏳ impresión |
| C6 | Agujeros de aguja para **BOOT y RESET** | — | Reprogramar sin abrir la carcasa. | ⏳ confirmar cuál es cuál en el módulo real |
| C8 | **Partición que sigue la geometría del grip** (24/11, feedback del profesor) | Plano z = 0 en toda la carcasa | Con el plano, cada grip quedaba como un tubo profundo que necesitaba soporte interior. Ahora la unión baja por la línea media de cada grip hasta la punta; cada mitad es una cáscara abierta. En el cuerpo sigue en z = 0. | ✅ CAD: tapa y base de 1 cuerpo cada una, sin interferencia |
| C9 | **2 pasadores de alineación por grip** (Ø3 × 4 mm en la tapa, agujero Ø3,3 en la base, torres Ø7) | — | En los grips la unión ya no es plana y el faldón no calzaba; sin guía podía quedar un escalón donde va la palma. | ⏳ impresión |
| C7 | USB-C arriba al centro, ventana 13,5 × 7,5 con bisel | — | Enchufe medido de 12,1 × 6,4 mm; el cable sale hacia el PC. | ⏳ probeta |

### Holguras (a confirmar con la probeta)

| Elemento | Pieza real | Agujero / encaje |
|---|---|---|
| Capuchón | Ø13 | Ø13,6 (0,3 por lado) |
| Vástago del pulsador | 3,8 | 3,95 |
| Enchufe USB-C | 12,1 × 6,4 | 13,5 × 7,5 |

### CMF

- **Material:** PLA o PETG (pendiente decidir para los clips: PETG flexa sin romperse, PLA es más preciso).
- **Color:** cuerpo gris neutro; acento solo donde se actúa (cruceta de colores, A/B negros).
- **Acabado:** cara de botones contra la cama para que quede lisa.
- ⏳ Muestras de 30 × 30 mm.
