

def get_retriever(retriever):
    """
    Gets the retriever
    Args:
        retriever: retriever name

    Returns:
        retriever: Retriever class

    """
    match retriever:
        case "tavily":
            from insight_researcher.tools.retrievers import TavilySearch
            retriever = TavilySearch
        case "google":
            from insight_researcher.tools.retrievers import GoogleSearch
            retriever = GoogleSearch
        case "searx":
            from insight_researcher.tools.retrievers import SearxSearch
            retriever = SearxSearch
        case "serpapi":
            raise NotImplementedError("SerpApiSearch is not fully implemented yet.")
            from insight_researcher.tools.retrievers import SerpApiSearch
            retriever = SerpApiSearch
        case "googleSerp":
            from insight_researcher.tools.retrievers import SerperSearch
            retriever = SerperSearch
        case "duckduckgo":
            from insight_researcher.tools.retrievers import Duckduckgo
            retriever = Duckduckgo
        case "BingSearch":
            from insight_researcher.tools.retrievers import BingSearch
            retriever = BingSearch

        case _:
            raise Exception("Retriever not found.")

    return retriever

