# Capturas del lab 2402: qué hacer y qué marcar

Lista para el ensayo, con el dataset de 4 tablas (`customers`, `products`, `orders`, `order_items`).

**Cómo se trabaja:**
- Tú haces cada captura **limpia** y la dejas en `screenshots/` (solo local, no se versiona) con su nombre exacto.
- Claude la recorta, difumina el email de la cuenta, pone las marcas y la copia a `pictures/` (el original se guarda como `*-raw.png`). Después ajusta la guía a lo que se vea en la captura.
- **Marca** = recuadro rojo con su número (①②③).
- Haz las capturas en inglés. El tema oscuro de Databricks sirve.

| # | Fichero | Estado | Dónde estás | Qué tiene que salir | Qué marcar |
|---|---|---|---|---|---|
| 1 | `2402-01-setup-run-all.png` | **pendiente** | Tu notebook `2402-01`, salida de la celda `%run` | Las 4 líneas de `file_stats` y la tabla por tier | ① ficheros de `orders` ② la fila `guest` con su ~25 % |
| 2 | `2402-02-query-a-result.png` | **pendiente** | Celda de la query A | La tabla de resultados, primeras filas | ① las filas del cliente `guest` arriba del todo |
| 3 | `2402-03-a-open-profile.png` | ✅ hecha | Bajo la celda de A | La tira de rendimiento | ① **Hide/Show performance** ② **View all in query history** |
| 3b | `2402-03b-query-history.png` | ✅ hecha | Query History (pestaña nueva) | Filtrado por la celda | ① los filtros de notebook y celda ② la query |
| 3c | `2402-03c-see-query-profile.png` | ✅ hecha, **repetir** | Panel lateral de la query | El panel con **See query profile** | ① **See query profile**. Las cifras del panel son del dataset viejo: repetirla con A del lab nuevo |
| 4 | `2402-04-a-no-pruning.png` | **pendiente** | Query Profile de A, panel de detalles | Tiles y bloque *Files & partitions* | ① **Files read** ② **Files pruned = 0** ③ el `▽ 0%` |
| 5 | `2402-05-a-memory-peak-shuffle.png` | **pendiente** | Query Profile de A: coloreado **Memory peak** + **Top operators** filtrado por Shuffle | Lista a la izquierda, grafo en el centro y el panel del Shuffle mayor a la derecha | ① botón **Memory peak** ② icono **Top operators** ③ filtro **Shuffle** ④ el Shuffle mayor en la lista y en el grafo |
| 6 | `2402-06-a-rows-skew.png` | **pendiente** | Query Profile de A: coloreado **Rows**, clic en el Shuffle por `customer_idx` (bajo el join con `customers`) | Grafo + panel del Shuffle | ① botón **Rows** ② el camino más oscuro ③ el Shuffle por `customer_idx` ④ en su panel, la métrica que enseñe el reparto (particiones, skew de AQE, tiempos) |
| 7 | `2402-07-genie-optimize.png` | opcional | Solo en un workspace con **Performance Insights**: Query Profile de A → **Optimize** | El panel de Genie Code | ① **Optimize** ② la recomendación ③ los dos pasos. Si no hay workspace con la preview, se quita el `cap` |
| 8 | `2402-08-benchmark-a.png` | **pendiente** | Celda `benchmark("A", QUERY_A)` | Las 5 ejecuciones y la mediana | ① la mediana |
| 9 | `2402-09-b-still-no-pruning.png` | **pendiente** | Query Profile de B, panel de detalles | Igual que la 4 | ① **Files pruned = 0**, todavía |
| 10 | `2402-10-benchmark-b.png` | **pendiente** | Celda `benchmark("B", QUERY_B)` | Las 5 ejecuciones y la mediana | ① la mediana |
| 11 | `2402-11-cluster-optimize.png` | **pendiente** | Celda del layout | Salida de `file_stats` de `orders` y `order_items` | ① `clustering ['order_date']` ② el número de ficheros |
| 12 | `2402-12-c-pruning.png` | **pendiente** | Query Profile de B después del layout, **clic en el Scan de `orders`** | Panel del operador a la derecha | ① **Files pruned** del Scan (≈ la mitad) ② **Files read**. No el panel de detalles: su % cuenta las cuatro tablas |
| 13 | `2402-13-benchmark-c.png` | **pendiente** | Celda `benchmark("C", QUERY_B)` + Top operators de C | La mediana y la lista de operadores | ① la mediana ② el % de Shuffle frente al de Scan |
| 15 | `2402-15-d-move-less.png` | **pendiente** | Query Profile de D, coloreado por **Memory peak**, clic en el Shuffle sobre `oi.order_idx` | Grafo + panel del Shuffle | ① el Shuffle de `order_items`, con muchas menos filas y memoria que en A ② Files pruned del Scan de `order_items` |
| 16 | `2402-16-benchmark-d.png` | **pendiente** | Celda `benchmark("D", QUERY_D)` | Las 5 ejecuciones y la mediana | ① la mediana, frente a la de A |
| 14 | `2402-14-proof.png` | **pendiente** | Celda `last_runs()` | La tabla con A, B, C y D | ① `pruned_files` ② `shuffle_mb` ③ `any_cache_hit = 0` |

## Mientras haces las capturas, apunta los números

De las capturas 4, 5, 6, 9, 12 y 14:
- ficheros leídos y podados de A, B y C;
- la memoria del Shuffle mayor;
- wall-clock y task time;
- las tres medianas.

Las slides y la guía solo usan cifras medidas.

Si la recomendación real de Genie Code (captura 7) no coincide con el texto del bloque G, manda la captura y ajusto el bloque a lo que diga de verdad.
