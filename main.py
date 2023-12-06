import pkgutil
import inspect
import importlib
from tools.base_tool import BaseTool
from tool_manager import ToolManager
from docstring_parser import parse
from colorama import Fore, Style, init
from openai import OpenAI
import json
import sys

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <PROMPT>')
        exit()

    init(autoreset=True)
    tools_package: importlib.ModuleType = importlib.import_module('tools')
    tm = ToolManager(tools_package)

    client = OpenAI()
    messages = [
        {
            "role": "system", 
            "content": "Help user achieve ends by utilizing and improving available tools"
        },
        {
            "role": "user",
            "content": sys.argv[1]
        }
    ]

    while True:
        response = tm.get_response(messages)
        print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{response.content}")
        user_input = input(f"{Fore.YELLOW}User: {Style.RESET_ALL}")

        if user_input.lower() in ['exit', 'quit', 'q']:
            print(f"{Fore.RED}Exiting the interactive session.{Style.RESET_ALL}")
            break

        user_message = {
            "role": "user",
            "content": user_input
        }
        messages.append(user_message)


if __name__ == '__main__':
    main()
