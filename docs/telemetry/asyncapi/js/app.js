
    const schema = {
  "info": {
    "title": "Telemetry Broker",
    "version": "1.0",
    "contact": {
      "name": "Nikita Selivanov",
      "email": "niki_landgelo@outlook.com"
    }
  },
  "asyncapi": "3.0.0",
  "defaultContentType": "application/json",
  "servers": {
    "development": {
      "host": "smarthouse_nats:4222",
      "pathname": "",
      "protocol": "nats",
      "protocolVersion": "custom"
    }
  },
  "channels": {
    "Telemetry Publisher": {
      "address": "Telemetry Publisher",
      "description": "Publish event about new telemetry data",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "Message": {
          "title": "Telemetry Publisher:Message",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "properties": {
              "device_serial_number": {
                "title": "Device Serial Number",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-1>"
              },
              "device_location": {
                "title": "Device Location",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-2>"
              },
              "metrics": {
                "additionalProperties": {
                  "type": "number",
                  "x-parser-schema-id": "<anonymous-schema-4>"
                },
                "title": "Metrics",
                "type": "object",
                "x-parser-schema-id": "<anonymous-schema-3>"
              },
              "states": {
                "additionalProperties": {
                  "type": "string",
                  "x-parser-schema-id": "<anonymous-schema-6>"
                },
                "title": "States",
                "type": "object",
                "x-parser-schema-id": "<anonymous-schema-5>"
              }
            },
            "required": [
              "device_serial_number",
              "device_location"
            ],
            "title": "TelemetryPayload",
            "type": "object",
            "x-parser-schema-id": "TelemetryPayload"
          },
          "x-parser-unique-object-id": "Message",
          "x-parser-message-name": "Telemetry Publisher:Message"
        }
      },
      "bindings": {
        "nats": {
          "subject": "EVENTS.telemetry",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "Telemetry Publisher"
    }
  },
  "operations": {
    "Telemetry Publisher": {
      "action": "send",
      "channel": "$ref:$.channels.Telemetry Publisher",
      "messages": [
        "$ref:$.channels.Telemetry Publisher.messages.Message"
      ],
      "x-parser-unique-object-id": "Telemetry Publisher"
    }
  },
  "components": {
    "messages": {
      "Telemetry Publisher:Message": "$ref:$.channels.Telemetry Publisher.messages.Message"
    },
    "schemas": {
      "TelemetryPayload": "$ref:$.channels.Telemetry Publisher.messages.Message.payload"
    }
  },
  "x-parser-spec-parsed": true,
  "x-parser-api-version": 3,
  "x-parser-spec-stringified": true
};
    const config = {"show":{"sidebar":true},"sidebar":{"showOperations":"byDefault"}};
    const appRoot = document.getElementById('root');
    AsyncApiStandalone.render(
        { schema, config, }, appRoot
    );
  