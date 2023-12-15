from typing import List
from pathlib import Path
from insight_researcher import log, PROJECT_ROOT
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document
import faiss
import pickle


class FaissStorage:
    """
    The memory storage with Faiss as ANN search engine
    """

    def __init__(self, task_id, embeddings):
        self.task_id: str = task_id
        self.mem_path: Path = Path(PROJECT_ROOT / f"mem/{self.task_id}/")
        self._initialized: bool = False
        self.embeddings = embeddings
        self.store: FAISS = None  # Faiss engine

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    def recover_memory(self, task_id: str) -> List[Document]:
        self.task_id = task_id
        self.mem_path = Path(PROJECT_ROOT / f"mem/{self.task_id}/")
        self.mem_path.mkdir(parents=True, exist_ok=True)
        self.store = self._load()
        documents = []
        for _id, document in self.store.docstore._dict.items():
            documents.append(document)
        self._initialized = True

        return documents

    def _get_index_and_store_fname(self):
        index_fpath = Path(self.mem_path / f'{self.task_id}.index')
        storage_fpath = Path(self.mem_path / f'{self.task_id}.pkl')
        return index_fpath, storage_fpath

    def _write(self, docs, metadatas):
        store = FAISS.from_texts(docs, self.embeddings, metadatas=metadatas)
        return store

    def _load(self):
        index_file, store_file = self._get_index_and_store_fname()
        if not (index_file.exists() and store_file.exists()):
            log.info("Missing at least one of index_file/store_file, load failed and return None")
            return None
        index = faiss.read_index(str(index_file))
        with open(str(store_file), "rb") as f:
            store = pickle.load(f)
        store.index = index
        return store

    def persist(self):
        # create faiss persist directory
        if not self.mem_path.exists():
            self.mem_path.mkdir(parents=True, exist_ok=True)
        index_file, store_file = self._get_index_and_store_fname()
        store = self.store
        index = self.store.index
        faiss.write_index(store.index, str(index_file))
        store.index = None
        with open(store_file, "wb") as f:
            pickle.dump(store, f)
        store.index = index
        log.debug(f'Agent {self.role_id} persist memory into local')

    def add(self, documents: List[Document]) -> bool:
        """ add message into memory storage"""

        docs = [document.page_content for document in documents]
        metadatas = [document.metadata for document in documents]
        if not self.store:
            # init Faiss
            self.store = self._write(docs, metadatas)
            self._initialized = True
        else:
            self.store.add_texts(texts=docs, metadatas=metadatas)
        # self.persist()
        log.info(f"Agent {self.task_id}'s memory_storage add a message")

    def search_similar(self, query, k=4) -> List[Document]:
        """search for dissimilar messages"""
        if not self.store:
            return []
        resp = self.store.similarity_search_with_score(
            query=query,
            k=k
        )
        return [item for item, score in resp]

    def clean(self):
        index_fpath, storage_fpath = self._get_index_and_store_fname()
        if index_fpath and index_fpath.exists():
            index_fpath.unlink(missing_ok=True)
        if storage_fpath and storage_fpath.exists():
            storage_fpath.unlink(missing_ok=True)

        self.store = None
        self._initialized = False
        