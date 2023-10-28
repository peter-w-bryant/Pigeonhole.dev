# api_docs.py

create_project_doc = {
    "tags": ["Projects"],
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "description": "The JWT of the current user. The required header format is: **{'Authorization: Bearer {JWT}'}**",
            "type": "string",
            "example": "Bearer <JWT_token>",
        },
        {
            "name": "JSON object",
            "in": "body",
            "required": True,
            "description": "A JSON object containing the GitHub URL of the project.",
            "schema": {
                "type": "object",
                "properties": {
                    "gh_url": {
                        "type": "string",
                        "description": "The full GitHub URL of the project.",
                        "example": "https://github.com/pallets/flask",
                    },
                },
            },
        },
    ],
    "responses": {
        200: {"description": "Project added to the database successfully, returns a success message"},
        400: {"description": "Invalid GitHub URL, returns an error message"},
        409: {"description": "Project already exists in the database, returns an error message"},
        500: {"description": "Error adding the project to the database, returns an error message"},
    },
}
