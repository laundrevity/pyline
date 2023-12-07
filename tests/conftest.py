from utils.tool_manager import ToolManager
import pytest
import tools

@pytest.fixture(scope='module')
def tool_manager():
    return ToolManager()
