# Lab 2402 · One bad query, three symptoms

Tema 24 · inglés · serverless (Free Edition sirve) · laboratorio con guía HTML.

| Fichero | Qué es |
|---|---|
| `2402-00-create-environment.ipynb` | Setup: catálogo `lab2402.shop` con `customers`, `products`, `orders` y `order_items` (skew forzado: el 25 % de los pedidos con `customer_idx = 0`) y los helpers `file_stats`, `run_fresh`, `benchmark` y `last_runs`. Lo llama el notebook del alumno con `%run` |
| `2402-01-read-less-balance-more-solution.ipynb` | Solución. El alumno crea su propio notebook `2402-01-read-less-balance-more` y lo construye celda a celda con la guía |
| `laboratorio-2402.yaml` → `laboratorio-2402.html` | Guía (motor `05-motores/052-demos-html`), en borrador. El código lo lee de la solución |
| `CAPTURAS.md` · `pictures/` | Qué capturar y las capturas ya marcadas (3 de 14) |

**La historia:**
- **A · la consulta mala:** 0 files pruned, shuffle pesado (Memory peak) y skew (Rows).
- **B · instrucción 1 de Genie:** arreglar el predicado. Files pruned sigue en 0.
- **C · instrucción 2:** `CLUSTER BY (order_date)` + `OPTIMIZE FULL`.

Las tres ejecuciones se comparan con un benchmark honesto y se prueban desde `system.query.history`.

Para repetir A después de C, volver a ejecutar la celda `%run` con `rebuild = yes`.

Copia renumerada del lab 0301 de RevoData (`revodata-spark-performance/demos/lab-0301-read-less-balance-more`).
