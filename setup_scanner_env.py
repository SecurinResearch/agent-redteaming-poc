"""
Setup environment variables for AgentFence and Agentic-Radar to use LiteLLM proxy
"""
import os
from config import Config


def setup_litellm_environment():
    """Configure environment variables for LiteLLM compatibility with scanners"""
    
    print("🔧 Configuring scanners to use LiteLLM proxy...")
    
    # Set OpenAI-compatible environment variables for Agentic-Radar and AgentFence
    os.environ['OPENAI_API_KEY'] = Config.LITELLM_API_KEY
    os.environ['OPENAI_BASE_URL'] = Config.LITELLM_BASE_URL
    os.environ['OPENAI_API_BASE'] = Config.LITELLM_BASE_URL  # Alternative env var name
    os.environ['OPENAI_MODEL'] = Config.LITELLM_MODEL
    
    # Set Azure OpenAI environment variables as fallback (only if not using OpenAI format)
    # Comment out to prioritize OpenAI format for agentic-radar
    # os.environ['AZURE_OPENAI_API_KEY'] = Config.LITELLM_API_KEY
    # os.environ['AZURE_OPENAI_ENDPOINT'] = Config.LITELLM_BASE_URL
    
    # Set additional OpenAI environment variables for compatibility
    os.environ['OPENAI_API_VERSION'] = '2024-02-15-preview'  # Required for some tools
    
    # Set LiteLLM specific environment variables
    os.environ['LITELLM_BASE_URL'] = Config.LITELLM_BASE_URL
    os.environ['LITELLM_API_KEY'] = Config.LITELLM_API_KEY
    os.environ['LITELLM_MODEL'] = Config.LITELLM_MODEL
    
    print("✅ Environment configured:")
    print(f"   API Key: {Config.LITELLM_API_KEY[:10]}...")
    print(f"   Base URL: {Config.LITELLM_BASE_URL}")
    print(f"   Model: {Config.LITELLM_MODEL}")
    
    return True


if __name__ == "__main__":
    setup_litellm_environment()
