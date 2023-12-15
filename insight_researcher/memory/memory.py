from typing import List

from .retriever import SearchAPIRetriever
from langchain.retrievers import (
    ContextualCompressionRetriever,
)
from langchain.retrievers.document_compressors import (
    DocumentCompressorPipeline,
    EmbeddingsFilter,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from insight_researcher import log
from .faiss_storage import FaissStorage
from langchain.schema import Document


class Memory:
    def __init__(self, cfg, task_id):
        """
        self.documents = []  # scraper page content list: [{"url": "url1", "raw_content": "content1"}, {"url": "url2", "raw_content": "content2"}]
        self.context = {}  # scraper page content dict: {"url1": "content1", "url2": "content2"}
        self.messages = [] # OpenAI chat messages, not used currently, for future
        """
        self.task_id = task_id
        self.cfg = cfg
        self.embeddings = OpenAIEmbeddings()
        self.documents = []
        self.context = {}
        self.messages = []
        self.faiss_storage = FaissStorage(task_id, self.embeddings)
        self.top_k = cfg.max_search_results_per_query

    def _get_contextual_retriever(self, pages):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        relevance_filter = EmbeddingsFilter(embeddings=self.embeddings, similarity_threshold=0.78)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[splitter, relevance_filter]
        )
        base_retriever = SearchAPIRetriever(
            pages=pages
        )
        contextual_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=base_retriever
        )
        return contextual_retriever

    def _pretty_print_docs(self, docs):
        return f"\n".join(f"Source: {d.metadata.get('source')}\n"
                          f"Title: {d.metadata.get('title')}\n"
                          f"Content: {d.page_content}\n"
                          for i, d in enumerate(docs) if i < self.top_k)

    def _get_context(self, query, pages):
        compressed_docs = self._get_contextual_retriever(pages)
        relevant_docs = compressed_docs.get_relevant_documents(query)  # 这句代码开始真正执行相似度计算，比较耗时
        return self._pretty_print_docs(relevant_docs)

    def add_memory(self, url_content_list):
        """
        Args:
            url_content_list:  url-content pair list, formatted as below
            [{"url": "url1", "raw_content": "content1"}, {"url": "url2", "raw_content": "content2"}]

        """
        self.documents.extend(url_content_list)
        lc_documents = []
        for url_content in url_content_list:
            self.context.update({url_content["url"]: url_content["raw_content"]})
            if url_content["raw_content"] is not None:
                # 之所以在这里才做非None判断，是因为self.context中的key要做已爬url去重，即使爬虫爬不到内容的url也要留着，防止无效重爬
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                for idx, chunk in enumerate(splitter.split_text(url_content["raw_content"])):
                    lc_documents.append(
                        Document(page_content=chunk, metadata={"source": url_content["url"], "chunk_id": idx}))
        self.faiss_storage.add(lc_documents)

    def get_similar_content_by_query(self, query, pages):
        return self._get_context(query, pages)

    def retrieve_memory(self, query):
        docs = self.faiss_storage.search_similar(query, k=self.top_k)
        return self._pretty_print_docs(docs)

    def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url set.
        Args: url_set_input (set[str]): The url set to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.context.keys():
                log.info(f"✅ Adding source url to research: {url}")
                new_urls.append(url)

        return new_urls

    def add_messages(self, messages):
        self.messages.extend(messages)
