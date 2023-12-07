from utils.tool_manager import ToolManager
from colorama import Fore, Style, init
from pathlib import Path
import datetime
import argparse
import logging

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ToolManager Command Line Interface")
    parser.add_argument("prompt", type=str, help="The initial prompt for the assistant")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the log level")
    parser.add_argument("--log-file", default=f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log", help="Set the log file name")
    parser.add_argument("--state", action="store_true", default=False, help="Whether to include state.txt in initial system.txt prompt")
    args = parser.parse_args()

    # Set up logging
    log_level = getattr(logging, args.log_level.upper(), None)
    log_filename = Path("/app/logs/" + args.log_file)
    logging.basicConfig(
        level=log_level,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler() # To output to console as well
        ],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'
    )
    logging.info(f"Starting the ToolManager CLI...")

    init(autoreset=True)
    tm = ToolManager()

    prompt = args.prompt
    if prompt.lower() == 'debug':
        for tool_name, tool in tm.tools.items():
            print(f"{tool_name}: {tool}")
        exit()

    base_system_prompt = "Help user achieve ends by utilizing and improving available tools"
    if args.state:
        system_prompt = base_system_prompt + f"\n\nCurrent source code:\n\n{open('state.txt').read()}"
    else:
        system_prompt = base_system_prompt

    messages = [
        {
            "role": "system", 
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
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
