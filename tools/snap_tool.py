from tools.base_tool import BaseTool
import json
import os


class SnapTool(BaseTool):
    @staticmethod
    def add_line_numbers(code):
        lines = code.split('\n')
        numbered_lines = [f"{idx + 1: >4}: {line}" for idx, line in enumerate(lines)]
        return '\n'.join(numbered_lines)

    def execute(self, input: str) -> str:
        """
        Return the formatted source code of the current project. If 'infra' field is True,
        include Dockerfile, docker-compose.yml, and requirements.txt, but exclude __pycache__ directories.

        Args:
            input (str): JSON string with an 'infra' field to indicate infrastructure inclusion, and optional 'line_numbers' field to include line numbers in source code output (defaults to True).
        """
        # Parse the JSON input
        params = json.loads(input)
        include_infra = params.get('infra', False)
        line_numbers = params.get('line_numbers', True)

        # Initialize the formatted source code string
        formatted_code = ''

        # List of project-related file extensions
        py_files = ['.py']
        infra_files = ['Dockerfile', 'docker-compose.yml', 'requirements.txt']
        all_files = py_files + infra_files if include_infra else py_files

        # Traverse the project directory
        for root, dirs, files in os.walk('.'):
            # Skipping __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__' and d != 'venv']
            
            for file in files:
                if any(file.endswith(ext) for ext in all_files):
                    file_path = os.path.join(root, file)
                    # Add file path header
                    formatted_code += f'--- BEGIN {file_path} ---\n'

                    # Read the content of the file
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if line_numbers:
                            content = self.add_line_numbers(content)
                        formatted_code += content

                    # Add file path footer
                    formatted_code += f'\n--- END {file_path} ---\n\n'
        
        # Write to state.txt
        with open('state.txt', 'w') as f:
            f.write(formatted_code)

        return formatted_code
