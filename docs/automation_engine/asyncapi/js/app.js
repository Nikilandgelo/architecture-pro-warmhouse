
    const schema = {
  "info": {
    "title": "Automation Engine Broker",
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
    "Telemetry Events Handler": {
      "address": "Telemetry Events Handler",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "SubscribeMessage": {
          "title": "Telemetry Events Handler:SubscribeMessage",
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
          "x-parser-unique-object-id": "SubscribeMessage",
          "x-parser-message-name": "Telemetry Events Handler:SubscribeMessage"
        }
      },
      "bindings": {
        "nats": {
          "subject": "EVENTS.telemetry",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "Telemetry Events Handler"
    },
    "Activity Status Publisher": {
      "address": "Activity Status Publisher",
      "description": "Publish command about the new status",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "Message": {
          "title": "Activity Status Publisher:Message",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "properties": {
              "device_serial_number": {
                "title": "Device Serial Number",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-7>"
              },
              "activity_status": {
                "title": "Activity Status",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-8>"
              }
            },
            "required": [
              "device_serial_number",
              "activity_status"
            ],
            "title": "ActivityStatusPayload",
            "type": "object",
            "x-parser-schema-id": "ActivityStatusPayload"
          },
          "x-parser-unique-object-id": "Message",
          "x-parser-message-name": "Activity Status Publisher:Message"
        }
      },
      "bindings": {
        "nats": {
          "subject": "COMMANDS.devices.activity_status",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "Activity Status Publisher"
    },
    "Dynamic Value Publisher": {
      "address": "Dynamic Value Publisher",
      "description": "Publish command about the new value",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "Message": {
          "title": "Dynamic Value Publisher:Message",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "properties": {
              "device_serial_number": {
                "title": "Device Serial Number",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-9>"
              },
              "new_value": {
                "title": "New Value",
                "type": "number",
                "x-parser-schema-id": "<anonymous-schema-10>"
              }
            },
            "required": [
              "device_serial_number",
              "new_value"
            ],
            "title": "DynamicValuePayload",
            "type": "object",
            "x-parser-schema-id": "DynamicValuePayload"
          },
          "x-parser-unique-object-id": "Message",
          "x-parser-message-name": "Dynamic Value Publisher:Message"
        }
      },
      "bindings": {
        "nats": {
          "subject": "COMMANDS.devices.dynamic_target_value",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "Dynamic Value Publisher"
    }
  },
  "operations": {
    "Telemetry Events Handler": {
      "action": "receive",
      "channel": "$ref:$.channels.Telemetry Events Handler",
      "messages": [
        "$ref:$.channels.Telemetry Events Handler.messages.SubscribeMessage"
      ],
      "x-parser-unique-object-id": "Telemetry Events Handler"
    },
    "Activity Status Publisher": {
      "action": "send",
      "channel": "$ref:$.channels.Activity Status Publisher",
      "messages": [
        "$ref:$.channels.Activity Status Publisher.messages.Message"
      ],
      "x-parser-unique-object-id": "Activity Status Publisher"
    },
    "Dynamic Value Publisher": {
      "action": "send",
      "channel": "$ref:$.channels.Dynamic Value Publisher",
      "messages": [
        "$ref:$.channels.Dynamic Value Publisher.messages.Message"
      ],
      "x-parser-unique-object-id": "Dynamic Value Publisher"
    }
  },
  "components": {
    "messages": {
      "Telemetry Events Handler:SubscribeMessage": "$ref:$.channels.Telemetry Events Handler.messages.SubscribeMessage",
      "Activity Status Publisher:Message": "$ref:$.channels.Activity Status Publisher.messages.Message",
      "Dynamic Value Publisher:Message": "$ref:$.channels.Dynamic Value Publisher.messages.Message"
    },
    "schemas": {
      "TelemetryPayload": "$ref:$.channels.Telemetry Events Handler.messages.SubscribeMessage.payload",
      "ActivityStatusPayload": "$ref:$.channels.Activity Status Publisher.messages.Message.payload",
      "DynamicValuePayload": "$ref:$.channels.Dynamic Value Publisher.messages.Message.payload"
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
  