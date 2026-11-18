import os
from config import CHAR_LIMIT

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a specified file relative to the working directory as a string",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description":"Path to specified file relative to the working directory"
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path, "r") as f:
            file_content_string = f.read(CHAR_LIMIT)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'

        return file_content_string

    except Exception as e:
        return f"Error: {e}"