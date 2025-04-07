import requests
from typing import Dict, Any, Optional
from config.config import PROMPT, API_KEY_GEMINI, load_model_config
from time import time

class GeminiAPI:
    def __init__(self):
        # 加载Gemini模型配置
        config = load_model_config('gemini')
        self.base_url = config['base_url']
        self.model = config['model']
        self.api_key = API_KEY_GEMINI

    def ask(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": PROMPT.format(time(), question)
                        }
                    ]
                }
            ]
        }

        params = {
            "key": self.api_key
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini API request failed: {str(e)}")