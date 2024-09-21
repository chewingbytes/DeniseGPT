tools = [
    {
        "type": "function",
        "function": {
            "name": "get_code_content",
            "description": "Get the entire code content of a specific file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "the name of the file you want the code contents from",
                    },
                },
                "required": ["file_name"],
            },
        },
    },
]
