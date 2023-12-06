from tools.base_tool import BaseTool
from contextlib import redirect_stdout
import io


class ExecTool(BaseTool):
    def execute(self, input: str) -> str:
        """
        Execute the given source in the context of globals and locals. The source must be a string representing one or more Python statements.

        Args:
            input (str): source code to execute in the context of globals and locals.
        """
        output = io.StringIO() # Create a StringIO object to capture output
        with redirect_stdout(output):
            try:
                exec(input) # Execute the provided input within the redirect context
            except Exception as e:
                return f"Got error executing {input}: {e}"
        
        return output.getvalue() # Return the contents of output
