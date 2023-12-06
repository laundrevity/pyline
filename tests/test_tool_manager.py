import pytest


def test_tool_manager_discovery(tool_manager):
    assert tool_manager is not None
    assert 'GptTool' in tool_manager.tools
    assert 'ExecTool' in tool_manager.tools

    print(f"tools JSON: {tool_manager.get_tools_json()}")

def test_tool_manager_execute(tool_manager):
    response = tool_manager.execute_tool('ExecTool', input='print("Hello World!")')
    assert response == "Hello World!\n"
