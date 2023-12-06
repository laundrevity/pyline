from tools.base_tool import BaseTool
from openai import OpenAI
import json


class GptTool(BaseTool):
    def execute(self, input: str) -> str:
        """
        Communicate with OpenAI's GPT model using a JSON string representing messages.

        Args:
            input (str): JSON string representing the messages to send to the model.

                Example:
                [
                    {
                        "role": "user", 
                        "content": "What is AI?"
                    }
                ]
        """
        client = OpenAI()

        try:
            messages = json.loads(input) if isinstance(input, str) else input
            if not isinstance(messages, list):
                messages = [messages]
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON input: {input}")
        
        print(f"{messages=}")
        response = client.chat.completions.create(
            messages=messages,
            model='gpt-4-1106-preview'
        )
        return response.choices[0].message.content
