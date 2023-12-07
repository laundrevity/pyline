from tools.base_tool import BaseTool
import random
import string
from enum import Enum
import json

class CodeToolState(Enum):
    DONE=0,
    CREATING_TESTS=1,
    FIXING_TESTS=2,

class CodeTool(BaseTool):
    dependencies = ['GptTool', 'ShellTool', 'FileTool', 'SnapTool']

    # def tests_pass(self) -> bool:
    #     result = self.manager.execute_tool('ShellTool', input='{"command": "pytest", "args": []}')
    #     last_line = result.split('\n')[-1]
    #     return 'failed' not in last_line

    def execute(self, input: str) -> str:
        """
        Use GptTool, ShellTool, and FileTool to orchestrate and incorporate suggested modifications to the code.

        Args:
            input (str): Description of the desired changes to make to the code.
        """

        # First, create a new git branch
        branch_name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8))
        branch_command_str = json.dumps({
            "command": "git",
            "args": ["checkout", "-b", f"{branch_name}"]
        })
        self.manager.execute_tool("ShellTool", input=branch_command_str)

        # Now, generate a fresh snapshot and use GptTool to generate a new test
        self.manager.execute_tool("SnapTool", input=json.dumps({'infra': False, 'line_numbers': False}))

        #  Now build the system prompt using the fresh snapshot
        system_prompt = (
            f"You are an quality assurance engineer. "
            f"Your only goal is to create tests which embody the requirements."
            f"You will be given a description of desired functionality, and you will ONLY return valid Python code containing a test for that functionality."
            f"Here is the current project source code:\n\n{open('state.txt').read()}\n\n"
        )
        user_prompt = f"Desired functionality: {input}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        qa_result = self.manager.execute_tool("GptTool", input=json.dumps(messages))
        # Now parse the QA result to ensure it's valid Python code
        # Strip leading and trailing backticks (```) and whitespace
        if qa_result.startswith('```python') and qa_result.endswith('```'):
            qa_result = qa_result[9:-3].strip()
        elif qa_result.startswith('```') and qa_result.endswith('```'):
            qa_result = qa_result[3:-3].strip()
        
        self.manager.logger.debug(f"QA engineer result: {qa_result}")

        # Now, create a new test file
        file_creation_string = json.dumps([
            {
                "action": "create",
                "path": f"/app/tests/test_{branch_name}.py",
                "content": f"{qa_result}"
            }
        ])
        self.manager.execute_tool("FileTool", input=file_creation_string)

        # Try to see if the tests pass, in which case we are more or less done
        tests_pass = False
        while not tests_pass:
            test_result = self.manager.execute_tool('ShellTool', input='{"command": "pytest", "args": []}')
            last_line = test_result.split('\n')[-1]
            if 'failed' not in last_line:
                tests_pass = True
            else:
                # If the tests fail, then try to get a FileTool JSON call from GPT to apply
                # Generate a fresh snap including the possibly new tests or modifications
                self.manager.execute_tool("SnapTool", input=json.dumps({'infra': False, 'line_numbers': False}))

                system_prompt = (
                    f"You are a backend developer. You want to make the tests pass."
                    f"Your ONLY goal is to modify the code until the tests pass -- you are NOT allowed to just modify the tests so that they pass."
                    f"Here is the current project source code:\n\n{open('state.txt').read()}\n\n"
                )
                user_prompt = f"Current failing test output: {test_result}"

                # What to do now? Ideally we want GPT to suggest a function call (e.g. FileTool) that would fix the test
                # but GptTool doesn't currently allow for tools JSON, and it seems unwieldy to explicite create a ChatCompletion here
                return f"failing tests: {test_result}"

        return "Not yet implemented"
