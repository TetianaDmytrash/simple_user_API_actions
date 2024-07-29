schema_user = {
    "type": "object",
    "properties": {
        'completed': {'type': 'boolean'},
        'created': {'type': 'string'},
        'email': {'type': 'string'},
        'firstName': {'type': 'string'},
        'uid': {'format': 'uuid', 'type': 'string'},
        'lastName': {'type': 'string'},
        'password': {'type': 'string'},
        'summary': {'type': 'string'},
        'username': {'type': 'string'}
    },
    "required": ["firstName", "lastName", "email", "completed", "username", "password", "summary"]
}
