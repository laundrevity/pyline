from tools.base_tool import BaseTool
import json
import os


class FileTool(BaseTool):
    @staticmethod
    def perform_operation(path, content=None, line_number=None, action=None):
        with open(path, 'r') as file:
            lines = file.readlines()

        if action == 'create':
            lines = [content + '\n']

        # Note: Line-numbers are not zero-indexed, but list elements are, hence the -1
        elif action == 'insert' and line_number is not None:
            if line_number < 1: 
                line_number = 1
            elif line_number > len(lines):
                line_number = len(lines)
            lines.insert(line_number - 1, content + '\n')

        elif action == 'update' and line_number is not None:
            if line_number < 1 or line_number > len(lines):
                raise IndexError("Line number out of range")
            lines[line_number - 1] = content + '\n'

        elif action == 'delete' and line_number is not None:
            if line_number < 1 or line_number > len(lines):
                raise IndexError("Line number out of range")
            lines.pop(line_number - 1)

        with open(path, 'w') as file:
            file.writelines(lines)

    def execute(self, input: str) -> str:
        """
        Execute the sequence of file operations represented by the given JSON string.

        Args:
            input (str): JSON string representing the sequence of file operations to make.

                Example:
                [
                    {
                        "action": "create",
                        "path": "new_file.txt",
                        "content": "Initial content of the file."
                    },
                    {
                        "action": "insert",
                        "path": "existing_file.txt",
                        "line_number": 2,
                        "content": "Inserted line at index 2."
                    },
                    {
                        "action": "update",
                        "path": "existing_file.txt",
                        "line_number": 0,
                        "content": "Updated content at line 0."
                    },
                    {
                        "action": "delete",
                        "path": "existing_file.txt",
                        "line_number": 4
                    },
                    {
                        "action": "remove",
                        "path": "old_file.txt"
                    }
                ]
        """
        try:
            operations = json.loads(input) if isinstance(input, str) else input
            if not isinstance(operations, list):
                operations = [operations]
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON input: {input}")
        
        for op in operations:
            action = op['action']
            path = op['path']
            content = op.get('content')
            line_number = op.get('line_number')

            if action in ['insert', 'update', 'delete'] and line_number is None:
                raise ValueError(f"Line number is required for {action}")
            
            if action == 'remove':
                os.remove(path)
            else:
                if action == 'create' or not os.path.exists(path):
                    with open(path, 'w'): pass # Create empty file if none exists
                
                self.perform_operation(path, content, line_number, action)
            
        
        return "File operations executed successfully."
