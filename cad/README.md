# CAD — Carcasa v6

| Archivo | Contenido |
|---|---|
| `Control_G7_v6.f3d` | Proyecto Fusion 360 (carcasa, capuchones, perilla, separadores, PCB y componentes) |
| `Control_G7_v6_ensamble.step` | Ensamble completo en STEP |
| `G7_D4.4_placa.step` | PCB D4.4 con componentes |
| `stl/` | 14 piezas listas para imprimir en la Bambu A1 |
| `renders/` | Vistas de la carcasa v6 |
| `scripts_fusion/` | Scripts de Fusion que generan la geometría (`build.py` → `finish.py` → `extras.py` → `fix2.py`) y sus datos |
| `modelos_componentes/` | Modelos 3D de los componentes (KY-023, pulsadores, RP2350-Plus, TFT) |

Medidas: 184 × 137 × 52 mm · pared 2,4 mm · 4 × M2×6 · 6 clips. Decisiones en [`../DECISIONES.md`](../DECISIONES.md).

## Impresión (Bambu A1)

- Tapa: cara de botones contra la cama.
- Pared: 6 perímetros (2,4 mm con boquilla de 0,4).
- ⏳ Imprimir primero la probeta de holguras.
