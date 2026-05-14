[![progress-banner](https://backend.codecrafters.io/progress/claude-code/aaf50006-f9fe-4f86-8745-ffe5ca37f1fe)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

A Python CLI coding assistant inspired by Claude Code, built for a CodeCrafters challenge. It features an agentic loop that interacts with LLMs via OpenRouter, utilizing tool calling to autonomously read/write files and execute Bash commands to fulfill user prompts.

## Features

* **Agentic Loop:** Continually processes LLM responses and executes necessary tool calls until the user's prompt is completely fulfilled.
* **Tool Calling:** Equips the LLM with three primary capabilities:
  * `Read`: Read the contents of local files.
  * `Write`: Create or edit files in the workspace.
  * `Bash`: Execute shell commands and capture their output (`stdout` & `stderr`).
* **LLM Integration:** Connects to Anthropic's Claude models via OpenRouter using the standard OpenAI Python SDK format.

## Setup & Usage

1. Ensure you have Python and `uv` installed.
2. Set your environment variables (using OpenRouter):
   ```sh
   export OPENROUTER_API_KEY="your_api_key_here"
   export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
   ```
3. Run the program with a prompt:
   ```sh
   ./your_program.sh -p "Write a hello world python script in greeting.py"
   ```
