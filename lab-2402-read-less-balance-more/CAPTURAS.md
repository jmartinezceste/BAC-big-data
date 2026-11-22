# Capturas del lab 2402: qué hacer y qué marcar

Diseño A → B → C (validado el 21.11 con `2402-validate-demo.ipynb`). Dataset de 4 tablas, `order_items` con `order_date`.

**Cómo se trabaja:**
- Tú haces cada captura **limpia** y la dejas en `screenshots/` (solo local, no se versiona) con su nombre (prefijo `2402-` o `2402-`, da igual).
- Claude la recorta, difumina el email de la cuenta, pone las marcas y la copia a `pictures/` (el original se guarda como `*-raw.png`, que no se sube a git). Después ajusta la guía a lo que se vea.
- **Marca** = recuadro rojo con su número (①②③).

| # | Fichero | Estado | Dónde estás | Qué marcar |
|---|---|---|---|---|
| 1 | `2402-01-setup-run-all.png` | **pendiente** | Tu notebook, salida de la celda `%run` | ① ficheros por tabla (16 / 16 / 32 / 32) ② la fila `guest` con su ~25 % |
| 2 | `2402-02-query-a-result.png` | ✅ hecha | Celda de la query A | ① las filas del cliente `guest` |
| 3b | `2402-03b-query-history.png` | ✅ hecha | Query History (pestaña nueva) | ① filtros de notebook y celda ② la query |
| 3c | `2402-03c-see-query-profile.png` | ✅ hecha | Panel lateral de la query | ① See query profile |
| 4 | `2402-04-a-no-pruning.png` | ✅ hecha | Query Profile de A, panel de detalles | ① Files read ② Files pruned = 0 ③ `▽ 0%` |
| 5 | `2402-05-a-memory-peak-shuffle.png` | ✅ hecha | Query Profile de A: Memory peak + Top operators por Shuffle | ① Memory peak ② Top operators ③ filtro Shuffle ④ Shuffle sobre `oi.order_idx` |
| 6 | `2402-06-a-rows-skew.png` | ✅ hecha | Query Profile de A coloreado por Rows | ① Rows ② Shuffle sobre `o.customer_idx` ③ el Inner Join con `customers` |
| 7 | `2402-07-genie-optimize.png` | ✅ hecha | Query Profile de A → Performance insights | ① icono ② DATA_SKEW ③ Optimize query ④ etiqueta en el grafo |
| 8 | `2402-08-benchmark-a.png` | ✅ hecha | Celda `benchmark("A", QUERY_A)` | ① la mediana |
| 9 | `2402-09-b-still-no-pruning.png` | ✅ hecha | Query Profile de B, panel de detalles | ① Files read ② Files pruned = 0 |
| 10 | `2402-10-benchmark-b.png` | ✅ hecha | Celda `benchmark("B", QUERY_B)` | ① la mediana |
| 11 | `2402-11-cluster-optimize.png` | ✅ hecha | Celda del layout | ① `clustering ['order_date']` y ficheros de las dos tablas |
| 12 | `2402-12-c-everything-right.png` | ✅ hecha | Celda de la query C y su resultado | ① el filtro en `oi.order_date` ② el GROUP BY previo ③ el join con `customers` |
| 12b | `2402-12b-c-profile.png` | ✅ hecha | Query Profile de C | ① Files read 73 (`▽ 36%`) ② Files pruned 41 ③ Tasks total time ④ Shuffle sobre `oi.order_idx` (27,5 M filas) ⑤ el join con `customers` sobre lo ya agregado |
| 13 | `2402-13-benchmark-c.png` | ✅ hecha | Celda `benchmark("C", QUERY_C)` | ① la mediana |
| 14 | `2402-14-proof.png` | ✅ hecha | Celda `compare(QUERY_A, QUERY_C)` | ① las tres medianas ② `same 100 rows: True` |

## Cifras de referencia (`medium`)

- Validación del 21.11: A 9,49 s · B 9,88 s · C 3,83 s.
- Sesión de las capturas (22.11): A 10,29 s · B 9,99 s · C 4,10 s (40 % de A), mismas 100 filas.
- C: 73 ficheros leídos y 41 podados, el shuffle de `order_items` pasa de 55 M a 27,5 M filas, y el tasks total time de 34 s a 19 s.
