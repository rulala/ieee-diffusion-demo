from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from pathlib import Path
from textwrap import dedent
from typing import Any

import gradio as gr
import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")
load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
FIRECRAWL_BASE_URL = os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev/v1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
DEFAULT_SEED_URL = os.getenv("DEFAULT_SEED_URL", "https://en.wikipedia.org/wiki/Ohiya")
DEFAULT_CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
DEFAULT_TOP_K = int(os.getenv("TOP_K", "4"))


class SearchDemoError(RuntimeError):
    pass


def _firecrawl_headers() -> dict[str, str]:
    if not FIRECRAWL_API_KEY:
        raise SearchDemoError("FIRECRAWL_API_KEY was not found. Put it in a local .env file at the repo root.")
    return {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json",
    }


def _scrape_url(url: str) -> Document:
    payload = {"url": url, "formats": ["markdown"]}
    response = requests.post(
        f"{FIRECRAWL_BASE_URL.rstrip('/')}/scrape",
        headers=_firecrawl_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    data = body.get("data", {})
    markdown = data.get("markdown") or ""
    title = data.get("metadata", {}).get("title") or data.get("title") or url
    if not markdown.strip():
        raise SearchDemoError(f"Firecrawl scrape returned no markdown for {url}")
    return Document(page_content=markdown, metadata={"source": url, "title": title, "provider": "firecrawl_scrape"})


def _search_web(query: str, limit: int = 4) -> list[Document]:
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {"formats": ["markdown"]},
    }
    response = requests.post(
        f"{FIRECRAWL_BASE_URL.rstrip('/')}/search",
        headers=_firecrawl_headers(),
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    body = response.json()
    rows = body.get("data") or []
    docs: list[Document] = []
    for row in rows:
        markdown = row.get("markdown") or row.get("content") or ""
        url = row.get("url") or row.get("source") or ""
        title = row.get("title") or url or "Untitled"
        if not markdown.strip() or not url:
            continue
        docs.append(Document(page_content=markdown, metadata={"source": url, "title": title, "provider": row.get("provider", "firecrawl_search")}))
    if not docs:
        raise SearchDemoError("Firecrawl search returned no usable markdown results.")
    return docs


def _build_vectorstore(documents: list[Document], chunk_size: int, chunk_overlap: int) -> tuple[Chroma, str, list[Document]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise SearchDemoError("No chunks were created from the fetched documents.")

    persist_dir = tempfile.mkdtemp(prefix="chroma_search_demo_")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
    collection_name = f"search_demo_{uuid.uuid4().hex[:8]}"
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir,
    )
    return vectorstore, persist_dir, chunks


def _format_sources(documents: list[Document]) -> str:
    seen: set[tuple[str, str]] = set()
    lines = ["## Sources"]
    for doc in documents:
        source = doc.metadata.get("source", "")
        title = doc.metadata.get("title", source)
        key = (title, source)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- **{title}** — {source}")
    return "\n".join(lines)


def _format_retrieved_context(documents: list[Document]) -> str:
    lines = []
    for i, doc in enumerate(documents, start=1):
        title = doc.metadata.get("title", doc.metadata.get("source", f"Chunk {i}"))
        source = doc.metadata.get("source", "")
        chunk = doc.page_content.strip().replace("\r", "")
        if len(chunk) > 1400:
            chunk = chunk[:1400].rstrip() + "…"
        lines.append(f"[{i}] {title}\nSource: {source}\n\n{chunk}")
    return "\n\n---\n\n".join(lines)


def _answer_from_retrieved(question: str, retrieved_docs: list[Document]) -> str:
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', '')}\nTitle: {doc.metadata.get('title', '')}\nContent:\n{doc.page_content}"
        for doc in retrieved_docs
    )

    prompt = dedent(
        f"""
        You are answering a transport-domain question using retrieved evidence only.

        Rules:
        - Use only the provided context.
        - If the answer is not supported by the context, say: "I don't know based on the provided context."
        - Be concise and practical.
        - When you make a claim, ground it in the retrieved material.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    ).strip()

    llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    result = llm.invoke(prompt)
    return getattr(result, "content", str(result)).strip()


def run_search_demo(
    question: str,
    mode: str,
    seed_url: str,
    max_results: int,
    chunk_size: int,
    chunk_overlap: int,
    top_k: int,
) -> tuple[str, str, str, str]:
    if not question.strip():
        raise gr.Error("Enter a question first.")

    seed_url = seed_url.strip() or DEFAULT_SEED_URL
    fetched_docs: list[Document] = []
    persist_dir: str | None = None

    try:
        status_lines = [f"Mode: {mode}"]
        if mode == "Seed URL RAG":
            status_lines.append(f"Scraping seed URL: {seed_url}")
            fetched_docs = [_scrape_url(seed_url)]
        elif mode == "Firecrawl web search":
            status_lines.append(f"Searching the web for: {question}")
            fetched_docs = _search_web(question, limit=max_results)
        elif mode == "Seed URL + Firecrawl web search":
            status_lines.append(f"Scraping seed URL: {seed_url}")
            fetched_docs.append(_scrape_url(seed_url))
            status_lines.append(f"Searching the web for: {question}")
            fetched_docs.extend(_search_web(question, limit=max_results))
        else:
            raise SearchDemoError(f"Unknown mode: {mode}")

        vectorstore, persist_dir, _chunks = _build_vectorstore(fetched_docs, chunk_size, chunk_overlap)
        retrieved_docs = vectorstore.as_retriever(search_kwargs={"k": top_k}).invoke(question)
        if not retrieved_docs:
            raise SearchDemoError("Retriever returned no context.")

        answer = _answer_from_retrieved(question, retrieved_docs)
        sources = _format_sources(retrieved_docs)
        context = _format_retrieved_context(retrieved_docs)
        status_lines.append(f"Fetched documents: {len(fetched_docs)}")
        status_lines.append(f"Retrieved chunks: {len(retrieved_docs)}")
        status = "\n".join(status_lines)
        return answer, sources, context, status
    except requests.HTTPError as e:
        detail = ""
        try:
            detail = e.response.text
        except Exception:
            pass
        raise gr.Error(f"Firecrawl request failed: {e}\n{detail}")
    except Exception as e:
        raise gr.Error(str(e))
    finally:
        if persist_dir and Path(persist_dir).exists():
            shutil.rmtree(persist_dir, ignore_errors=True)


DESCRIPTION = dedent(
    """
    # Tiny Gradio Search Demo

    This is a **small technical UI** for the repo's RAG side.

    It lets people:
    - ask a question
    - use either a **seed URL**, **Firecrawl web search**, or **both**
    - retrieve evidence
    - read the grounded answer, sources, and retrieved chunks

    It is intentionally small: no training, no notebook orchestration, just a demo surface for **search + grounded answering**.
    """
).strip()


with gr.Blocks(title="IEEE Diffusion Demo — Search UI") as demo:
    gr.Markdown(DESCRIPTION)

    with gr.Row():
        question = gr.Textbox(label="Question", placeholder="Ask about a transport topic, safety bulletin, operating procedure, or maintenance issue")
    with gr.Row():
        mode = gr.Radio(
            choices=["Seed URL RAG", "Firecrawl web search", "Seed URL + Firecrawl web search"],
            value="Firecrawl web search",
            label="Search mode",
        )
        seed_url = gr.Textbox(label="Optional seed URL", value=DEFAULT_SEED_URL)
    with gr.Row():
        max_results = gr.Slider(1, 8, value=4, step=1, label="Max Firecrawl search results")
        chunk_size = gr.Slider(300, 2000, value=DEFAULT_CHUNK_SIZE, step=50, label="Chunk size")
        chunk_overlap = gr.Slider(0, 500, value=DEFAULT_CHUNK_OVERLAP, step=10, label="Chunk overlap")
        top_k = gr.Slider(1, 8, value=DEFAULT_TOP_K, step=1, label="Retriever top-k")

    run_btn = gr.Button("Search and answer", variant="primary")

    with gr.Row():
        answer = gr.Markdown(label="Grounded answer")
    with gr.Row():
        sources = gr.Markdown(label="Sources")
    with gr.Accordion("Retrieved evidence", open=False):
        context = gr.Textbox(lines=18, label="Retrieved chunks")
    with gr.Accordion("Run status", open=False):
        status = gr.Textbox(lines=8, label="Status")

    run_btn.click(
        run_search_demo,
        inputs=[question, mode, seed_url, max_results, chunk_size, chunk_overlap, top_k],
        outputs=[answer, sources, context, status],
    )


if __name__ == "__main__":
    demo.launch()
