-- 1001 · Load one day's production report into bronze
--
-- Job parameter: file (for example production_2026-10-19.csv).
-- Safe to re-run with the same file: REPLACE WHERE swaps the rows of that file
-- instead of appending them again.

CREATE TABLE IF NOT EXISTS lab1001.bronze.production (
  date              DATE,
  park_id           STRING,
  park              STRING,
  turbine_id        STRING,
  model             STRING,
  rated_power_mw    DOUBLE,
  avg_wind_speed_ms DOUBLE,
  operating_hours   DOUBLE,
  energy_mwh        DOUBLE,
  source_file       STRING,
  loaded_at         TIMESTAMP
);

INSERT INTO lab1001.bronze.production
REPLACE WHERE source_file = :file
SELECT
  date,
  park_id,
  park,
  turbine_id,
  model,
  rated_power_mw,
  avg_wind_speed_ms,
  operating_hours,
  energy_mwh,
  :file               AS source_file,
  current_timestamp() AS loaded_at
FROM read_files(
  '/Volumes/lab1001/landing/data/' || :file,
  format => 'csv',
  header => true,
  schema => 'date DATE, park_id STRING, park STRING, turbine_id STRING, model STRING, rated_power_mw DOUBLE, avg_wind_speed_ms DOUBLE, operating_hours DOUBLE, energy_mwh DOUBLE'
);
