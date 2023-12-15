from .retrievers import get_retriever
from .scraper import Scraper
from insight_researcher import log


class Tool:
    def __init__(self, cfg, memory):
        self.cfg = cfg
        self.retriever = get_retriever(cfg.retriever)
        self.scraper = Scraper(cfg)
        self.memory = memory

    def scrape_sites_by_query(self, sub_query):
        """
        Args:
            sub_query:
        Returns:
        TODO: 细品，返回值的逻辑有些许问题，后面再修复
        """
        # Get Urls
        retriever = self.retriever(sub_query)
        search_results = retriever.search(max_results=self.cfg.max_search_results_per_query)
        new_search_urls = self.memory.get_new_urls([url.get("href") for url in search_results])
        if new_search_urls is None or 0 == len(new_search_urls):
            return []

        # Scrape Urls
        log.info(f"📝Scraping urls {new_search_urls}...")
        scraped_url_content_list = self.scraper.run(new_search_urls)
        self.memory.add_memory(scraped_url_content_list)
        scraped_url_content_list = [url_content for url_content in scraped_url_content_list if
                                    url_content['raw_content'] is not None]
        return scraped_url_content_list
