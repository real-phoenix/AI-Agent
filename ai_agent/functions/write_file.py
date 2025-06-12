import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    try: 
        working_dir_path = os.path.abspath(working_directory)

        if file_path and  not os.path.exists(file_path): 
            os.makedirs(file_path, exist_ok=True)

        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path.startswith(working_dir_path): 
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e: 
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a file, creating or overwriting it in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path for the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file.",
            ),
        },
    ),
)