"""Tarea de ingesta: un CSV del volumen pasa a una tabla Delta de la capa bronze.

Es el mismo script para todos los ficheros: lo que cambia entre tareas son los
parametros. Por eso un workflow puede tener cuatro ingestas con un solo codigo.

Parametros:
  --input_file    ruta del CSV en el volumen (/Volumes/...)
  --output_table  tabla destino, con catalogo y schema (catalogo.bronze.tabla)
  --write_mode    overwrite (por defecto) o append
  --partition_by  columnas de particion separadas por coma; vacio = sin particion
"""
import argparse
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# En serverless la sesion ya existe; en un cluster clasico la crea. En los dos
# casos, getOrCreate devuelve la misma.
spark = SparkSession.builder.getOrCreate()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ingesta")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input_file", required=True)
    p.add_argument("--output_table", required=True)
    p.add_argument("--write_mode", default="overwrite", choices=["overwrite", "append"])
    p.add_argument("--partition_by", default="")
    args = p.parse_args()

    df = (spark.read
          .option("header", True)
          .option("inferSchema", True)
          .csv(args.input_file)
          .withColumn("ingest_time", current_timestamp()))

    filas = df.count()
    log.info("Filas leidas de %s: %s", args.input_file, filas)
    if filas == 0:
        raise ValueError(f"El fichero {args.input_file} no tiene filas.")

    escritor = df.write.format("delta").mode(args.write_mode)
    columnas = [c.strip() for c in args.partition_by.split(",") if c.strip()]
    if columnas:
        escritor = escritor.partitionBy(*columnas)
    escritor.saveAsTable(args.output_table)

    log.info("Ingesta completada en %s", args.output_table)


if __name__ == "__main__":
    main()
