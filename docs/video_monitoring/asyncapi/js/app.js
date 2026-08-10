
    const schema = {
  "asyncapi": "3.1.0",
  "info": {
    "title": "Video Monitoring WebSocket",
    "version": "1.0",
    "contact": {
      "name": "Nikita Selivanov",
      "email": "niki_landgelo@outlook.com"
    }
  },
  "servers": {
    "development": {
      "host": "video_monitoring:9996",
      "protocol": "ws",
      "pathname": "/api/v1/video/connect"
    }
  },
  "channels": {
    "VideoStream": {
      "address": "/api/v1/video/connect",
      "servers": [
        "$ref:$.servers.development"
      ],
      "messages": {
        "VideoFrame": {
          "title": "VideoFrame",
          "description": "Binary video frame pushed to the client after connection is accepted.",
          "payload": {
            "type": "string",
            "format": "binary",
            "description": "Raw binary frame data (opaque bytes), not JSON or UTF-8 text.",
            "x-parser-schema-id": "<anonymous-schema-1>"
          },
          "x-parser-unique-object-id": "VideoFrame",
          "x-parser-message-name": "VideoFrame"
        }
      },
      "bindings": {
        "ws": {
          "method": "GET",
          "query": {
            "type": "object",
            "properties": {
              "device_serial_number": {
                "type": "string",
                "description": "Serial number of the target device."
              },
              "stream_url": {
                "type": "string",
                "description": "Camera stream source URL."
              }
            },
            "required": [
              "device_serial_number",
              "stream_url"
            ]
          },
          "headers": {
            "type": "object",
            "properties": {
              "Authorization": {
                "type": "string",
                "description": "Bearer JWT token, e.g. 'Bearer <token>'."
              }
            },
            "required": [
              "Authorization"
            ]
          },
          "bindingVersion": "0.1.0"
        }
      },
      "x-parser-unique-object-id": "VideoStream"
    }
  },
  "operations": {
    "VideoStreamSend": {
      "action": "send",
      "channel": "$ref:$.channels.VideoStream",
      "messages": [
        "$ref:$.channels.VideoStream.messages.VideoFrame"
      ],
      "x-parser-unique-object-id": "VideoStreamSend"
    }
  },
  "components": {
    "messages": {
      "VideoFrame": "$ref:$.channels.VideoStream.messages.VideoFrame"
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
  