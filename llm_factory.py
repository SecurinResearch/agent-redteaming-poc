"""
LLM Factory for creating LangChain LLM instances
Supports LiteLLM proxy and Azure OpenAI
"""
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.language_models import BaseChatModel
from config import Config


class LLMFactory:
    """Factory for creating LLM instances based on configuration"""

    @staticmethod
    def create_llm() -> BaseChatModel:
        """
        Create an LLM instance based on the configured provider

        Returns:
            BaseChatModel: LangChain chat model instance
        """
        llm_config = Config.get_llm_config()

        if llm_config["provider"] == "litellm":
            return LLMFactory._create_litellm_instance(llm_config)
        elif llm_config["provider"] == "azure":
            return LLMFactory._create_azure_instance(llm_config)
        else:
            raise ValueError(f"Unknown LLM provider: {llm_config['provider']}")

    @staticmethod
    def _create_litellm_instance(config: dict) -> ChatOpenAI:
        """
        Create LiteLLM proxy instance using ChatOpenAI
        LiteLLM proxy is OpenAI-compatible, so we use ChatOpenAI with custom base_url

        Args:
            config: LiteLLM configuration dictionary

        Returns:
            ChatOpenAI: LangChain ChatOpenAI instance configured for LiteLLM
        """
        return ChatOpenAI(
            model=config["model"],
            openai_api_key=config["api_key"],
            openai_api_base=config["base_url"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            top_p=1.0
        )

    @staticmethod
    def _create_azure_instance(config: dict) -> AzureChatOpenAI:
        """
        Create Azure OpenAI instance

        Args:
            config: Azure OpenAI configuration dictionary

        Returns:
            AzureChatOpenAI: LangChain AzureChatOpenAI instance
        """
        return AzureChatOpenAI(
            azure_deployment=config["deployment_name"],
            openai_api_version=config["api_version"],
            azure_endpoint=config["azure_endpoint"],
            api_key=config["api_key"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
        )

    @staticmethod
    def create_evaluator_llm() -> BaseChatModel:
        """
        Create an LLM instance specifically for evaluation
        Uses same provider but can be configured differently if needed

        Returns:
            BaseChatModel: LangChain chat model for evaluation
        """
        # For evaluation, we want lower temperature for more consistent judgments
        llm = LLMFactory.create_llm()
        llm.temperature = 0.1
        return llm


# Test the factory
if __name__ == "__main__":
    print("Testing LLM Factory...")
    print(f"Provider: {Config.LLM_PROVIDER}")

    try:
        llm = LLMFactory.create_llm()
        print(f"✅ Successfully created LLM: {type(llm).__name__}")

        # Test a simple call
        response = llm.invoke("Say 'Hello, World!' if you can hear me.")
        print(f"✅ LLM Response: {response.content}")

    except Exception as e:
        print(f"❌ Error creating LLM: {e}")
