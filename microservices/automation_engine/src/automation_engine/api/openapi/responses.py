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

SCENARIO_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Scenario is not existing for this owner",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Scenario not found"
                }
            }
        }
    }
}

DEVICE_SCENARIO_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "description": "The requested device or scenario does not exist.",
        "content": {
            "application/json": {
                "examples": {
                    "Missing Device": {
                        "summary": "Missing Device",
                        "value": {"detail": "Device not found"},
                    },
                    "Missing Scenario": {
                        "summary": "Missing Scenario",
                        "value": {"detail": "Scenario not found"},
                    },
                }
            }
        },
    }
}
