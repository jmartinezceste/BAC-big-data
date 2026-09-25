"""Tarea gold: KPI de puntualidad por modelo de aeronave, pais de origen y mes.

Parametros:
  --vuelos_table       silver de vuelos
  --aeronaves_table    silver de aeronaves
  --aeropuertos_table  silver de aeropuertos
  --output_table       tabla gold de salida
"""
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, month, round as round_, when, year

spark = SparkSession.builder.getOrCreate()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vuelos_table", required=True)
    p.add_argument("--aeronaves_table", required=True)
    p.add_argument("--aeropuertos_table", required=True)
    p.add_argument("--output_table", required=True)
    args = p.parse_args()

    vuelos = spark.table(args.vuelos_table)
    aeronaves = spark.table(args.aeronaves_table)
    origenes = spark.table(args.aeropuertos_table).withColumnRenamed("aeropuerto_id", "origen_id")

    kpi = (vuelos
           .join(aeronaves, "aeronave_id")
           .join(origenes, "origen_id")
           .withColumn("anio", year("fecha"))
           .withColumn("mes", month("fecha"))
           .groupBy("modelo", "pais", "anio", "mes")
           .agg(count("vuelo_id").alias("total_vuelos"),
                count(when(col("estado") == "a_tiempo", True)).alias("vuelos_a_tiempo"))
           .withColumn("puntualidad_pct",
                       round_(col("vuelos_a_tiempo") / col("total_vuelos") * 100, 1)))

    kpi.write.format("delta").mode("overwrite").saveAsTable(args.output_table)
    print(f"Escrita {args.output_table}: {kpi.count()} filas")


if __name__ == "__main__":
    main()
