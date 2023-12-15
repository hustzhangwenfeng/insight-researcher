# Tavily API Retriever

# libraries
import os
from tavily import TavilyClient
from requests.exceptions import HTTPError, ReadTimeout, SSLError, ConnectionError, Timeout
from tenacity import (
    after_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from insight_researcher.utils.logs import log


class TavilySearch():
    """
    Tavily API Retriever
    """
    def __init__(self, query):
        """
        Initializes the TavilySearch object
        Args:
            query:
        """
        self.query = query
        self.api_key = self.get_api_key()
        self.client = TavilyClient(self.api_key)

    def get_api_key(self):
        """
        Gets the Tavily API key
        Returns:

        """
        # Get the API key
        try:
            api_key = os.environ["TAVILY_API_KEY"]
        except:
            raise Exception("Tavily API key not found. Please set the TAVILY_API_KEY environment variable. "
                            "You can get a key at https://app.tavily.com")
        return api_key

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        after=after_log(log, log.level("WARNING").name),
        retry=retry_if_exception_type((HTTPError, ReadTimeout, SSLError, ConnectionError, Timeout))
    )
    def search(self, max_results=7):
        """
        Searches the query
        Returns:

        """
        # Search the query
        results = self.client.search(self.query, search_depth="advanced", max_results=max_results)
        # Return the results
        search_response = [{"href": obj["url"], "body": obj["content"]} for obj in results.get("results", [])]
        return search_response
