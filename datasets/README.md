# Datasets sintéticos para las demos de ingesta

Versión 1.2 · 27 de septiembre de 2026 (la del [manifiesto](manifest.json)). Datos ficticios y deterministas, generados para los laboratorios 0501–0505, reconstruidos a partir de los vídeos. No son los archivos originales de Databricks Academy. Todos los correos pertenecen a `example.com`.

En el repositorio del alumnado esta carpeta vive en la raíz, junto a las carpetas `lab-050X-…`. Cada laboratorio la lee desde su `00_preparar_entorno`, que copia al volumen solo los ficheros que necesita y comprueba sus recuentos. **Ningún laboratorio se ha ejecutado todavía en Databricks.**

## Inventario

| Grupo / archivo | Filas de datos | Uso |
|---|---:|---|
| `users-historical/part-00000.snappy.parquet` | 62.876 | Histórico de usuarios |
| `users-historical/part-00001.snappy.parquet` | 62.875 | Histórico de usuarios |
| `users-historical/part-00002.snappy.parquet` | 62.875 | Histórico de usuarios |
| `users-historical/part-00003.snappy.parquet` | 62.875 | Histórico de usuarios |
| **Total usuarios** | **251.501** | lab-0501 y lab-0503 |
| `sales-csv/000.csv` | 3.149 | Lote inicial de lab-0502; ventas de lab-0504 |
| `sales-csv/001.csv` | 2.932 | Segundo lote de lab-0502; ventas de lab-0504 |
| `sales-csv/002.csv` | 3.200 | Ventas de lab-0504 |
| `sales-csv/003.csv` | 3.203 | Ventas de lab-0504 |
| **Total ventas** | **12.484** | Los cuatro archivos juntos |
| `csv-demo-files/malformed_example_1_data.csv` | 4 | lab-0504: un timestamp incompatible con BIGINT |
| `csv-demo-files/malformed_example_2_data.csv` | 4 | lab-0504: falta el primer nombre de cabecera |
| `events-kafka/000.json` | 1.126 | lab-0505: primera mitad de los eventos de la demo |
| `events-kafka/001.json` | 1.126 | lab-0505: segunda mitad de los eventos de la demo |
| `events-kafka/002.json`–`005.json` | 1.900 | Lotes adicionales para prácticas incrementales; **ningún laboratorio los usa todavía** |
| `events-kafka/006.json`–`007.json` | 1.100 | lab-0505, extensión opcional: traen el campo nuevo `campaign` |
| **Total eventos Kafka** | **5.252** | Los ocho archivos juntos |

Las filas CSV de esta tabla no incluyen la cabecera. Los tamaños de `002.csv` y `003.csv` son decisiones del dataset sintético; no se presentan como recuentos confirmados de esos archivos en el vídeo.

El [manifiesto](manifest.json) contiene tamaños, recuentos, defectos deliberados y SHA-256 de los dieciocho archivos. No se incluyen archivos auxiliares en los directorios de datos.

## Correspondencia con los laboratorios

| Laboratorio | Archivos | Parámetros que hay que configurar |
|---|---|---|
| [lab-0501 · CTAS y COPY INTO](../lab-0501-ingest-ctas-copy-into/01_ingesta_ctas_copy_into.ipynb) | Los cuatro Parquet de `users-historical/` | Ninguno: `00_preparar_entorno` crea el catálogo `lab0501` y carga los ficheros desde `datasets/` |
| [lab-0502 · Streaming tables y Auto Loader](../lab-0502-streaming/01_streaming_tables_auto_loader.ipynb) | Primero `sales-csv/000.csv`; después `001.csv` | Ninguno: `00_preparar_entorno` crea el catálogo `lab0502` y carga los ficheros desde `datasets/` |
| [lab-0503 · Metadatos de ingesta](../lab-0503-metadatos-ingesta/01_metadatos_ingesta.ipynb) | Los mismos cuatro Parquet de `users-historical/` | Ninguno: `00_preparar_entorno` crea el catálogo `lab0503` y carga los ficheros desde `datasets/` |
| [lab-0504 · CSV y datos rescatados](../lab-0504-ingest-csv-rescued-data/01_ingesta_csv_rescued_data.ipynb) | Los cuatro `sales-csv/*.csv` y los dos `csv-demo-files/*.csv` | Ninguno: `00_preparar_entorno` crea el catálogo `lab0504` y carga los ficheros desde `datasets/` |
| [lab-0505 · JSON, Base64, STRUCT y VARIANT](../lab-0505-ingest-json/01_ingesta_json.ipynb) | `000.json` y `001.json` (demo, 2.252 eventos); `006.json` y `007.json` (extensión con `campaign`) | Ninguno: `00_preparar_entorno` crea el catálogo `lab0505` y carga los ficheros desde `datasets/` |

Cada laboratorio tiene su propio catálogo (`lab0501`…`lab0505`) y rutas `/Volumes/...` fijas, así que el alumnado no configura nada. Si cambias el nombre o el contenido de un fichero de esta carpeta, revisa los recuentos esperados en el `00_preparar_entorno` de cada laboratorio que lo usa: se detiene si no cuadran.

## Grupo A: usuarios en Parquet

Esquema idéntico en los cuatro archivos, escritos con PyArrow 25.0.1, formato Parquet 2.6 y compresión Snappy:

| Campo | Tipo físico/lógico | Contenido |
|---|---|---|
| `user_id` | STRING | Identificador único, por ejemplo `U000000001` |
| `user_first_touch_timestamp` | INT64 / BIGINT | Microsegundos desde el epoch Unix, fechas de junio de 2020 en UTC |
| `email` | STRING nullable | Correo ficticio o nulo |

Hay **25.151 correos nulos** deliberados. No hay usuarios duplicados. Se cubren los 30 días de junio. No existen columnas de metadatos ni de rescate en el origen: las añaden `read_files` (`_rescued_data`) y lab-0503 (`_metadata`).

Resultados esperados: CTAS, COPY INTO y PySpark deben obtener 251.501 filas. La conversión del timestamp a DATE utiliza microsegundos y UTC. Repetir COPY INTO con el mismo destino y los archivos intactos no debe añadir filas.

## Grupo B: ventas CSV

Codificación UTF-8 sin BOM, finales de línea CRLF, cabecera en cada archivo y delimitador `|`. Todos los campos están entre comillas dobles; las comillas internas del JSON se escapan con barra inversa (`\`). El texto JSON se valida **después** de interpretar el CSV.

Opciones de lectura: `header=true`, `sep='|'`, `quote='"'`, `escape='\'`. Las dos últimas coinciden con las opciones por defecto de Spark, así que `read_files` con solo `sep` y `header` lee bien los cuatro ficheros (comprobado con Spark 3.5 en local). Para leer localmente con Python, usar `csv.reader(..., delimiter='|', quotechar='"', escapechar='\\', doublequote=False)`.

No abrir y volver a guardar estos archivos con una aplicación que cambie el separador, las unidades temporales o el escapado.

| Columna | Tipo de negocio esperado | Reglas |
|---|---|---|
| `order_id` | INT | Único en todo el grupo; de 298.592 a 311.075 |
| `email` | STRING | Existe como correo no nulo del histórico de usuarios |
| `transactions_timestamp` | BIGINT | Microsegundos; posterior al primer contacto del usuario |
| `total_item_quantity` | INT | Suma de cantidades en `items` |
| `purchase_revenue_in_usd` | DECIMAL(12,2) conceptual | Total del pedido; el lector puede inferir DOUBLE |
| `unique_items` | INT | Número de productos distintos en el pedido |
| `items` | STRING que contiene JSON | Lista de productos; no una columna ARRAY en el CSV |

Cada objeto de `items` contiene `item_id`, `item_name`, `quantity`, `price_in_usd`, `item_revenue_in_usd` y `coupon`. El cupón es nulo; no se aplican descuentos, impuestos ni gastos de envío. Los importes por línea son precio por cantidad y suman el total del pedido.

### Secuencia de lab-0502 (Auto Loader)

1. `00_preparar_entorno` deja en `/Volumes/lab0502/upload/upload` **solo `000.csv`** y comprueba **3.149 filas**.
2. La parte SQL crea la streaming table: **3.149 filas**.
3. El notebook copia `001.csv` desde `datasets/`, conservando `000.csv` intacto.
4. Refrescar: deben añadirse **2.932 filas**, total **6.081**.
5. Refrescar sin nuevos archivos: el total debe permanecer en **6.081**.
6. El apéndice de Python vuelve a ejecutar `00_preparar_entorno` (solo `000.csv`, checkpoint vacío) y repite la secuencia.

No añadir `002.csv` ni `003.csv` al volumen `upload` de lab-0502. lab-0504 sí carga los cuatro lotes, en su propio catálogo, y obtiene 12.484 filas.

La única copia canónica local de cada lote está en `sales-csv/`. Las entradas remotas separadas son estados de ejecución de prácticas distintas, no nuevas copias de material didáctico en el repositorio.

PySpark necesita además un volumen de estado con una carpeta exclusiva por consulta: en lab-0502 es `/Volumes/lab0502/streaming/checkpoints/python_csv_autoloader`. **No hay que fabricar checkpoints locales**, ni compartirlos entre SQL y Python, ni cambiarlos entre los dos lotes de una misma práctica.

## Grupo C: defectos controlados

Ambos archivos tienen cuatro filas, tres posiciones por fila, UTF-8 y separador `|`. Parten de los cuatro primeros pedidos del grupo B como ejemplos reconocibles, pero son fixtures independientes de diagnóstico.

### malformed_example_1_data.csv

Cabecera completa `order_id|email|transactions_timestamp`. El primer pedido conserva su identificador y correo, pero su timestamp se sustituye por **`aaa`**. Las otras tres marcas son enteros válidos.

Resultado previsto: la inferencia puede escoger STRING; al declarar BIGINT, el campo incompatible queda nulo y el valor original puede inspeccionarse en `_rescued_data`. La fila debe conservarse. En local (Spark 3.5) se comprobó la parte estándar: sin esquema la columna se infiere como STRING y, con el esquema de lab-0504, se conservan las 4 filas y la del `aaa` queda con el timestamp a `NULL`. Que el `aaa` llegue a `_rescued_data` es propio de Databricks y sigue pendiente de la primera ejecución.

### malformed_example_2_data.csv

Cabecera exacta `|email|transactions_timestamp`: solo falta el nombre `order_id`, no toda la cabecera. Los cuatro identificadores están presentes en las filas, son numéricos y caben en INT.

Resultado previsto según el vídeo: Databricks no crea columna para el campo sin nombre, lo recoge en `_rescued_data` bajo la clave `_c0` (junto a `_file_path`) y lab-0504 lo recupera con `cast(_rescued_data:_c0 AS BIGINT)`. En Spark de código abierto el mismo fichero produce en cambio una columna normal `_c0`; el comportamiento de Databricks sigue pendiente de la primera ejecución. No existe aquí un defecto de número de columnas ni de comillas.

## Grupo D: eventos JSON exportados de Kafka

Los ocho archivos `events-kafka/000.json`–`007.json` usan JSON Lines en UTF-8 con finales LF. Cada línea contiene un sobre con `key`, `offset`, `partition`, `timestamp`, `topic` y `value`. `key` y `value` son cadenas Base64 válidas; al decodificar `value` se obtiene el evento JSON que trabaja lab-0505.

Los 2.252 eventos originales (`000.json` y `001.json`) se reparten en tres particiones con offsets contiguos. Hay 300 eventos con artículos, 50 con `items: null` y 1.902 con `items: []`. Los arrays con artículos producen exactamente 506 filas al aplicar `explode`. Se incluyen compras con uno y tres artículos, cupones nulos y no nulos, objetos `ecommerce` completos y vacíos, diferentes dispositivos, fuentes de tráfico y ubicaciones.

El timestamp del sobre está en milisegundos y los timestamps interiores en microsegundos. La clave decodificada coincide con `user_id`, pero puede repetirse entre eventos; la posición de origen se identifica con `topic`, `partition` y `offset`.

### Ampliación del 2026-09-27

Se añadieron seis archivos sintéticos sin modificar `000.json` ni `001.json`.
Mantienen el sobre Kafka, Base64, tres particiones y offsets contiguos y únicos
por partición en todo el conjunto. Cada lote nuevo representa un día posterior.
Los usuarios se repiten y sus timestamps avanzan; no se han añadido duplicados
de la combinación `topic`, `partition`, `offset`.

| Archivo | Eventos | Filas de artículos con `explode` |
|---|---:|---:|
| `000.json` | 1126 | 506 |
| `001.json` | 1126 | 0 |
| `002.json` | 400 | 400 |
| `003.json` | 500 | 500 |
| `004.json` | 600 | 600 |
| `005.json` | 400 | 400 |
| `006.json` | 500 | 500 |
| `007.json` | 600 | 600 |
| **Total** | **5252** | **3506** |

Los lotes nuevos contienen compras de 1–4 artículos, cantidades de 1–3 unidades,
arrays vacíos y nulos, cupones ausentes o nulos, ciudades con caracteres UTF-8,
distintos dispositivos y fuentes de tráfico. Los importes son precio por cantidad,
sin descuentos. `006.json` y `007.json` incorporan un objeto opcional `campaign`
para comprobar que STRING/VARIANT lo conservan y que el STRUCT fijo de lab-0505
lo descarta (167 eventos en `006.json` y 200 en `007.json`: 367 en total).

Para practicar llegadas incrementales, comienza con `000.json` y `001.json`
en una carpeta de entrada del volumen y añade los nuevos archivos de uno en uno.
lab-0505 hace cargas batch con creación/reemplazo de tablas: por sí solo
no demuestra Auto Loader ni evita releer archivos. Para esa comparación utiliza
un flujo incremental con su checkpoint, como el de lab-0502, adaptando lector,
esquema y rutas a JSON.

Los recuentos de 2.252 eventos y 506 artículos del vídeo solo se reproducen con
los dos archivos originales. Al leer toda la carpeta se obtienen los nuevos
totales de esta tabla. Por eso lab-0505 carga solo esos dos en su carpeta principal.

La ampliación se generó sin aleatoriedad, rotando usuarios y productos del
conjunto original; los hashes y recuentos quedan registrados en manifest.json.

## Dónde los carga cada laboratorio

Carpetas que crea cada `00_preparar_entorno` al ejecutarse:

| Uso | Ubicación |
|---|---|
| Parquet de lab-0501 | `/Volumes/lab0501/upload/upload/users-historical` |
| Parquet de lab-0503 | `/Volumes/lab0503/upload/upload/users-historical` |
| Todos los CSV de ventas de lab-0504 | `/Volumes/lab0504/upload/upload/sales-csv` |
| Defectos de lab-0504 | `/Volumes/lab0504/upload/upload/csv-demo-files` |
| Eventos Kafka de lab-0505 | `/Volumes/lab0505/upload/upload/events-kafka` y `…/events-kafka-extra` |
| Entrada de lab-0502 (SQL y Python) | `/Volumes/lab0502/upload/upload` |
| Estado exclusivo del apéndice Python de lab-0502 | `/Volumes/lab0502/streaming/checkpoints/python_csv_autoloader` |

Ningún laboratorio lee `datasets/` directamente como origen: mezcla formatos, fixtures defectuosos y documentación. Cada `00_preparar_entorno` copia solo el grupo o los archivos concretos que necesita.

## Validación local realizada

- Relectura de todos los Parquet: esquema, número de filas, compresión Snappy y correos nulos.
- Unicidad de usuarios y pedidos; correos de ventas presentes en el histórico.
- Marcas temporales en microsegundos y pedidos posteriores al primer contacto.
- Relectura completa de los CSV con su dialecto, cabeceras, siete campos y recuentos.
- Parseo de los 12.484 valores JSON de `items`; cantidades, productos distintos e importes comprobados con aritmética decimal.
- Comprobación de los dos defectos exactos y de la ausencia de anomalías adicionales en esos fixtures.
- Validación inicial: decodificación de las 2.252 claves y valores Base64, estructura del sobre Kafka, offsets por partición, JSON interior y 506 filas de artículos.
- SHA-256 para detectar cambios posteriores.
- 3 de octubre de 2026, con Spark 3.5 en local, contra lo que afirman los laboratorios: los 18 SHA-256, recuentos totales y por fichero, esquemas Parquet, tipos inferidos de los CSV, JSON de `items`, zona horaria de `first_touch_date`, esquema STRUCT de lab-0505 (lee los 2.252 eventos sin nulos), 506 filas con `explode` y 2.458 con `explode_outer`.

**Pendiente en Databricks:** `read_files` real, contenido exacto de `_rescued_data` y `_c0`, CTAS, COPY INTO, streaming tables, checkpoints, idempotencia y VARIANT. Pasar los controles locales no sustituye esas pruebas.

## Reproducibilidad del contenido

No se utilizó aleatoriedad ni la hora de ejecución. Índices de usuario `i=0..251500`, epoch base `1590969600000000` y día `86400000000`, ambos en microsegundos:

- ID: `U` seguido del índice con nueve dígitos.
- Primer contacto: `base + (i * 104729000) % (30 * dia)`.
- Correo nulo cuando `i % 10 == 0`; en otro caso `user{indice:09d}@example.com`.
- Distribución de filas Parquet según el inventario; row groups de 16.384 filas.
- Pedido global `k=0..12483`: ID `298592+k`; usuario `(17*k+1)%251501`, incrementándolo en uno si es múltiplo de diez.
- Timestamp del pedido: `base + 60*dia + k*300000001`.
- Productos por pedido: `1+k%3`. Para posición `j` desde cero, producto `(k+j)%8` y cantidad `1+(k+j)%2`.
- Catálogo ordenado, precios en centavos: `M_STAN_T/85050`, `M_PREM_T/109260`, `M_STAN_K/107550`, `M_STAN_Q/94050`, `M_PREM_K/179550`, `PILLOW/4550`, `SHEETS/7950`, `BASE/24900`.
- Nombres correspondientes: Standard Twin Mattress, Premium Twin Mattress, Standard King Mattress, Standard Queen Mattress, Premium King Mattress, Memory Foam Pillow, Cotton Sheets, Bed Base.
- JSON compacto sin espacios, campos en el orden documentado; importes calculados desde centavos enteros. División en lotes según el inventario.
- Fixtures: primeros cuatro pedidos, conservando solo las tres primeras columnas y aplicando el defecto indicado.
- Eventos Kafka: 2.252 mensajes repartidos en dos archivos de 1.126 líneas y tres particiones; offsets contiguos por partición. Los primeros 197 eventos tienen un artículo, los siguientes 103 tienen tres, los siguientes 50 usan `items: null` y los 1.902 restantes `items: []`. El total de artículos es 506. `key` contiene el `user_id` en Base64 y `value` contiene el evento JSON compacto en Base64.

Los hashes identifican esta entrega concreta; otra versión de un escritor Parquet puede producir bytes distintos con idéntico contenido lógico. No se ha incorporado un generador persistente al producto ni se ha creado un motor nuevo.
