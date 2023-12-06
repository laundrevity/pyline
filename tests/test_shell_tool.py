from tools.shell_tool import ShellTool
import json


def test_echo(tool_manager):
    input_str = json.dumps(
        {
            "command": "echo",
            "args": ["greetings"]
        }
    )
    result = tool_manager.execute_tool('ShellTool', input=input_str)
    assert result == 'greetings'
