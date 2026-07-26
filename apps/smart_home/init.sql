-- Create the database if it doesn't exist
CREATE DATABASE smarthome;

-- Connect to the database
\c smarthome;

-- Create the sensors table
CREATE TABLE IF NOT EXISTS sensors (
    id PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    value FLOAT DEFAULT 0,
    unit VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'inactive'
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_sensors_type ON sensors(type);
CREATE INDEX IF NOT EXISTS idx_sensors_location ON sensors(location);
CREATE INDEX IF NOT EXISTS idx_sensors_status ON sensors(status);

-- Add comments to the fields
COMMENT ON COLUMN sensors.created_at IS 'Timestamp of sensor creation';
COMMENT ON COLUMN sensors.last_updated IS 'Timestamp of sensor last update';
COMMENT ON COLUMN sensors.name IS 'Name of the sensor';
COMMENT ON COLUMN sensors.type IS 'Type of sensor';
COMMENT ON COLUMN sensors.location IS 'Where the sensor is located';
COMMENT ON COLUMN sensors.value IS 'Current value of the sensor';
COMMENT ON COLUMN sensors.unit IS 'Unit of measurement for the sensor value';
COMMENT ON COLUMN sensors.status IS 'Current status of the sensor';
