from tools.base_tool import BaseTool
from contextlib import redirect_stdout
import traceback
import io


class ExecTool(BaseTool):
    def execute(self, input: str) -> str:
        """
        Execute the given source in the context of the ToolManager instance. The source must be a string representing one or more Python statements.

        Args:
            input (str): source code to execute in the context of the ToolManager instance.
        """
        output = io.StringIO() # Create a StringIO object to capture output
        with redirect_stdout(output):
            local_vars = {'manager': self.manager}
            try:
                # Pass 'manager' to the exec so it has access to the ToolManager instance
                exec(input, globals(), local_vars)
            except Exception as e:
                return f"Got error executing {input}: {traceback.format_exc()} {e}"
        
        return output.getvalue()
    