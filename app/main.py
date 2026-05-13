import argparse
import os
import sys
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

def read_file(file_path: str) -> str:
    with open(file=file_path) as f:
        return f.read()

def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "Read",
                "description": "Read and return the contents of the file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "Write",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "The path to the file to write"},
                        "content": {"type": "string", "description": "The content to write"}
                    },
                    "required": ["file_path", "content"]
                }
            }
        }
    ]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=[{"role": "user", "content": args.p}],
        tools=get_tools()
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # Extract the tool_calls
    if chat.choices[0].finish_reason == "tool_calls":
        for tool_call in chat.choices[0].message.tool_calls:
            if tool_call.function.name == "Read":
                file_path = json.loads(tool_call.function.arguments)["file_path"]
                print(read_file(file_path))
    else:
        if chat.choices[0].message.content:
            print(chat.choices[0].message.content)
        
    # Debug
    #print("Logs from your program will appear here!", file=sys.stderr)


if __name__ == "__main__":
    main()
