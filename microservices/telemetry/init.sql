
CREATE TABLE IF NOT EXISTS telemetry_database.telemetry_record (
    device_serial_number String COMMENT 'Unique serial number of the device that produced the telemetry record.',
    timestamp DateTime64 COMMENT 'Time when the telemetry record was produced or received.',
    device_location String COMMENT 'Location of the device at the time of telemetry collection.',
    metrics Map(String, Float64) COMMENT 'Numeric telemetry metrics, where the key is the metric name and the value is the metric value.',
    states Map(String, String) COMMENT 'Textual telemetry states, where the key is the state name and the value is the state value.'
) ENGINE = MergeTree
ORDER BY (device_serial_number, timestamp);
