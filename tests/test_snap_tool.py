import pytest
from unittest.mock import mock_open, patch
from tools.snap_tool import SnapTool
import json

def test_snap_tool_includes_py_files():
    # Instantiate SnapTool
    snap_tool = SnapTool(None)

    result = snap_tool.execute('{"infra": true}')

    assert 'test_snap_tool_includes_py_files' in result

def test_snap_tool_excludes_infra_files():
    # Instantiate SnapTool
    snap_tool = SnapTool(None)

    args = {'input': {'infra': False}}
    result_min = snap_tool.execute(json.dumps(args))
    result_full = snap_tool.execute('{"infra": true}')

    assert len(result_full) > len(result_min)
