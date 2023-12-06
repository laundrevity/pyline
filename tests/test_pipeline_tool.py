from tools.pipeline_tool import PipelineTool
import json


def test_simple_pipeline(tool_manager):
    input_str = json.dumps(
        [
            {
                "id": "helloResult",
                "tool": "ExecTool",
                "parameters": {
                    "input": "print('hello world')"
                }
            }
        ]
    )

    result = tool_manager.execute_tool('PipelineTool', input=input_str)
    assert json.loads(result).get('helloResult') == "hello world\n"

def test_substitution_pipeline(tool_manager):
    input_str = json.dumps(
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
    )
    
    result = tool_manager.execute_tool('PipelineTool', input=input_str)
    assert json.loads(result).get('echoResult') == "hello world"
