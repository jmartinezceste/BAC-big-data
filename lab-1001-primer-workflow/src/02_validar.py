"""Tarea de validacion: lee una tabla bronze, revisa su calidad y la pasa a silver.

En este laboratorio la validacion INFORMA: cuenta nulos, duplicados, valores
fuera de rango y fechas mal formadas, y lo deja en el log de la tarea. Todas las
filas pasan a silver. En el laboratorio 1002 la validacion pasa a SEPARAR las
filas malas en una tabla de cuarentena.

Las reglas de cada tabla viven en config.json, no en el codigo: el mismo script
valida cualquier tabla.

Parametros:
  --input_table   tabla bronze de entrada
  --output_table  tabla silver de salida
  --config_path   ruta del config.json en el volumen
  --table_name    clave de la tabla dentro de config.json
"""
import argparse
import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as max_, min as min_, to_date

spark = SparkSession.builder.getOrCreate()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input_table", required=True)
    p.add_argument("--output_table", required=True)
    p.add_argument("--config_path", required=True)
    p.add_argument("--table_name", required=True)
    args = p.parse_args()

    with open(args.config_path, encoding="utf-8") as f:
        reglas = json.load(f)[args.table_name]

    # Solo las columnas del modelo: fuera la columna tecnica ingest_time
    df = spark.table(args.input_table).select(*reglas["columnas_completas"])
    print(f"Validando {args.input_table}: {df.count()} filas")

    for pk in reglas.get("claves_primarias", []):
        print(f"  Nulos en la clave '{pk}': {df.filter(col(pk).isNull()).count()}")

    if reglas.get("claves_primarias"):
        dup = (df.groupBy(*reglas["claves_primarias"]).count()
                 .filter("count > 1").count())
        print(f"  Claves duplicadas: {dup}")

    for c, (lo, hi) in reglas.get("columnas_numericas", {}).items():
        real_lo, real_hi = df.select(min_(c), max_(c)).first()
        fuera = df.filter((col(c) < lo) | (col(c) > hi)).count()
        print(f"  '{c}': de {real_lo} a {real_hi} (esperado {lo}-{hi}), fuera de rango: {fuera}")

    fecha = reglas.get("columna_fecha")
    if fecha:
        malas = df.filter(to_date(col(fecha)).isNull()).count()
        print(f"  Fechas mal formadas en '{fecha}': {malas}")

    df.write.format("delta").mode("overwrite").saveAsTable(args.output_table)
    print(f"Escrita {args.output_table}")


if __name__ == "__main__":
    main()
