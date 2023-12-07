from tools.base_tool import BaseTool
import subprocess
import json

class ShellTool(BaseTool):
    def execute(self, input: str) -> str:
        """
        Execute a list of Linux commands in the shell and returns their concatenated output.

        Args:
            input (str): JSON representation of the list of commands to execute and optional arguments to pass.

                Example:
                [
                    {
                        "command": "ls",
                        "args": ["-ltrah"]
                    },
                    {
                        "command": "echo",
                        "args": ["foo", ">", "foo.txt"]
                    }
                ]
        """
        try:
            # Ensure 'commands' is a list of dictionaries
            commands = json.loads(input) if isinstance(input, str) else input
            if not isinstance(commands, list):
                commands = [commands]
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON input: {input}")
        result_str = ''
        
        for command_json in commands:
            command = command_json['command']
            args = command_json.get('args', [])
            redirect_out = None
            
            if '>' in args:  # detect redirection
                redirect_index = args.index('>')
                redirect_out = args[redirect_index + 1]  # get the output file 
                args = args[:redirect_index]  # remove '> and filename' from args
            
            try:
                # Run the command and handle output redirection
                if redirect_out:
                    with open(redirect_out, 'w') as fp:
                        subprocess.run([command] + args, stdout=fp, stderr=subprocess.PIPE, check=False)
                    msg = f'REDIRECTED_TO_FILE: {redirect_out}\n' 
                else:
                    # Execute command and capture stdout and stderr
                    completed_process = subprocess.run([command] + args, text=True, capture_output=True, check=False)
                    msg = completed_process.stdout
                
                result_str += msg + '\n'

            except subprocess.CalledProcessError as e:
                # Capture stderr from the exception if the command fails
                self.manager.logger.warning(f"CalledProcessError: {e}")
                result_str += e.stderr + e.stdout + '\n'
            except Exception as e:
                result_str += f"An unexpected error occurred: {e}\n"

        return result_str.strip()
