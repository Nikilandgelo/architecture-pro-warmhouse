from fastapi import status


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

DB_ERROR_RESPONSE = {
    status.HTTP_409_CONFLICT: {
        "description": "Database returned an error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Something went wrong"
                }
            }
        }
    }
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
