import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
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

# Check if there are function calls
if response.candidates and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'function_call') and part.function_call:
            function_call_part = part.function_call
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        elif hasattr(part, 'text') and part.text:
            print(part.text)
