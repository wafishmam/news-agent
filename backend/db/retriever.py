import os
import logging
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from ..agents.state import ArchiveResult

logger = logging.getLogger(__name__)

COLLECTION_NAME = "news_archive"
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")


def get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=PERSIST_DIR)

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    return collection


def retrieve_archive(query: str, k: int = 5) -> list[ArchiveResult]:
    collection = get_collection()

    if collection.count() == 0:
        logger.warning("[retriever] Archive is empty. Run scripts/seed_db.py first.")
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    archive_results: list[ArchiveResult] = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        archive_results.append({
            "title": meta.get("title", "Untitled"),
            "content": doc,
            "date": meta.get("date", "Unknown"),
            "relevance_score": round(1 - dist, 4),
        })

    return archive_results


def ingest_articles(articles: list[dict]) -> int:
    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for article in articles:
        ids.append(article["id"])
        documents.append(article["content"])
        metadatas.append({
            "title": article.get("title", ""),
            "date": article.get("date", ""),
            "url": article.get("url", ""),
        })

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    logger.info(f"[ingest] Upserted {len(ids)} articles into ChromaDB")
    return len(ids)