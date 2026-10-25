-- 1002 · 03 · Gold: the numbers the operations committee reads
--
-- Gold answers business questions. It reads only silver (clean, typed data)
-- and groups it. Each table is rebuilt in full on every run.

-- 1 · One row per wind farm and day
--     Readings arrive every 10 minutes, so each power value in kW lasts 1/6 h:
--     energy in MWh = sum(power_kw) / 6 / 1000.
CREATE OR REPLACE TABLE lab1002.gold.park_daily AS
SELECT
  t.park,
  CAST(s.reading_time AS DATE)                                     AS day,
  count(DISTINCT s.turbine_id)                                     AS turbines,
  round(sum(s.power_kw) / 6 / 1000, 1)                             AS energy_mwh,
  -- Share of readings in which the turbine was available (not in maintenance)
  round(100 * avg(CASE WHEN s.status = 'MAINTENANCE' THEN 0 ELSE 1 END), 1)
                                                                   AS availability_pct,
  -- Energy produced against the maximum the turbines could have produced
  round(100 * sum(s.power_kw) / 1000 / sum(t.rated_power_mw), 1)   AS capacity_factor_pct
FROM lab1002.silver.scada AS s
JOIN lab1002.silver.turbines AS t USING (turbine_id)
GROUP BY t.park, CAST(s.reading_time AS DATE);

-- 2 · One row per maintenance stop
CREATE OR REPLACE TABLE lab1002.gold.maintenance_stops AS
SELECT
  w.work_order_id,
  t.park,
  w.turbine_id,
  w.reason,
  round((unix_timestamp(w.end_time) - unix_timestamp(w.start_time)) / 3600, 1) AS hours_stopped
FROM lab1002.silver.work_orders AS w
JOIN lab1002.silver.turbines AS t USING (turbine_id);
