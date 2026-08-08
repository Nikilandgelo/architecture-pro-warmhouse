
    const schema = {
  "info": {
    "title": "Device Management Broker",
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
    "ActivityStatusCommand": {
      "address": "ActivityStatusCommand",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "SubscribeMessage": {
          "title": "ActivityStatusCommand:SubscribeMessage",
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
              "activity_status": {
                "enum": [
                  "on",
                  "off"
                ],
                "title": "DeviceActivityStatuses",
                "type": "string",
                "x-parser-schema-id": "DeviceActivityStatuses"
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
          "x-parser-unique-object-id": "SubscribeMessage",
          "x-parser-message-name": "ActivityStatusCommand:SubscribeMessage"
        }
      },
      "bindings": {
        "nats": {
          "subject": "COMMANDS.devices.activity_status",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "ActivityStatusCommand"
    },
    "DynamicTargetValueCommand": {
      "address": "DynamicTargetValueCommand",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "SubscribeMessage": {
          "title": "DynamicTargetValueCommand:SubscribeMessage",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "properties": {
              "device_serial_number": {
                "title": "Device Serial Number",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-2>"
              },
              "new_value": {
                "title": "New Value",
                "type": "number",
                "x-parser-schema-id": "<anonymous-schema-3>"
              }
            },
            "required": [
              "device_serial_number",
              "new_value"
            ],
            "title": "DynamicTargetValuePayload",
            "type": "object",
            "x-parser-schema-id": "DynamicTargetValuePayload"
          },
          "x-parser-unique-object-id": "SubscribeMessage",
          "x-parser-message-name": "DynamicTargetValueCommand:SubscribeMessage"
        }
      },
      "bindings": {
        "nats": {
          "subject": "COMMANDS.devices.dynamic_target_value",
          "bindingVersion": "custom"
        }
      },
      "x-parser-unique-object-id": "DynamicTargetValueCommand"
    }
  },
  "operations": {
    "ActivityStatusCommand": {
      "action": "receive",
      "channel": "$ref:$.channels.ActivityStatusCommand",
      "messages": [
        "$ref:$.channels.ActivityStatusCommand.messages.SubscribeMessage"
      ],
      "x-parser-unique-object-id": "ActivityStatusCommand"
    },
    "DynamicTargetValueCommand": {
      "action": "receive",
      "channel": "$ref:$.channels.DynamicTargetValueCommand",
      "messages": [
        "$ref:$.channels.DynamicTargetValueCommand.messages.SubscribeMessage"
      ],
      "x-parser-unique-object-id": "DynamicTargetValueCommand"
    }
  },
  "components": {
    "messages": {
      "ActivityStatusCommand:SubscribeMessage": "$ref:$.channels.ActivityStatusCommand.messages.SubscribeMessage",
      "DynamicTargetValueCommand:SubscribeMessage": "$ref:$.channels.DynamicTargetValueCommand.messages.SubscribeMessage"
    },
    "schemas": {
      "DeviceActivityStatuses": "$ref:$.channels.ActivityStatusCommand.messages.SubscribeMessage.payload.properties.activity_status",
      "ActivityStatusPayload": "$ref:$.channels.ActivityStatusCommand.messages.SubscribeMessage.payload",
      "DynamicTargetValuePayload": "$ref:$.channels.DynamicTargetValueCommand.messages.SubscribeMessage.payload"
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
  