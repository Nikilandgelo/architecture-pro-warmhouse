from fastapi import status

WRONG_TOKEN_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid device token in header was provided",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid device token."
                }
            }
        }
    }
}

UNAUTHORIZED_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Authentication credentials is missing or invalid",
        "content": {
            "application/json": {
                "example": {"detail": "Authentication credentials is invalid."}
            }
        },
    },
}

DEVICE_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Device is not existing",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Device not found"
                }
            }
        }
    }
}

DEVICE_DIFFERENT_OWNER_RESPONSE = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Requested device belongs to another owner",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Forbidden"
                }
            }
        }
    }
}
