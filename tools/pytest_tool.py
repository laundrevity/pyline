from tools.base_tool import BaseTool
import json


class PytestTool(BaseTool):
    dependencies = ['ShellTool']

    def execute(self, input: str) -> str:
        """
        Run tests using PyTest and return a string indicating the test results.
        
        Args:
            input (str): JSON string with selected_tests field to specify which tests to run.
                         
        Example input:
        {
            "selected_tests": ["test_pipeline_tool.py"]
        }
        """
        # Parse the input JSON to get the selected tests
        if input:
            params = json.loads(input)
        else:
            params = {}
        
        # Construct the PyTest command arguments
        pytest_args = []
        selected_tests = params.get("selected_tests", [])
        if selected_tests:
            pytest_args.append('-k')
            pytest_args.extend(selected_tests)
        
        # Run PyTest using the ShellTool and return its output
        # Convert PyTest args into the JSON format expected by ShellTool
        command_args = [{"command": "pytest", "args": pytest_args}]
        json_args = json.dumps(command_args)
        
        return self.manager.execute_tool("ShellTool", input=json_args)