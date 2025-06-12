import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions
from functions.run_python import run_python_file 
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info


def main(): 
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY") 
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error: No prompt provided.")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    prompt_input = sys.argv[1]
    if verbose:
        print(f"User prompt: {prompt_input}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt_input)]),
    ]

    for i in range(0,20): 
        curr_op = generate_content(client, messages, verbose)
        tool_call = False
        for cand in curr_op.candidates: 
            messages.append(cand.content)
            for part in cand.content.parts: 
                if "function_call" in part: 
                    function_call = part['function_call']
                    function_call_res = call_function(function_call)

                    messages.append(
                        {
                            "role": "tool", 
                            "parts" : [{
                                "function_response": {
                                    "name": function_call["name"],
                                    "response": function_call_res
                                }
                            }]
                        }
                    )
                    tool_call = True
                    break
        if not tool_call: 
            for candidate in curr_op.candidates:
                for part in candidate.content.parts:
                    if 'text' in part:
                        print(part['text'])
            break

def generate_content(client, messages, verbose): 
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents =  messages, 
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Model decided to call function: {function_call.name}")
        function_call_result = call_function(function_call, verbose)
        try:
            response_data = function_call_result.parts[0].function_response.response
        except (AttributeError, IndexError):
            raise Exception("Fatal: function_call_result does not contain a function_response.")

        if verbose:
            print(f"-> {response_data}")


def call_function(function_call_part, verbose=False):
    if verbose: 
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")

    dict_functions = {
        "get_files_info" : get_files_info, 
        "get_file_content" : get_file_content, 
        "write_file" : write_file, 
        "run_python_file" : run_python_file
    }

    args_for_call = function_call_part.args.copy()
    args_for_call["working_directory"] = "./calculator"

    if function_call_part.name == "run_python_file":
        if "directory" in args_for_call:
            args_for_call["file_name"] = args_for_call.pop("directory")

    if function_call_part.name not in dict_functions: 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name ,
                    response={"error": f"Unknown function: {function_call_part.name }"},
                )
            ],
        )
    function_to_call = dict_functions[function_call_part.name]
    
    func_val = function_to_call(**args_for_call) # for calling dict
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": func_val},
            )
        ],
    )



if __name__ == "__main__":
    main()