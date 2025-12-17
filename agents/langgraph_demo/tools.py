"""
Tools for LangGraph Demo Agent
Includes basic tools with intentional vulnerabilities for red-teaming
"""
import os
import subprocess
import requests
from typing import Optional, Dict, Any
from langchain.tools import Tool


class LangGraphDemoTools:
    """Tools for the LangGraph Demo Agent with intentional vulnerabilities"""

    def __init__(self):
        self.tools = self._create_tools()

    def _create_tools(self) -> list:
        """Create and return list of tools"""
        return [
            Tool(
                name="web_search",
                description="Search the web for information. Input should be a search query string.",
                func=self.web_search
            ),
            Tool(
                name="execute_command",
                description="Execute system commands. DANGEROUS: Use with extreme caution!",
                func=self.execute_command
            ),
            Tool(
                name="read_file",
                description="Read contents of a file. Input should be a file path.",
                func=self.read_file
            ),
            Tool(
                name="write_file",
                description="Write content to a file. Input should be 'filepath|content'.",
                func=self.write_file
            ),
            Tool(
                name="get_environment",
                description="Get environment variables and system information.",
                func=self.get_environment
            )
        ]

    def web_search(self, query: str) -> str:
        """
        Search the web using a simple HTTP request
        VULNERABILITY: No input validation, potential SSRF
        """
        try:
            # Intentional vulnerability: Direct URL construction without validation
            if query.startswith("http"):
                # Direct URL access - potential SSRF vulnerability
                response = requests.get(query, timeout=5)
                return f"Response from {query}: {response.text[:500]}..."
            
            # Simple search simulation
            return f"Web search results for '{query}': [Simulated results - implement with real search API]"
        except Exception as e:
            return f"Search error: {str(e)}"

    def execute_command(self, command: str) -> str:
        """
        Execute system commands
        VULNERABILITY: Command injection, no sanitization
        """
        try:
            # Intentional vulnerability: Direct command execution without sanitization
            result = subprocess.run(
                command,
                shell=True,  # Dangerous: allows command injection
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return f"Command executed successfully:\n{result.stdout}"
            else:
                return f"Command failed with error:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Command timed out after 10 seconds"
        except Exception as e:
            return f"Execution error: {str(e)}"

    def read_file(self, filepath: str) -> str:
        """
        Read file contents
        VULNERABILITY: Path traversal, no access controls
        """
        try:
            # Intentional vulnerability: No path validation, allows directory traversal
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Limit output size
            if len(content) > 1000:
                return f"File content (first 1000 chars):\n{content[:1000]}..."
            else:
                return f"File content:\n{content}"
                
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, input_str: str) -> str:
        """
        Write content to file
        VULNERABILITY: Arbitrary file write, no path validation
        """
        try:
            # Parse input: filepath|content
            if '|' not in input_str:
                return "Error: Input format should be 'filepath|content'"
            
            filepath, content = input_str.split('|', 1)
            
            # Intentional vulnerability: No path validation, allows arbitrary file write
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return f"Successfully wrote {len(content)} characters to {filepath}"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def get_environment(self, query: str = "") -> str:
        """
        Get environment information
        VULNERABILITY: Information disclosure
        """
        try:
            info = {
                "current_directory": os.getcwd(),
                "environment_variables": dict(os.environ),  # Leaks all env vars
                "user": os.getenv("USER", "unknown"),
                "home": os.getenv("HOME", "unknown"),
                "path": os.getenv("PATH", "unknown")
            }
            
            # Intentional vulnerability: Exposes sensitive environment information
            return f"System Information:\n{str(info)[:1000]}..."
            
        except Exception as e:
            return f"Error getting environment info: {str(e)}"

    def get_tools(self) -> list:
        """Return the list of tools"""
        return self.tools


def test_tools():
    """Test the tools"""
    print("Testing LangGraph Demo Tools...")
    
    tools_manager = LangGraphDemoTools()
    tools = tools_manager.get_tools()
    
    print(f"Created {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")


if __name__ == "__main__":
    test_tools()
