import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Config class for Insight Researcher."""

    def __init__(self):
        """Initialize the config class."""
        self.retriever = os.getenv('SEARCH_RETRIEVER', "tavily")
        self.llm_provider = os.getenv('LLM_PROVIDER', "ChatOpenAI")
        self.fast_llm_model = os.getenv('FAST_LLM_MODEL', "gpt-4-1106-preview")
        self.smart_llm_model = os.getenv('SMART_LLM_MODEL', "gpt-4-1106-preview")
        self.fast_token_limit = int(os.getenv('FAST_TOKEN_LIMIT', 2000))
        self.smart_token_limit = int(os.getenv('SMART_TOKEN_LIMIT', 4000))
        self.browse_chunk_max_length = int(os.getenv('BROWSE_CHUNK_MAX_LENGTH', 8192))
        self.summary_token_limit = int(os.getenv('SUMMARY_TOKEN_LIMIT', 700))
        self.temperature = float(os.getenv('TEMPERATURE', 0.55))
        self.user_agent = os.getenv('USER_AGENT', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                                  "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        self.max_search_results_per_query = int(os.getenv('MAX_SEARCH_RESULTS_PER_QUERY', 5))
        self.memory_backend = os.getenv('MEMORY_BACKEND', "local")
        self.total_words = int(os.getenv('TOTAL_WORDS', 1000))
        self.report_format = os.getenv('REPORT_FORMAT', "APA")
        self.max_iterations = int(os.getenv('MAX_ITERATIONS', 3))
        self.mock_llm = True if 'true' == os.getenv('MOCK_LLM', 'False').lower() else False
