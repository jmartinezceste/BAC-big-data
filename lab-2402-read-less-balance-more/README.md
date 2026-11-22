# Lab 2402 · One bad query, three symptoms

Tema 24 · inglés · serverless (Free Edition sirve) · laboratorio con guía HTML.

| Fichero | Qué es |
|---|---|
| `2402-00-create-environment.ipynb` | Setup: catálogo `lab2402.shop` con `customers`, `products`, `orders` y `order_items` (skew forzado: el 25 % de los pedidos con `customer_idx = 0`) y los helpers `file_stats`, `run_fresh`, `benchmark` y `compare`. Lo llama el notebook del alumno con `%run` |
| `2402-01-read-less-balance-more-solution.ipynb` | Solución. El alumno crea su propio notebook `2402-01-read-less-balance-more` y lo construye celda a celda con la guía |
| `laboratorio-2402.yaml` → `laboratorio-2402.html` | Guía (motor `05-motores/052-demos-html`), en borrador. El código lo lee de la solución |
| `CAPTURAS.md` · `pictures/` | Qué capturar y las capturas ya marcadas (10 de 15) |

**La historia** (top 100 de clientes por ingresos de 2024):
- **A · la consulta mala:** 0 files pruned, shuffle pesado (Memory peak) y skew (Rows y la insight DATA_SKEW).
- **B · instrucción 1 de Genie:** arreglar el predicado. Files pruned sigue en 0 y el tiempo no cambia.
- **C · todo bien:** layout clusterizado por `order_date` en `orders` y `order_items`, filtro también en `oi.order_date` y agregación antes del join con `customers`. Mismas 100 filas que A, en una fracción del tiempo (validación: 9,5 s → 3,8 s).

El benchmark usa el sink `noop` para medir el motor y no el viaje del resultado. `compare()` compara las medianas y comprueba que A y C dan la misma respuesta.

Para repetir A después de C, volver a ejecutar la celda `%run` con `rebuild = yes`.
