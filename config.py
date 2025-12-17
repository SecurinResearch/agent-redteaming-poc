"""
Configuration module for AI Agent Red-teaming PoC
Handles LiteLLM and Azure OpenAI configuration
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration for the PoC"""

    # LLM Provider Selection
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "litellm")  # "litellm" or "azure"

    # LiteLLM Configuration
    LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
    LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "")
    LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gpt-4")

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4")

    # OpenAI (for scanners)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Agent Configuration
    AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "2000"))

    # A2A Protocol Configuration
    A2A_HOST = os.getenv("A2A_HOST", "localhost")
    A2A_PORT = int(os.getenv("A2A_PORT", "8000"))
    A2A_BASE_URL = os.getenv("A2A_BASE_URL", f"http://localhost:8000")

    # File Operations Agent
    FILE_AGENT_ALLOWED_PATHS = os.getenv("FILE_AGENT_ALLOWED_PATHS", "/tmp").split(",")
    FILE_AGENT_MAX_FILE_SIZE = int(os.getenv("FILE_AGENT_MAX_FILE_SIZE", "10485760"))

    # Web Research Agent
    WEB_AGENT_MAX_RESULTS = int(os.getenv("WEB_AGENT_MAX_RESULTS", "5"))
    WEB_AGENT_TIMEOUT = int(os.getenv("WEB_AGENT_TIMEOUT", "30"))

    # Red-teaming Configuration
    REDTEAM_OUTPUT_DIR = os.getenv("REDTEAM_OUTPUT_DIR", "./reports")
    REDTEAM_LOG_LEVEL = os.getenv("REDTEAM_LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration based on provider"""
        if cls.LLM_PROVIDER == "litellm":
            if not cls.LITELLM_API_KEY:
                print("⚠️  Warning: LITELLM_API_KEY not set")
                return False
            if not cls.LITELLM_BASE_URL:
                print("⚠️  Warning: LITELLM_BASE_URL not set")
                return False
        elif cls.LLM_PROVIDER == "azure":
            if not cls.AZURE_OPENAI_API_KEY:
                print("⚠️  Warning: AZURE_OPENAI_API_KEY not set")
                return False
            if not cls.AZURE_OPENAI_ENDPOINT:
                print("⚠️  Warning: AZURE_OPENAI_ENDPOINT not set")
                return False
        else:
            print(f"⚠️  Warning: Unknown LLM_PROVIDER: {cls.LLM_PROVIDER}")
            return False

        return True

    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration based on provider"""
        if cls.LLM_PROVIDER == "litellm":
            return {
                "provider": "litellm",
                "base_url": cls.LITELLM_BASE_URL,
                "api_key": cls.LITELLM_API_KEY,
                "model": cls.LITELLM_MODEL,
                "temperature": cls.AGENT_TEMPERATURE,
                "max_tokens": cls.AGENT_MAX_TOKENS,
            }
        elif cls.LLM_PROVIDER == "azure":
            return {
                "provider": "azure",
                "api_key": cls.AZURE_OPENAI_API_KEY,
                "azure_endpoint": cls.AZURE_OPENAI_ENDPOINT,
                "api_version": cls.AZURE_OPENAI_API_VERSION,
                "deployment_name": cls.AZURE_OPENAI_DEPLOYMENT_NAME,
                "temperature": cls.AGENT_TEMPERATURE,
                "max_tokens": cls.AGENT_MAX_TOKENS,
            }
        else:
            raise ValueError(f"Unknown LLM provider: {cls.LLM_PROVIDER}")

# Validate configuration on import
if __name__ != "__main__":
    if not Config.validate():
        print("\n❌ Configuration validation failed!")
        print("Please copy .env.example to .env and fill in your credentials.")
        print("See .env.example for required variables.\n")
