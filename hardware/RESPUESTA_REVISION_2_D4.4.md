# Respuesta a la Revisión 2 — G7 · Control proyecto 2

**Revisión revisada:** D4.3 (26/10/2026) · **Revisión entregada:** D4.4 (27/10/2026)  
**Grupo 7 (G7) · IND474** · V. Kohler, G. Hidalgo, F. Guaita, E. Rojas

Este documento responde, en el mismo orden, a las tres correcciones y a la nota menor de la *Revisión 2: estado para fabricación* (26/10/2026). La respuesta a la revisión 1 sigue vigente en `RESPUESTA_FEEDBACK_D4.3.pdf`.

**Verificación de D4.4 (KiCad 9.0.3):**

- ERC: 0 errores y 0 advertencias.
- DRC con `--schematic-parity --severity-all`: 0 violaciones, 0 pads sin conectar, 0 problemas de paridad.
- 0 pads SMD en la placa: todas las huellas son THT o NPTH.
- Esquinas de pista: **0 a 90°**, 176 a 45°, 0 agudas (el script `corners.py` cuenta todos los codos entre dos segmentos de la misma red y capa).
- Gerbers regenerados: contorno de 125,0 × 70,0 mm, 112 PTH (28 vías + 84 pads THT) y 8 NPTH.

---

## Corrección 1: componentes SMD → THT — hecha

| Ref | D4.3 (SMD) | D4.4 (THT) | Huella KiCad |
|---|---|---|---|
| SW1–SW6 | Tact 12 × 12 SMD (PTS125) | Tact 12 × 12 × 7,3 THT de 4 patas (Omron B3F-4055 o genérico), patrón 12,5 × 5 | `Button_Switch_THT:SW_PUSH-12mm` |
| C1 | 100 nF 0805 | 100 nF cerámico de disco, paso 5 mm | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| C2 | 10 µF 1210 | 10 µF / 50 V electrolítico radial Ø5 × 11, paso 2 mm | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` |
| JP1 | Puente de soldadura | **Eliminado**. BLK (J4.7) queda sin conectar, como ya estaba (el backlight enciende por defecto) | — |

Detalles:

- **Courtyards.** La huella THT de 12 mm ocupa 15,5 × 14,5 mm de courtyard, más que el paso de 12,75 de D4.3. El D-pad queda a **14,5 mm en vertical y 12,5 mm en horizontal** desde su centro, que es el mínimo sin solapar courtyards. RIGHT no puede ir más a la derecha porque llega a la fila de pines del módulo (J2). Nuevos centros: UP (22; 24), DOWN (22; 53), LEFT (9,5; 38,5), RIGHT (34,5; 38,5). A, B y MENU no cambian.
- **Ergonomía** (mismo modelo del estudio: base del pulgar a 44,5 mm de radio cómodo): UP a 46,0 mm (D4.3: 45,8; D3.1: 54,8), LEFT 33,2, RIGHT 34,7, DOWN 17,1. El cuerpo de LEFT queda a 3,5 mm del canto. A–B sigue a 17,9 mm y el stick a 43,2 mm.
- **C1/C2 junto a J4:** C1 a 4,0–4,6 mm de J4.2 y C2 a 8,9–9,7 mm, ambos ≤ 10 mm y fuera de la huella del TFT. El "+" de C2 va serigrafiado en el pad cuadrado.
- **BOM** actualizada (`BOM_D4.4.csv` / `.xlsx`). Los pulsadores THT, el disco y el electrolítico figuran como "POR COMPRAR", porque el kit de pulsadores que tenemos es SMD.
- Re-ruteo completo, DRC con paridad en 0 y Gerbers nuevos. El zip de D4.3 queda obsoleto.

## Corrección 2: pistas a 90° → 45° — hecha

Se aplicó la opción 2 recomendada (postproceso reproducible), más una pasada de verificación:

1. **`router.py`** ahora achaflana cada codo recto al generar la ruta (función `chamfer_net`). Prueba d = 1,0 mm, luego d/2 y d/4, y solo acepta el chaflán si el tramo nuevo no se acerca a menos de la holgura de ningún obstáculo. Los extremos de cada ruta se ajustan al centro del pad, así no quedan tramos cortos que formen ángulos agudos.
2. **`corners.py fix`** recorre los codos que quedaron rectos (por falta de espacio), prueba chaflanes de 0,8 a 0,12 mm y conserva cada uno solo si el DRC no empeora.
3. **`corners.py`** cuenta el resultado sobre el `.kicad_pcb` final.

Resultado: **0 esquinas a 90°** (en D4.3 había 156), 176 a 45° y 0 agudas. Las pistas de +3V3 siguen todas a 0,6 mm (netclass PWR) y la holgura mínima sigue en 0,25 mm. Como todo está en los scripts, regenerar la placa no pierde los chaflanes.

## Corrección 3: J4 frente a la línea H6/H8 — revisada con la pieza real; J4 se mantiene

La revisión indica comprobarlo con la pantalla real y, *"si la pieza real tuviera los pines a 1,5 mm del borde, dejarlo como está y anotar la medida"*. Eso es lo que muestran las tres fuentes que tenemos:

| Fuente | Pines al borde | Agujeros al borde | Diferencia |
|---|---|---|---|
| Plano del vendedor ZJY-IPS130 (cotas "1.50" y "2.50") | 1,50 mm | 2,50 mm | 1,0 mm |
| Modelo 3D de GrabCAD del mismo módulo | 1,53 mm | 2,50 mm | ~1,0 mm |
| Foto de nuestra pantalla, escalada con el paso real de los agujeros (22,78 mm) | — | — | 1,0–1,1 mm |

En la pieza la fila de pines **no** está en el eje de los agujeros: está 1,0 mm más cerca del borde. Por eso J4 queda en x = 100,94 y los agujeros H6/H8 en x = 99,94. Si J4 se moviera a 99,94, los pines quedarían 1,0 mm fuera del zócalo.

La foto anotada está en `3_Instrucciones/fotos/TFT_pines_vs_agujeros_anotado.png` y la medida va anotada en el README ("Mecánica"). En Y la posición ya estaba bien según la revisión (J4.1 a 6,27 mm del borde).

Antes de pedir la PCB se hará la comprobación del paso 1: la pantalla real sobre `D4.4_frente_1a1.pdf` impreso al 100 %.

## Nota menor: orientación del cable XH al KY-023 — hecha

- En la serigrafía, junto a J3, el pin 1 está rotulado "GND".
- En el README (montaje) se indica **marcar el hilo GND del cable con marcador o termorretráctil en los dos extremos** y hacer coincidir esa marca con el GND del KY-023 (primer pin de su serigrafía) y con el pin 1 de J3. En el plano de la tapa se anota "GND" junto a la salida del cable.

## Lista de "Lo que falta antes de fabricar"

| Ítem | Estado |
|---|---|
| SW1–SW6, C1, C2 y JP1 a THT; BOM | ✅ Hecho (JP1 eliminado) |
| Todas las esquinas a 45° | ✅ 0 esquinas a 90° |
| J4 vs H6/H8 con la pantalla real | ✅ Medido: los pines están a 1,5 mm del borde, así que J4 se mantiene. Falta la prueba sobre el papel 1:1 |
| ERC 0, DRC con paridad 0, zip D4.4, README y plano | ✅ Hecho |
| Impresión 1:1 con piezas reales y fotos | ⏳ Pendiente: requiere los pulsadores THT, que hay que comprar |
| Maqueta ergonómica con 3 personas | ⏳ Pendiente |
| Pedido a JLCPCB revisando el zip en su visor | ⏳ Después de los dos puntos anteriores |
