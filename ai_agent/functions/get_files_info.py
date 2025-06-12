import os
from google.genai import types
WORKING_DIR = "./calculator"

def get_files_info(working_directory, directory=None):
    try: 
        trgt_dir = directory if directory is not None else working_directory
        working_dir_path = os.path.abspath(working_directory)
        trgt_dir_path = os.path.abspath(os.path.join(working_directory, trgt_dir))

        if not trgt_dir_path.startswith(working_dir_path): 
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(trgt_dir_path):
            return f'Error: "{directory}" is not a directory'
        
        dir_list = []
        for item in os.listdir(trgt_dir_path): 
            item_path = os.path.join(trgt_dir_path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            dir_list.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(dir_list)
    
    except Exception as e: 
        return f"Error: {str(e)}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)