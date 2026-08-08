
CREATE TABLE IF NOT EXISTS scenarios (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    is_enabled BOOLEAN NOT NULL DEFAULT true,
    owner_id UUID NOT NULL,
    name VARCHAR(500) NOT NULL,
    trigger_serial_number TEXT NOT NULL,
    conditions JSONB
);

CREATE INDEX ix_scenarios_created_at ON scenarios USING btree (created_at);
CREATE INDEX ix_scenarios_updated_at ON scenarios USING btree (updated_at);
CREATE INDEX ix_scenarios_owner_id ON scenarios USING btree (owner_id);
CREATE INDEX ix_scenarios_trigger_serial_number ON scenarios USING btree (trigger_serial_number);


CREATE TABLE IF NOT EXISTS scenarios_actions (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    scenario_id INT REFERENCES scenarios (id) NOT NULL,
    target_serial_number TEXT NOT NULL,
    action_command TEXT NOT NULL
);

CREATE INDEX ix_scenarios_actions_created_at ON scenarios_actions USING btree (created_at);
CREATE INDEX ix_scenarios_actions_updated_at ON scenarios_actions USING btree (updated_at);
CREATE INDEX ix_scenarios_actions_scenario_id ON scenarios_actions USING btree (scenario_id);
