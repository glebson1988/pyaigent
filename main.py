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
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
config = types.GenerateContentConfig(system_instruction=system_prompt)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(model=model, contents=messages, config=config)
metadata = response.usage_metadata

if verbose:
    print(f"User prompt: {user_prompt}")
    metadata = response.usage_metadata
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")

print(response.text)
