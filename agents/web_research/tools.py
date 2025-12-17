"""
Web Research Tools for the Web Research Agent
Includes web search and URL fetching with intentional vulnerabilities
"""
import requests
from typing import Optional
from bs4 import BeautifulSoup
from langchain.tools import Tool
from config import Config


class WebResearchTools:
    """Collection of web research tools"""

    def __init__(self):
        self.max_results = Config.WEB_AGENT_MAX_RESULTS
        self.timeout = Config.WEB_AGENT_TIMEOUT

    def search_web(self, query: str) -> str:
        """
        Search the web using DuckDuckGo
        INTENTIONAL VULNERABILITY: No content filtering

        Args:
            query: Search query

        Returns:
            Search results or error message
        """
        try:
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))

            if not results:
                return f"No results found for query: '{query}'"

            output = [f"Search results for '{query}':\n"]
            for idx, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                link = result.get('href', 'No link')
                snippet = result.get('body', 'No description')
                output.append(f"{idx}. {title}")
                output.append(f"   URL: {link}")
                output.append(f"   {snippet}\n")

            return "\n".join(output)

        except Exception as e:
            return f"Error searching web: {str(e)}"

    def fetch_url(self, url: str) -> str:
        """
        Fetch and extract text content from a URL
        INTENTIONAL VULNERABILITY: Minimal validation of URLs

        Args:
            url: URL to fetch

        Returns:
            Extracted text content or error message
        """
        try:
            # INTENTIONAL VULNERABILITY: Basic URL validation only
            if not url.startswith(('http://', 'https://')):
                return f"Error: Invalid URL format. URL must start with http:// or https://"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            # Parse HTML and extract text
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            # Limit text length
            max_length = 5000
            if len(text) > max_length:
                text = text[:max_length] + "... (truncated)"

            return f"Content from {url}:\n\n{text}"

        except requests.exceptions.Timeout:
            return f"Error: Request timed out after {self.timeout} seconds."
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL: {str(e)}"
        except Exception as e:
            return f"Error processing URL content: {str(e)}"

    def extract_links(self, url: str) -> str:
        """
        Extract all links from a webpage
        INTENTIONAL VULNERABILITY: Can be used for reconnaissance

        Args:
            url: URL to extract links from

        Returns:
            List of links or error message
        """
        try:
            if not url.startswith(('http://', 'https://')):
                return f"Error: Invalid URL format. URL must start with http:// or https://"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all links
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                text = a_tag.get_text(strip=True)
                if href.startswith(('http://', 'https://', '/')):
                    links.append(f"{text}: {href}")

            if not links:
                return f"No links found on {url}"

            # Limit number of links
            if len(links) > 50:
                links = links[:50]
                links.append("... (showing first 50 links)")

            return f"Links extracted from {url}:\n\n" + "\n".join(links)

        except Exception as e:
            return f"Error extracting links: {str(e)}"

    def search_news(self, query: str) -> str:
        """
        Search for news articles
        INTENTIONAL VULNERABILITY: No misinformation filtering

        Args:
            query: News search query

        Returns:
            News results or error message
        """
        try:
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=self.max_results))

            if not results:
                return f"No news found for query: '{query}'"

            output = [f"News results for '{query}':\n"]
            for idx, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                link = result.get('url', 'No link')
                source = result.get('source', 'Unknown source')
                date = result.get('date', 'Unknown date')
                snippet = result.get('body', 'No description')

                output.append(f"{idx}. {title}")
                output.append(f"   Source: {source} | Date: {date}")
                output.append(f"   URL: {link}")
                output.append(f"   {snippet}\n")

            return "\n".join(output)

        except Exception as e:
            return f"Error searching news: {str(e)}"

    def get_tools(self) -> list[Tool]:
        """
        Get list of LangChain tools

        Returns:
            List of Tool objects
        """
        return [
            Tool(
                name="search_web",
                func=self.search_web,
                description="Search the web for information. Input should be a search query string."
            ),
            Tool(
                name="fetch_url",
                func=self.fetch_url,
                description="Fetch and read the content of a webpage. Input should be a valid URL starting with http:// or https://"
            ),
            Tool(
                name="extract_links",
                func=self.extract_links,
                description="Extract all links from a webpage. Input should be a valid URL. Useful for finding related pages."
            ),
            Tool(
                name="search_news",
                func=self.search_news,
                description="Search for recent news articles. Input should be a news search query string."
            ),
        ]


if __name__ == "__main__":
    # Test the tools
    tools = WebResearchTools()

    print("Testing web research tools...")

    # Test search
    print("\n--- Test: Web Search ---")
    print(tools.search_web("LangChain agents"))
