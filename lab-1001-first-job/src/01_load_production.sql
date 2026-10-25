-- 1001 · Load the production reports into bronze
--
-- Reads every report in the volume. COPY INTO remembers which files it has
-- already loaded: each run only adds the new ones, and running it twice by
-- mistake adds nothing.

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

COPY INTO lab1001.bronze.production
FROM (
  SELECT
    CAST(date AS DATE)                AS date,
    park_id,
    park,
    turbine_id,
    model,
    CAST(rated_power_mw AS DOUBLE)    AS rated_power_mw,
    CAST(avg_wind_speed_ms AS DOUBLE) AS avg_wind_speed_ms,
    CAST(operating_hours AS DOUBLE)   AS operating_hours,
    CAST(energy_mwh AS DOUBLE)        AS energy_mwh,
    _metadata.file_name               AS source_file,
    current_timestamp()               AS loaded_at
  FROM '/Volumes/lab1001/landing/data/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
