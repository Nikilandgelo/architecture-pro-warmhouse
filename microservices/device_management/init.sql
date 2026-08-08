
CREATE TABLE IF NOT EXISTS device_types (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    name VARCHAR(300) NOT NULL,
    manufacturer VARCHAR(300) NOT NULL,
    interaction_protocol VARCHAR(255) NOT NULL,
    measurement_unit VARCHAR(50),
    has_dynamic_values BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE (name, manufacturer, interaction_protocol)
);

CREATE INDEX ix_device_types_created_at ON device_types USING btree (created_at);
CREATE INDEX ix_device_types_updated_at ON device_types USING btree (updated_at);
CREATE INDEX ix_device_types_name ON device_types USING btree (name);
CREATE INDEX ix_device_types_interaction_protocol ON device_types USING btree (interaction_protocol);


CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    owner_id UUID NOT NULL,
    name VARCHAR(300) NOT NULL,
    serial_number TEXT NOT NULL,
    type_id INT REFERENCES device_types (id) NOT NULL,
    installation_status VARCHAR(255) NOT NULL DEFAULT 'active',
    activity_status VARCHAR(255) NOT NULL DEFAULT 'off',
    location TEXT NOT NULL,
    dynamic_target_value DOUBLE PRECISION,
    metadata JSONB
);

CREATE UNIQUE INDEX devices_serial_number_active_uidx
    ON devices (serial_number)
    WHERE installation_status = 'active';

CREATE INDEX ix_devices_created_at ON devices USING btree (created_at);
CREATE INDEX ix_devices_updated_at ON devices USING btree (updated_at);
CREATE INDEX ix_devices_owner_id ON devices USING btree (owner_id);
CREATE INDEX ix_devices_serial_number ON devices USING btree (serial_number);
CREATE INDEX ix_devices_type_id ON devices USING btree (type_id);


CREATE TABLE IF NOT EXISTS allowed_commands (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    command TEXT NOT NULL UNIQUE,
    type_id INT REFERENCES device_types (id) NOT NULL
);

CREATE INDEX ix_allowed_commands_created_at ON allowed_commands USING btree (created_at);
CREATE INDEX ix_allowed_commands_updated_at ON allowed_commands USING btree (updated_at);
CREATE INDEX ix_allowed_commands_type_id ON allowed_commands USING btree (type_id);



COMMENT ON COLUMN device_types.name IS 'Unique human-readable name of the device type.';
COMMENT ON COLUMN device_types.interaction_protocol IS 'Protocol used to interact with devices of this type, for example MQTT, HTTP, etc.';
COMMENT ON COLUMN device_types.measurement_unit IS 'Default measurement unit used by devices of this type.';
COMMENT ON COLUMN device_types.has_dynamic_values IS 'Indicates whether devices of this type support dynamic target values.';

COMMENT ON COLUMN devices.owner_id IS 'UUID identifier of the user that owns the device.';
COMMENT ON COLUMN devices.name IS 'Human-readable name of the device.';
COMMENT ON COLUMN devices.serial_number IS 'Unique serial number assigned to the physical device.';
COMMENT ON COLUMN devices.type_id IS 'Reference to the device type in the device_types table.';
COMMENT ON COLUMN devices.installation_status IS 'Current installation status of the device, for example active, inactive, etc.';
COMMENT ON COLUMN devices.activity_status IS 'Current operational activity status of the device, for example on, off, etc.';
COMMENT ON COLUMN devices.location IS 'Current location of the device.';
COMMENT ON COLUMN devices.dynamic_target_value IS 'Optional dynamic target value used by devices that support configurable target values.';

COMMENT ON COLUMN allowed_commands.is_deleted IS 'Soft-delete flag indicating whether the command is considered deleted.';
COMMENT ON COLUMN allowed_commands.command IS 'Unique command that is allowed and can be proceed for a specific device type.';
COMMENT ON COLUMN allowed_commands.type_id IS 'Reference to the device type for which this command is allowed.';


INSERT INTO device_types (name, manufacturer, interaction_protocol, measurement_unit, has_dynamic_values)
VALUES
    ('Thermostat', 'Bosch', 'MQTT', '°C', true),
    ('Thermostat', 'Tuya', 'HTTP', '°F', true),
    ('Bulb', 'Philips Hue', 'MQTT', '%', true),
    ('Automatic Gate', 'Came', 'HTTP', NULL, false),
    ('Video Camera', 'Hikvision', 'RTSP', NULL, false)
;
