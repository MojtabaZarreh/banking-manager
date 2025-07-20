from .base import BaseAgent
from .registry import register_agent
from google.genai import Client
from google.genai.types import HttpOptions 

@register_agent("ocr")
class OCRAgent(BaseAgent):
    def __init__(self, agent_name, model="gemini-2.5-flash", endpoint="https://api.gapgpt.app/", api_key='sk-NoXiKQ9JB8qPlauOmNdNqUiS7tLC4Yp6qWLgkp9BGuL0f2Z7'):
        super().__init__(agent_name, model, endpoint, api_key)
        self.client = Client(http_options=HttpOptions(base_url=endpoint), api_key=self.api_key)
        
    def parse(self, text: str) -> str:
        return "Parse not implemented in this agent."
        
    def analyst(self, income, expense, balance) -> str:
        return "Parse not implemented in this agent."

    def ocr(self, image_path: str) -> str:
        
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        prompt = f"""Extract the following fields from a scanned image of a bank transaction slip written in Persian. Return the result as a JSON object with English keys only. The expected keys are:
                    - amount (integer)
                    - account (string)
                    - balance (integer)
                    - date (string in YYYY-MM-DD format if possible)
                    - type (integer): use -1 for withdrawal and 1 for deposit

                    Do not include any other text, metadata, explanation, or formatting. Return only the JSON output.
                """

        response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    {"role": "user", "parts": [
                        {"text": prompt},
                        {"inline_data": {
                            "mime_type": "image/jpeg", 
                            "data": image_data
                        }}
                    ]}
                ]
        )
             
        return response.text

# agent = OCRAgent("test_ocr")
# result = agent.ocr(r"C:\Users\lecaw\Desktop\banking-manager\agents\phi.jpeg")
# print(result)