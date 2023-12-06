from tools.base_tool import BaseTool
import json
import re


class PipelineTool(BaseTool):
    def execute(self, input: str) -> str:
        """
        Execute the given sequence of tool calls using a JSON string representing tool calls and arguments.

        Args:
            input (str): JSON string representing the sequence of tool calls to make. Note that we can use $ together with identifiers to pass along output from one tool to another later tool. Do NOT include 'functions.' in the tool name -- simply use GptTool, ShellTool, etc. Notice that each object in the JSON list here has a "parameters" key -- NOT an "args" key.

                Example:
                [
                    {
                        "id": "generateText",
                        "tool": "GptTool",
                        "parameters": {
                            "input": [{"role": "user", "content": "create Python code for hello world, and ONLY return that Python code"}]
                        }
                    },
                    {
                        "id": "executeGeneratedCode",
                        "tool": "ExecTool",
                        "parameters": {
                            "input": "${generateText}"
                        }
                    }
                ]
        """

        # Parse the JSON input
        try:
            pipeline = json.loads(input) if isinstance(input, str) else input
            if not isinstance(pipeline, list):
                pipeline = [pipeline]
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON input: {input}")

        context = {}

        for step in pipeline:
            # Extract tool name, parameters, and result storage id
            tool_name = step.get("tool")
            parameters = step.get("parameters")
            step_id = step.get("id")

            # Resolve parameter references
            resolved_params = {}
            for param_name, param_value in parameters.items():
                if isinstance(param_value, str):
                    # Look for string substitutions within the parameter string
                    def replace_match(match):
                        ref_id = match.group(1)
                        if ref_id in context:
                            return str(context[ref_id]).strip()  # Added .strip() to remove any newline characters
                        else:
                            raise ValueError(f"Unresolved reference: {ref_id}")
                    # Replace all occurrences of ${identifier} with the corresponding value from context
                    resolved_params[param_name] = re.sub(r'\$\{(\w+)\}', replace_match, param_value)
                else:
                    resolved_params[param_name] = param_value

            # Execute the tool with resolved parameters
            execution_result = self.manager.execute_tool(tool_name, **resolved_params)

            # Store the result in context with identifier
            if step_id:
                context[step_id] = execution_result

        return json.dumps(context)
