"""Tarea gold: coste medio de mantenimiento por aeronave, modelo y mes.

Parametros:
  --mantenimiento_table  silver de mantenimientos
  --aeronaves_table      silver de aeronaves
  --output_table         tabla gold de salida
"""
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, month, round as round_, year

spark = SparkSession.builder.getOrCreate()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mantenimiento_table", required=True)
    p.add_argument("--aeronaves_table", required=True)
    p.add_argument("--output_table", required=True)
    args = p.parse_args()

    mantenimientos = spark.table(args.mantenimiento_table)
    aeronaves = spark.table(args.aeronaves_table)

    kpi = (mantenimientos
           .join(aeronaves, "aeronave_id")
           .withColumn("anio", year("fecha"))
           .withColumn("mes", month("fecha"))
           .groupBy("aeronave_id", "modelo", "anio", "mes")
           .agg(count("mantenimiento_id").alias("total_mantenimientos"),
                round_(avg("costo_usd"), 2).alias("coste_medio_usd"),
                round_(avg("duracion_hr"), 1).alias("duracion_media_hr")))

    kpi.write.format("delta").mode("overwrite").saveAsTable(args.output_table)
    print(f"Escrita {args.output_table}: {kpi.count()} filas")


if __name__ == "__main__":
    main()
