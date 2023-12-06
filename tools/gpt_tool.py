from tools.base_tool import BaseTool
from openai import OpenAI
import json


class GptTool(BaseTool):
    def __init__(self, manager, model='gpt-4-1106-preview'):
        super().__init__(manager)
        self.model = model
        self.client = OpenAI()

    def execute(self, input: str) -> str:
        """
        Communicate with OpenAI's GPT model using a JSON string representing messages.

        Args:
            input (str): JSON string representing the messages to send to the model.

                Example:
                [
                    {
                        "role": "user", 
                        "content": "What is 2+2?"
                    }
                ]
        """

        try:
            messages = json.loads(input) if isinstance(input, str) else input
            if not isinstance(messages, list):
                messages = [messages]
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON input: {input}")
        
        print(f"{messages=}")
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        return response.choices[0].message.content
