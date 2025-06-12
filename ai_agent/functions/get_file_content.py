import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try: 
        working_dir_path = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if  working_dir_path.startswith(file_path): 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path): 
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string)==10000: 
                file_content_string = file_content_string + f'...File "{file_path}" truncated at 10000 characters'
            return file_content_string 
    except Exception as e: 
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content truncated to 10k words.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path for the file to write to, relative to the working directory.",
            ),
            "file_content": types.Schema(
                type=types.Type.STRING,
                description="The truncated 10k words file content",
            ),
        },
    ),
)