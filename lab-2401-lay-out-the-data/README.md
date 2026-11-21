# Lab 2401 · Lay out the data: from small files to liquid clustering

Tema 24 · inglés · serverless (Free Edition sirve).

| Fichero | Qué es |
|---|---|
| `2401-00-create-environment.ipynb` | Setup: catálogo `lab2401`, schema `layout`, volumen para las tablas por ruta de la parte A, las dos tablas grandes de la parte B y los helpers (`file_stats`, `show_files`, `last_commits`, `path_table`). Lo llama el lab con `%run` |
| `2401-01-lay-out-the-data.ipynb` | El lab (notebook SQL con celdas `%python`) |

**Parte A · la mecánica (1 M filas):**
1. 200 ficheros pequeños.
2. OPTIMIZE: compacta, pero no ordena.
3. min/max por fichero.
4. ZORDER BY (id).
5. Con datos nuevos, Z-order reescribe toda la tabla.
6. PARTITIONED BY (year) no ayuda a filtrar por id.
7. CLUSTER BY (id) + OPTIMIZE.
8. Con datos nuevos, liquid clustering solo reescribe lo nuevo.

**Parte B · la prueba:** la misma consulta de una semana sobre una tabla gestionada desordenada y otra clusterizada. El run 1 en frío y el run 2 en caliente; en el Query Profile se miran files pruned, bytes read y task time.

Copia renumerada de la demo 00 de RevoData (`revodata-spark-performance/demos/00-lay-out-the-data`).
