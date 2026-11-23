# Control proyecto 2 — Mando arcade USB · rev D4.4

**Grupo 7 (G7) · IND474 Desarrollo de Productos Físicos** · V. Kohler, G. Hidalgo, F. Guaita, E. Rojas · 27/10/2026

Placa portadora de 125 × 70 × 1,6 mm a dos caras, **con montaje 100 % THT** (todo se suelda a mano; el fabricante solo hace la PCB). Lleva un D-pad de cuatro pulsadores de 12 mm, los botones A/B de 12 mm, un botón MENU de 6 mm, una pantalla TFT ST7789 de 1,3" y un joystick KY-023. El microcontrolador es un Waveshare RP2350-Plus-M que va en zócalos por la cara posterior, con el USB-C hacia el borde superior. El mando funciona como teclado HID por USB y no tiene batería.

Las respuestas punto por punto a las revisiones docentes están en **`RESPUESTA_REVISION_2_D4.4.pdf`** (revisión 2, 26/10) y en **`RESPUESTA_FEEDBACK_D4.3.pdf`** (revisión 1, 22/10).

## Estado

| Verificación | Resultado (KiCad 9.0.3) |
|---|---|
| ERC | 0 errores, 0 advertencias |
| DRC (`--schematic-parity --severity-all`) | 0 violaciones, 0 pads sin conectar, 0 problemas de paridad, 0 errores de huella |
| Gerbers releídos con Gerbonara | contorno 125,0 × 70,0 mm · 112 PTH (28 vías) · 8 NPTH (4 × Ø3,2 y 4 × Ø2,2) |
| Componentes SMD | 0 (todas las huellas son THT o NPTH) |
| Esquinas de pista a 90° | 0 · 176 esquinas a 45° · 0 agudas (script `corners.py`) |
| Pinout de J1–J4 contra la tabla GPIO | 0 diferencias (script de comprobación) |

Esto **no** reemplaza las pruebas físicas descritas más abajo, en "Antes de fabricar" y "Prueba eléctrica".

### Historial de revisiones

| Rev. | Fecha | Cambio |
|---|---|---|
| D3.1 | 20/10 | Revisión entregada al profesor |
| D4.0 | 23/10 | Corrección docente: C1/C2 montados, fijaciones, serigrafía, símbolos de potencia, cosido GND, BOM/README |
| D4.1 | 26/10 | Los pulsadores de 12 mm del kit son **SMD** (patas dobladas, patrón 14 × 5) → huella PTS125Sx73SMTR |
| D4.2 | 26/10 | D-pad compacto (paso 12,75). El TFT se enchufa **directo** en J4. TFT corrido +1 mm para que el tornillo M2 trasero no pise J1 |
| D4.3 | 26/10 | J3 sale de la zona del KY-023: los pines acodados del KY y su conector chocaban con J3. El plano mecánico queda en 1:1 |
| **D4.4** | **27/10** | **Revisión 2 del profesor:** montaje 100 % THT (pulsadores de 12 mm THT, C1 disco, C2 electrolítico; se elimina JP1) y todas las pistas a 45°. D-pad ajustado a los courtyards THT. J4 se mantiene, con la evidencia de la pieza real |

## Diagrama de bloques

```
USB-C (PC) ──► RP2350-Plus-M (USB, regulador 3V3)
                 ├─ GP2..GP9  ◄── 7 pulsadores + clic del stick (INPUT_PULLUP, a GND)
                 ├─ GP26/27 (ADC) ◄── KY-023 VRx/VRy  [J3 JST XH, 3V3]
                 ├─ GP18/19/20/21 (SPI0) ──► TFT ST7789 SCK/MOSI/DC/RST [J4 zócalo, 3V3]
                 └─ 3V3(OUT) ──► TFT + KY-023 (C1 100 nF disco + C2 10 µF electrolítico junto a J4)
```

## Tabla GPIO

| Función | GPIO | Pin físico | Contacto |
|---|---|---|---|
| UP | GP2 | 4 | J1.4 |
| DOWN | GP3 | 5 | J1.5 |
| LEFT | GP4 | 6 | J1.6 |
| RIGHT | GP5 | 7 | J1.7 |
| A | GP6 | 9 | J1.9 |
| B | GP7 | 10 | J1.10 |
| MENU | GP8 | 11 | J1.11 |
| JOY_SW (clic) | GP9 | 12 | J1.12 |
| ADC_X (VRx) | GP26 / ADC0 | 31 | J2.10 |
| ADC_Y (VRy) | GP27 / ADC1 | 32 | J2.9 |
| TFT_SCK (SCL) | GP18 | 24 | J2.17 |
| TFT_MOSI (SDA) | GP19 | 25 | J2.16 |
| TFT_DC | GP20 | 26 | J2.15 |
| TFT_RST (RES) | GP21 | 27 | J2.14 |
| 3V3(OUT) | — | 36 | J2.5 |
| GND | — | 3, 8, 13, 18, 23, 28, 33 (AGND), 38 | J1.3/8/13/18 · J2.3/8/13/18 |

En J1, el contacto n corresponde al pin físico n. En J2, el contacto 1 es el pin 40 y el contacto 20 es el pin 21, porque el módulo va espejado en la cara posterior. El pinout es el de la Pico 2: Waveshare declara el RP2350-Plus compatible con ella, y la "-M" trae las tiras soldadas de fábrica. La tabla completa está en `1_Diseno_KiCad/conexiones-hileras.csv`.

## Conectores (con la serigrafía real de los módulos)

| Conector | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| **J3** JST XH 5 → KY-023 | GND | 3V3 (al "+5V" del KY) | VRx | VRy | SW | | |
| **J4** zócalo 1×7 ← TFT | GND | 3V3 (VCC) | SCL = SCK | SDA = MOSI | RES | DC | BLK |

![KY-023: serigrafía de pines](fotos/KY-023_serigrafia_pines.jpg)
![TFT ZJY-IPS130: serigrafía de pines](fotos/TFT_serigrafia_pines.jpg)
![TFT: pines a ~1 mm del eje de los agujeros](fotos/TFT_pines_vs_agujeros_anotado.png)

- **KY-023.** Vistos de arriba hacia abajo, los pines son SW, VRy, VRx, +5V y GND, en el orden inverso al de J3. El cable JST queda directo: GND con GND, …, SW con SW. Se alimenta a **3,3 V**: las entradas ADC no toleran 5 V.
- **TFT.** Es el modelo de **7 pines sin CS**. El de 8 pines no es compatible. SCL y SDA son señales SPI, no I²C, y se usa SPI en modo 3. El TFT se enchufa en J4 con la pantalla hacia el frente y el cabezal a la derecha, de modo que el pin 1 (marca "1", GND) queda arriba. Un TFT girado invierte VCC y GND y se destruye.
- **BLK (J4.7) queda sin conectar**, porque según la ficha del módulo el backlight enciende por defecto. JP1 se eliminó en D4.4 (era SMD).

## Mecánica (ver `planos/D4.4_plano_mecanico_1a1.pdf`)

- **Portadora.** Va fijada con H1–H4 (M3, a 4 mm de las esquinas). Por detrás, el módulo y el USB-C llegan a −16,8 mm, así que se usan separadores M3 de **18 mm** y una ventana de 12 × 7 mm en el canto superior, centrada en x = 53.
- **TFT.** Va enchufado en J4 (zócalo de 8,5 mm, pines en x 100,94; y 10,38–25,62). Los pines del módulo están a 1,5 mm del borde y los agujeros a 2,5 mm (plano del vendedor, foto anotada y modelo 3D); por eso J4 queda 1,0 mm más afuera que H6/H8 y atornillado en H5–H8 (M2): (65,72; 6,61), (99,94; 6,61), (65,72; 29,39) y (99,94; 29,39). Estos agujeros siguen el patrón 34,22 × 22,78 del plano ZJY. Usa separadores redondos de nailon de Ø ≤ 3,5 y **11 mm** de alto. La PCB del TFT queda a 11,0 mm y el vidrio a 13,7 mm.
- **KY-023.** Va **atornillado a la tapa superior** desde abajo, con 4 tornillos M2,5 a torres de 7,5 mm. Sus agujeros son de Ø3,0 en patrón 26,5 × 20,5 y el stick queda en (60,5; 55), a 43,2 mm de la base del pulgar izquierdo. Su PCB queda a 9 mm sobre la portadora, el domo pasa por un hueco de Ø20 y el pomo Ø26 queda 1,2 mm sobre la tapa. El cable JST va a **J3, que está abajo a la derecha** (pines x 104–114, y 60), fuera de la zona del KY.
- **Tapa propuesta.** La cara exterior va a 19 mm. Los capuchones (12 mm) y el MENU (5,5 mm) llevan prolongadores impresos. El TFT queda ~5 mm bajo la ventana, en un rebaje.
- **Centros de los controles** (mm locales, desde la esquina superior izquierda, vista de frente): UP (22; 24), DOWN (22; 53), LEFT (9,5; 38,5), RIGHT (34,5; 38,5), A (114; 36), B (98; 44), MENU (112; 12). El D-pad THT queda a 14,5 mm en vertical y 12,5 mm en horizontal del centro: es el mínimo sin solapar los courtyards de 15,5 × 14,5 mm y sin acercar RIGHT a la fila de pines del módulo.
- **C2** (electrolítico Ø5 × 11) va de pie junto a J4, fuera de la huella del TFT, y alcanza ~11,5 mm de altura. El archivo KiCad tiene un offset de (50, 50).
- **Modelos 3D (GrabCAD)** en la carpeta `Modelos 3D (GrabCAD)` del grupo. Las medidas del TFT coinciden con el plano del vendedor (< 0,2 mm); el KY mide 34 × 26 con agujeros Ø3,0 en 26,5 × 20,5; el pulsador de 12 mm alcanza 12,0 de alto con capuchón.

## Orden de montaje

1. C1 (disco) y C2 (electrolítico: la pata larga, +, va al pad cuadrado marcado "+").
2. Pulsadores SW1–SW7 (THT, cara frontal).
3. J3 (JST XH) y J4 (zócalo 1×7), cara frontal. **Cable XH al KY-023:** marcar el hilo GND con marcador o termorretráctil en los dos extremos; esa marca va al GND del KY (primer pin de su serigrafía) y al pin 1 de J3, rotulado "GND" en la placa. En la tapa se rotula "GND" junto a la salida del cable. Conviene soldar J4 con el TFT enchufado y atornillado, para que quede alineado.
4. J1 y J2 (zócalos 1×20) por la **cara posterior**, con el módulo insertado.
5. Revisión sin energía (ver abajo). Después: módulo, TFT y cable del KY.

## Antes de fabricar (lo que el DRC no cubre)

0. **Comprar** lo que no está en el kit (ver BOM, "POR COMPRAR"): 6 pulsadores táctiles **THT** de 12 × 12 × 7,3 mm con 4 patas rectas (tipo Omron B3F-4055; el kit que tenemos es SMD y no sirve), 1 condensador cerámico de disco de 100 nF y 1 electrolítico de 10 µF / ≥ 10 V, Ø5 × 11 mm, paso 2 mm.
1. Imprimir `planos/D4.4_frente_1a1.pdf` y `planos/D4.4_dorso_1a1_espejo.pdf` al 100 %. Medir la barra de 50 mm y el contorno de 125 × 70.
2. Comprobar las piezas reales sobre la impresión:
   - pulsadores THT de 12 mm con las patas en los agujeros de 12,5 × 5;
   - MENU en el patrón 6,5 × 4,5;
   - RP2350 boca abajo sobre el dorso, con los 40 pines en los taladros y el USB-C arriba;
   - TFT con sus 7 pines en J4 y sus 4 agujeros en H5–H8.
3. Agujeros del KY y tipo de conector **confirmados el 26/10**: los agujeros del KY coinciden con el modelo (Ø3,0, patrón 26,5 × 20,5) y el conector es JST **XH** (paso 2,50).
4. Maqueta ergonómica 1:1 con 3 personas, una de ellas de mano pequeña. Comprobar que alcanzan UP y A sin mover la mano, que pasan del D-pad al stick sin cambiar el agarre y que MENU solo se pulsa a propósito.

## Prueba eléctrica escalonada (placa armada)

1. **Sin módulo y sin energía.** No debe haber continuidad entre 3V3 y GND. Comprobar continuidad entre: zócalo pin 38 ↔ J4.1 ↔ J3.1 (GND), pin 36 ↔ J4.2 ↔ J3.2 (3V3), pin 31 ↔ J3.3, pin 32 ↔ J3.4, pin 24 ↔ J4.3, pin 25 ↔ J4.4, pin 27 ↔ J4.5 y pin 26 ↔ J4.6.
2. **Con módulo y USB, sin TFT ni KY.** Medir 3,3 V entre J4.2 (+) y J4.1 (−), y entre J3.2 y J3.1.
3. **TFT.** Enchufarlo y cargar un sketch de color sólido (SPI modo 3). Si el backlight no enciende, unir BLK a 3V3 con un puente de cable en el pin 7 del zócalo.
4. **KY.** Leer GP26/GP27 en reposo (≈ mitad de escala) y en los extremos.
5. **Prueba larga.** 30 min de uso y 10 reconexiones USB. Registrar reinicios, imagen corrupta o entradas falsas.

## Firmware

El borrador Arduino-Pico (`4_Anexos/firmware/`) usa los mismos pines desde D3.1. Para completarlo:

- `INPUT_PULLUP` en GP2..GP9.
- Antes de leer el ADC, deshabilitar la entrada digital del pad en GP26/27 (errata RP2350-E9).
- ST7789 sin CS, en SPI modo 3.
- Mapa HID: flechas, Z (A), X (B) y Escape (MENU).

## Estructura de la carpeta de entrega

| Carpeta | Contenido |
|---|---|
| `1_Diseno_KiCad/` | Proyecto KiCad 9: abrir `Control proyecto 2.kicad_pro`. Incluye las bibliotecas propias (`Control_proyecto_2.kicad_sym`, `Control_proyecto_2.pretty`) con sus tablas `sym-lib-table` y `fp-lib-table`, y la tabla de pines `conexiones-hileras.csv` |
| `2_Gerber_Produccion/` | **`G7_Gerber_D4.4_para_fabricante.zip`** (el archivo que se sube al fabricante), los mismos Gerbers y taladros sueltos para revisarlos, mapas de taladro y `ESPECIFICACION_FABRICACION.txt` (capas, espesor, cobre, acabado) |
| `3_Instrucciones/` | Este README (md y pdf), `RESPUESTA_REVISION_2_D4.4.pdf`, `RESPUESTA_FEEDBACK_D4.3.pdf`, BOM (CSV y XLSX), `planos/` (esquemático en PDF, planos 1:1 frente y dorso, plano mecánico de la tapa, renders), `fotos/` (serigrafía de los módulos) y `verificacion/` (reportes ERC/DRC) |
| `4_Anexos/` | Borrador de firmware y scripts reproducibles del diseño |
