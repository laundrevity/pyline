import pytest
import json
import os


def test_create_and_remove_file(tool_manager):
    # Create a small text file
    input_str = json.dumps(
        [
            {
                "action": "create",
                "path": "foo.txt",
                "content": "initial content of the file"
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=input_str)
   
    # Verify that file exists
    assert os.path.exists(os.path.join(os.getcwd(), 'foo.txt'))

    # Remove the small file
    input_str = json.dumps(
        [
            {
                "action": "remove",
                "path": "foo.txt"
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=input_str)
    assert not os.path.exists(os.path.join(os.getcwd(), 'foo.txt'))

@pytest.fixture(scope='function')
def temp_file(tmp_path):
    # Create a new temp file for a test
    file = tmp_path / 'test.txt'
    file.write_text("Line 1\nLine 2\nLine 3\n")
    return str(file)

def test_insert_line(tool_manager, temp_file):
    # Insert a line into the test file at specified index
    input_str = json.dumps(
        [
            {
                "action": "insert",
                "path": temp_file,
                "line_number": 2,
                "content": "Inserted line"
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=input_str)

    # Verify that line is inserted at the right position
    with open(temp_file, 'r') as f:
        lines = f.readlines()
    assert lines[1] == "Inserted line\n"

def test_update_line(tool_manager, temp_file):
    # Update a line in the test file
    input_str = json.dumps(
        [
            {
                "action": "update",
                "path": temp_file,
                "line_number": 1,
                "content": "Updated line 1"
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=input_str)

    # Verify that the line has been updated
    with open(temp_file, 'r') as f:
        lines = f.readlines()
    assert lines[0] == "Updated line 1\n"

def test_delete_line(tool_manager, temp_file):
    # Delete a line in the test file
    input_str = json.dumps(
        [
            {
                "action": "delete",
                "path": temp_file,
                "line_number": 2
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=input_str)

    # Verify that the line has been deleted
    with open(temp_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "Line 3" not in lines

def test_combined_operations(tool_manager, temp_file):
    # Perform a combination of operations: create, insert, update, and delete lines
    
    print(f"before file ops: {open(temp_file, 'r').readlines()}")
    
    file_ops = json.dumps(
        [
            {
                "action": "insert",
                "path": temp_file,
                "line_number": 1,
                "content": "Inserted line at top"
            },
            {
                "action": "update",
                "path": temp_file,
                "line_number": 2,
                "content": "Updated old line 1"
            },
            {
                "action": "delete",
                "path": temp_file,
                "line_number": 3
            }
        ]
    )
    tool_manager.execute_tool('FileTool', input=file_ops)

    # Check the result of the operations
    with open(temp_file, 'r') as f:
        lines = f.readlines()
    
    print(f"{lines=}")
    
    assert lines[0] == "Inserted line at top\n"
    assert lines[1] == "Updated old line 1\n"
    assert "Line 1" not in lines

def test_non_existing_line_operations(tool_manager, temp_file):
    # Attempt to update a non-existing line index, should raise an error
    input_str = json.dumps(
        [
            {
                "action": "update",
                "path": temp_file,
                "line_number": 10,
                "content": "Non-existing line"
            }
        ]
    )
    result = tool_manager.execute_tool('FileTool', input=input_str)
    error = result.split('\n')[-1]
    assert error == ' Line number out of range'