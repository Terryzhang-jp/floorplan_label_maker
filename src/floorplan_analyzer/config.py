import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Configuration class for managing API keys and other settings"""
    
    def __init__(self, env_path: str = None):
        """
        Initialize configuration
        
        Args:
            env_path: Path to .env file (optional)
        """
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()
        
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key or self.api_key == 'your_api_key_here':
            raise ValueError("Please set a valid GOOGLE_API_KEY")
        
        self.model_name = "gemini-1.5-flash"
        self.min_features = 3
        self.max_words_per_feature = 4
        self.min_words_per_feature = 2
    
    @property
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return bool(self.api_key and self.api_key != 'your_api_key_here') 