from tools.base_tool import BaseTool
import json
import re


class PipelineTool(BaseTool):
    @staticmethod
    def substitute_placeholders(params, outputs):
        for key, value in params.items():
            if isinstance(value, str):
                # Substitute placeholders in strings
                for output_key, output_value in outputs.items():
                    placeholder = f"${{{output_key}}}"
                    if placeholder in value:
                        value = value.replace(placeholder, output_value)
                params[key] = value
            elif isinstance(value, dict):
                # Recursively handle dictionaries
                PipelineTool.substitute_placeholders(value, outputs)
            elif isinstance(value, list):
                # Handle lists: iterate through elements and substitute placeholders in strings
                params[key] = [
                    v.replace(f"${{{output_key}}}", outputs[output_key]) 
                    if isinstance(v, str) else v 
                    for v in value for output_key in outputs 
                    if f"${{{output_key}}}" in str(v)
                ]


    def execute(self, input: str) -> str:
        """
        Execute the given sequence of tool calls using a JSON string representing tool calls and arguments.

        Args:
            input (str): JSON string representing the sequence of tool calls to make. Note that we can use $ together with identifiers to pass along output from one tool to another later tool. Do NOT include 'functions.' in the tool name -- simply use GptTool, ShellTool, etc. Notice that each object in the JSON list here has a "parameters" key -- NOT an "args" key.

                Example:
                [
                    {
                        "id": "helloResult",
                        "tool": "ExecTool",
                        "parameters": {
                            "input": "print('hello world')"
                        }
                    },
                    {
                        "id": "echoResult",
                        "tool": "ShellTool",
                        "parameters": {
                            "input": {
                                "command": "echo",
                                "args": ["${helloResult}"]
                            }
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

            self.substitute_placeholders(parameters, context)

            # Execute the tool with resolved parameters
            execution_result = self.manager.execute_tool(tool_name, **parameters)

            # Store the result in context with identifier
            if step_id:
                context[step_id] = execution_result

        return json.dumps(context)
