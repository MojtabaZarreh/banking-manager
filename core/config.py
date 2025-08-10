import logging
from abc import abstractmethod
import os

class Settings:
    
    Agent1 = {
        "ENDPOINT": "https://api.groq.com/openai/v1/chat/completions",
        "API_KEY": "#YOUR_API_KEY"
    }
    
    Agent2 = {
        "ENDPOINT": "https://api.groq.com/openai/v1/chat/completions",
        "API_KEY": "#YOUR_API_KEY"
    }
    
    @abstractmethod
    def setup_logging():
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "system.log")

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
settings = Settings()