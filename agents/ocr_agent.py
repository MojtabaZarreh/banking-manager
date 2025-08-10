import base64
from .base import BaseAgent
from .registry import register_agent
from core.config import settings
from groq import Groq

@register_agent("ocr")
class OCRAgent(BaseAgent):
    def __init__(self, agent_name, model="meta-llama/llama-4-scout-17b-16e-instruct", api_key=settings.Agent1['API_KEY']):
        super().__init__(agent_name, model, api_key)
        self.client = Groq(api_key=self.api_key)
        
    def parse(self, text: str) -> str:
        return "Parse not implemented in this agent."
        
    def analyst(self, income, expense, balance) -> str:
        return "Parse not implemented in this agent."

    def ocr(self, image_url: str) -> str:
        prompt = """Extract the following fields from a scanned image of a bank transaction slip written in Persian. Return the result as a JSON object with English keys only. The expected keys are:
                    - amount (integer)
                    - account (string)
                    - balance (integer)
                    - date (string in YYYY-MM-DD format if possible)
                    - type (integer): use -1 for withdrawal and 1 for deposit

                    Do not include any other text, metadata, explanation, or formatting. Return only the JSON output.
                """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
        )
        return response.choices[0].message.content

# agent = OCRAgent("ocr")
# result = agent.ocr('')
# print(result)