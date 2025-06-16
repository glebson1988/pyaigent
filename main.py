import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

def call_function(function_call_part, verbose=False):
    available_functions_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in available_functions_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args["working_directory"] = "./calculator"

    try:
        function_result = available_functions_map[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )

verbose = "--verbose" in sys.argv

# Remove --verbose from the arguments to get the actual prompt
args = [arg for arg in sys.argv[1:] if arg != "--verbose"]

if not args:
    print("Error: Please provide a prompt as a command-line argument.")
    print("Usage: python3 main.py \"Your prompt here\" [--verbose]")
    sys.exit(1)

user_prompt = " ".join(args)
model = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Use '.' for the root/current directory.",
            ),
        },
        required=["directory"]
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(model=model, contents=messages, config=config)
metadata = response.usage_metadata

if verbose:
    print(f"User prompt: {user_prompt}")
    metadata = response.usage_metadata
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")

if response.candidates and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'function_call') and part.function_call:
            function_call_part = part.function_call
            function_call_result = call_function(function_call_part, verbose)

            if not (function_call_result.parts and
                    hasattr(function_call_result.parts[0], 'function_response') and
                    function_call_result.parts[0].function_response):
                raise Exception("Invalid function response format")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        elif hasattr(part, 'text') and part.text:
            print(part.text)
