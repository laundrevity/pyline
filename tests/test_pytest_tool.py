import pytest
import json


def test_tool_with_no_selection(tool_manager):
    selected_tests_str = json.dumps(
        {
            "selected_tests": ["test_pipeline_tool.py"]
        }
    )
    result = tool_manager.execute_tool("PytestTool", input=selected_tests_str)
    print(f"{result=}")
    # assert True
