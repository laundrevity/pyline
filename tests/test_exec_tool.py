import pytest


def test_exec_tool_execution(tool_manager):
    exec_tool = tool_manager.tools['ExecTool']
    code = 'x = 1 + 1\nresult = x * 2\nprint(result)'
    expected_result = '4'
    response = exec_tool.execute(input=code)
    assert response.strip() == expected_result

def test_exec_tool_with_syntax_error(tool_manager):
    exec_tool = tool_manager.tools['ExecTool']
    code_with_error = 'x = 1 + '
    response = exec_tool.execute(input=code_with_error)
    assert "SyntaxError" in response or "Got error executing" in response
