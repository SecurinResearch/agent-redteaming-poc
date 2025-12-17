"""
Test Setup Script
Verifies that the environment is correctly configured
"""
import sys
from pathlib import Path


def print_header(text):
    """Print section header"""
    print(f"\n{'='*60}")
    print(text)
    print('='*60)


def test_imports():
    """Test if all required packages can be imported"""
    print_header("Testing Package Imports")

    packages = [
        ("langchain", "LangChain"),
        ("langchain_openai", "LangChain OpenAI"),
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("dotenv", "Python-dotenv"),
        ("requests", "Requests"),
    ]

    failed = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            failed.append(name)

    # Optional packages
    print("\nOptional packages (for web search):")
    optional = [
        ("duckduckgo_search", "DuckDuckGo Search"),
        ("bs4", "BeautifulSoup4"),
    ]

    for package, name in optional:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"⚠ {name} - Not installed (optional)")

    if failed:
        print(f"\n❌ Missing required packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✅ All required packages installed")
    return True


def test_config():
    """Test configuration"""
    print_header("Testing Configuration")

    try:
        from config import Config

        print(f"LLM Provider: {Config.LLM_PROVIDER}")

        if Config.LLM_PROVIDER == "litellm":
            print(f"LiteLLM Base URL: {Config.LITELLM_BASE_URL}")
            print(f"LiteLLM Model: {Config.LITELLM_MODEL}")
            if Config.LITELLM_API_KEY:
                print("✓ LiteLLM API Key: Set")
            else:
                print("✗ LiteLLM API Key: NOT SET")
                return False

        elif Config.LLM_PROVIDER == "azure":
            print(f"Azure Endpoint: {Config.AZURE_OPENAI_ENDPOINT}")
            print(f"Azure Deployment: {Config.AZURE_OPENAI_DEPLOYMENT_NAME}")
            if Config.AZURE_OPENAI_API_KEY:
                print("✓ Azure API Key: Set")
            else:
                print("✗ Azure API Key: NOT SET")
                return False

        print("\n✅ Configuration loaded successfully")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_llm_connection():
    """Test LLM connection"""
    print_header("Testing LLM Connection")

    try:
        from llm_factory import LLMFactory

        print("Creating LLM instance...")
        llm = LLMFactory.create_llm()
        print(f"✓ LLM created: {type(llm).__name__}")

        print("\nTesting LLM call...")
        response = llm.invoke("Say 'test successful' if you can read this.")
        print(f"✓ LLM response: {response.content[:100]}")

        print("\n✅ LLM connection working")
        return True

    except Exception as e:
        print(f"❌ LLM connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your .env file configuration")
        print("2. Verify API keys are correct")
        print("3. If using LiteLLM, ensure the proxy is running")
        return False


def test_agents():
    """Test agent initialization"""
    print_header("Testing Agents")

    agents = [
        ("File Operations", "agents.file_operations.agent", "FileOperationsAgent"),
        ("Web Research", "agents.web_research.agent", "WebResearchAgent"),
        ("Communication", "agents.communication.agent", "CommunicationAgent"),
    ]

    all_ok = True
    for name, module, class_name in agents:
        try:
            mod = __import__(module, fromlist=[class_name])
            AgentClass = getattr(mod, class_name)
            agent = AgentClass()
            print(f"✓ {name} Agent")
        except Exception as e:
            print(f"✗ {name} Agent - {str(e)[:50]}")
            all_ok = False

    if all_ok:
        print("\n✅ All agents initialized successfully")
    else:
        print("\n⚠️  Some agents failed to initialize")

    return all_ok


def test_project_structure():
    """Test project structure"""
    print_header("Testing Project Structure")

    required_files = [
        "config.py",
        "llm_factory.py",
        "api_server.py",
        "run_all_scans.py",
        "requirements.txt",
        ".env.example",
        "README.md",
    ]

    required_dirs = [
        "agents/file_operations",
        "agents/web_research",
        "agents/communication",
        "attacks",
        "evaluation",
        "redteaming/agentic_radar",
        "redteaming/agentfence",
        "redteaming/a2a_scanner",
    ]

    all_ok = True

    print("Checking files:")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_ok = False

    print("\nChecking directories:")
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} - MISSING")
            all_ok = False

    if all_ok:
        print("\n✅ Project structure complete")
    else:
        print("\n❌ Some files/directories missing")

    return all_ok


def test_attack_payloads():
    """Test attack payload files"""
    print_header("Testing Attack Payloads")

    import json

    payload_files = [
        "attacks/tool_misuse.json",
        "attacks/harmful_content.json",
    ]

    total_attacks = 0
    for file_path in payload_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            attacks = data.get("attacks", [])
            print(f"✓ {file_path}: {len(attacks)} attacks")
            total_attacks += len(attacks)
        except Exception as e:
            print(f"✗ {file_path}: {e}")

    print(f"\n✅ Total attack scenarios: {total_attacks}")
    return True


def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        AI Agent Red-Teaming PoC - Setup Verification        ║
╚══════════════════════════════════════════════════════════════╝
""")

    results = []

    # Run tests
    results.append(("Project Structure", test_project_structure()))
    results.append(("Package Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Attack Payloads", test_attack_payloads()))
    results.append(("LLM Connection", test_llm_connection()))
    results.append(("Agent Initialization", test_agents()))

    # Summary
    print_header("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  ✅ ALL TESTS PASSED - YOU'RE READY TO GO!                  ║
╚══════════════════════════════════════════════════════════════╝

Next steps:
  1. Run a simple test: python agents/file_operations/agent.py
  2. Start API server: python api_server.py
  3. Run full suite: python run_all_scans.py

For more info, see QUICKSTART.md
""")
        return 0
    else:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  SOME TESTS FAILED - PLEASE FIX ISSUES ABOVE            ║
╚══════════════════════════════════════════════════════════════╝

Common fixes:
  1. Install dependencies: pip install -r requirements.txt
  2. Configure .env: cp .env.example .env && nano .env
  3. Check LLM provider is running (if using LiteLLM)

For help, see README.md or QUICKSTART.md
""")
        return 1


if __name__ == "__main__":
    sys.exit(main())
