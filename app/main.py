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
    
def write_file(args_dict: dict) -> str:
    with open(args_dict["file_path"], "w") as f:
        f.write(args_dict["content"])
    return "File written successfully."

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

    messages = [{"role": "user", "content": args.p}]

    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=get_tools()
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        # Record the assistant's response
        response_message = chat.choices[0].message
        messages.append(response_message)

        # Repeat until complete
        if not response_message.tool_calls:
            if response_message.content:
                print(response_message.content)
            break

        # Execute tool calls
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "Read":
                file_path = json.loads(tool_call.function.arguments)["file_path"]
                result = read_file(file_path)
            elif tool_call.function.name == "Write":
                args_dict = json.loads(tool_call.function.arguments)
                result = write_file(args_dict)
            else:
                result = "Unknown tool"

            # Add each tool call result to your messages array required for the next iteration
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    # Debug
    #print("Logs from your program will appear here!", file=sys.stderr)


if __name__ == "__main__":
    main()
