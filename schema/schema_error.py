"""
schema for compare error responses
"""
schema_error_with_message = {
    "type": "object",
    "properties": {
        "errorCode": {"type": "integer"},
        "errorMessage": {"type": "string"},
        "path": {"type": "string"},
        "httpStatus": {"type": "string"}
    },
    "required": ["errorCode", "errorMessage", "path", "httpStatus"]
}

schema_error_without_message = {
    "type": "object",
    "properties": {
        "code": {"type": "integer"},
        "status": {"type": "string"}
    },
    "required": ["code", "status"]
}