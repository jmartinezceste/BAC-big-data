"""Tarea de validacion con cuarentena: las filas buenas a silver, las malas aparte.

Evoluciona el validador del laboratorio 1001, que solo informaba. Aqui cada fila
se comprueba contra las reglas de esquemas.json y, si incumple alguna, va a la
tabla de cuarentena con una columna `motivo` que dice QUE regla ha fallado. Asi
nadie tiene que adivinar por que una fila no llego a silver.

Reglas (todas salen de esquemas.json, ninguna esta escrita en el codigo):
  - clave primaria nula o duplicada          -> pk_nula / pk_duplicada
  - columna obligatoria nula o en blanco      -> nulo:<columna>
  - valor numerico fuera de su rango          -> rango:<columna>

Parametros:
  --input_table       tabla bronze de entrada
  --output_table      tabla silver con las filas validas
  --quarantine_table  tabla de cuarentena con las filas invalidas y su motivo
  --config_path       ruta de esquemas.json en el volumen
  --table_name        clave de la tabla dentro de esquemas.json
"""
import argparse
import json
from functools import reduce

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F

spark = SparkSession.builder.getOrCreate()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input_table", required=True)
    p.add_argument("--output_table", required=True)
    p.add_argument("--quarantine_table", required=True)
    p.add_argument("--config_path", required=True)
    p.add_argument("--table_name", required=True)
    args = p.parse_args()

    with open(args.config_path, encoding="utf-8") as f:
        esquema = json.load(f)[args.table_name]

    df = spark.table(args.input_table).select(*esquema["expected_columns"])
    tipos = {c["name"]: c["type"].lower() for c in esquema["columns"]}
    obligatorias = [c["name"] for c in esquema["columns"] if not c.get("nullable", True)]
    pk = esquema.get("pk", [])

    # Cada regla es (condicion de fallo, etiqueta). Se evaluan todas a la vez.
    reglas = []
    if pk:
        reglas.append((reduce(lambda x, y: x | y, [F.col(c).isNull() for c in pk]), "pk_nula"))
        repeticiones = F.count(F.lit(1)).over(Window.partitionBy(*pk))
        reglas.append((repeticiones > 1, "pk_duplicada"))
    for c in obligatorias:
        falla = F.col(c).isNull()
        if tipos.get(c) == "string":
            falla = falla | (F.trim(F.col(c)) == "")
        reglas.append((falla, f"nulo:{c}"))
    for c, (lo, hi) in esquema.get("numeric_ranges", {}).items():
        reglas.append((F.col(c).isNotNull() & ((F.col(c) < lo) | (F.col(c) > hi)), f"rango:{c}"))

    etiquetas = F.array(*[F.when(cond, F.lit(txt)) for cond, txt in reglas])
    df = (df.withColumn("_motivos", F.filter(etiquetas, lambda x: x.isNotNull()))
            .withColumn("motivo", F.concat_ws(", ", "_motivos"))
            .withColumn("_es_mala", F.size("_motivos") > 0)
            .drop("_motivos"))

    validas = df.filter(~F.col("_es_mala")).drop("_es_mala", "motivo")
    malas = (df.filter(F.col("_es_mala")).drop("_es_mala")
               .withColumn("fecha_validacion", F.current_timestamp()))

    # overwrite en las dos: cada ejecucion recalcula silver y cuarentena desde
    # bronze, asi relanzar el job nunca duplica filas
    validas.write.format("delta").mode("overwrite").saveAsTable(args.output_table)
    malas.write.format("delta").mode("overwrite").option("overwriteSchema", "true") \
         .saveAsTable(args.quarantine_table)

    print(f"{args.input_table}: {validas.count()} validas -> {args.output_table}, "
          f"{malas.count()} en cuarentena -> {args.quarantine_table}")
    for fila in malas.groupBy("motivo").count().orderBy("motivo").collect():
        print(f"  {fila['count']:>3}  {fila['motivo']}")


if __name__ == "__main__":
    main()
