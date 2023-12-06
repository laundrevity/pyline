from tools.base_tool import BaseTool
from tools.manager_exec_tool import ManagerExecTool
from typing import Dict, List
import inspect
import pkgutil
import importlib
from docstring_parser import parse
import traceback
from openai import OpenAI
from colorama import Fore
import json


class ToolManager:
    def __init__(self, tools_package, model='gpt-4-1106-preview'):
        self.tools: Dict[str, BaseTool] = self.discover_tools(tools_package)
        self.tools['ManagerExecTool'] = ManagerExecTool(self)
        self.client = OpenAI()
        self.model = model
        
    @staticmethod
    def generate_json_for_tool(tool):
        """Generate JSON representation for the tool by introspecting the execute method."""

        # Grab execute function details
        execute_function = tool.execute
        sig = inspect.signature(execute_function)
        parsed_docstring = parse(inspect.getdoc(execute_function))
        parameters = sig.parameters

        # Formulate the JSON for the tool
        json_definition = {
            "type": "function",
            "function": {
                "name": tool.__name__,
                "description": parsed_docstring.short_description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

        for param_name, param in parameters.items():
            if param_name == 'self':  # Skip 'self' parameter
                continue
            
            # Extract the description of the parameter from the docstring
            param_description = next(
                (p.description for p in parsed_docstring.params if p.arg_name == param_name),
                ""
            )

            json_definition["function"]["parameters"]["properties"][param_name] = {
                "type": "string",  # Placeholder, refine as needed for other data types
                "description": param_description
            }

            # Here we're adding parameters as required if they don't have a default value
            if param.default is inspect.Parameter.empty:
                json_definition["function"]["parameters"]["required"].append(param_name)

        return json_definition

    def get_tools_json(self):
        return [
            self.generate_json_for_tool(tool.__class__) for tool in self.tools.values()
        ]

    def discover_tools(self, tools_package):
        tools = {}
        for finder, name, ispkg in pkgutil.iter_modules(
            tools_package.__path__,
            tools_package.__name__ + "."):
            if not ispkg:
                module = importlib.import_module(name)
                for member_name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BaseTool) and member_name != 'BaseTool':
                        # Capitalize the first letter to match the class name convention
                        if 'Manager' not in obj.__name__:
                            tools[obj.__name__] = obj(self)
        return tools
        
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        try:
            tool_obj = self.tools[tool_name]
            return tool_obj.execute(**kwargs)
        except Exception as e:
            return f"Error executing {tool_name}: {traceback.format_exc()} {e}"


    def get_response(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.get_tools_json(),
            tool_choice='auto'
        )
        completion_messages = response.choices[0].message
        messages.append(completion_messages)
        tool_call_responses = []
        # Process each tool call suggested by the GPT response

        if completion_messages.tool_calls:

            for tool_call in completion_messages.tool_calls:
                tool_name = tool_call.function.name
                function_args = tool_call.function.arguments

                # Execute the tool
                if input(f"{Fore.MAGENTA}{tool_name}({function_args}) ? (y/n) ").lower() == 'n':
                    result = f"User rejected tool usage!"
                else:
                    print(f"{Fore.MAGENTA}=>")
                    try:
                        kwargs = json.loads(function_args)
                    except Exception as e:
                        print(f'{Fore.RED}Error parsing JSON {function_args=}: {e}')
                        kwargs = {}

                    result = self.execute_tool(tool_name, **kwargs)
                    print(f"{Fore.MAGENTA}{result}")

                if result is None:
                    result = "None"

                # Prepare response
                tool_response = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "tool_name",
                    "content": json.dumps(result) if isinstance(result, dict) else result
                }
                tool_call_responses.append(tool_response)
            
            messages.extend(tool_call_responses)

            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages # disallow repeated function calls?
            )
            return second_response.choices[0].message
        
        else:
            return completion_messages
