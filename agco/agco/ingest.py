import os, json, glob
from typing import List, Tuple
import fitz  # pymupdf
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from tqdm import tqdm

DATA_DIR = "data"
CORE_DIR = os.path.join(DATA_DIR, "core")
OPTIONAL_DIR = os.path.join(DATA_DIR, "optional")

INDEX_DIR = "index"
COLLECTION_NAME = "course"


def chunk_text(text: str, n_words: int = 1000, overlap: int = 200) -> List[str]:
    words = text.split()
    if not words:
        return []
    out = []
    step = max(1, n_words - overlap)
    i = 0
    while i < len(words):
        out.append(" ".join(words[i : i + n_words]))
        i += step
    return out


def read_pdf_pages_with_sections(path: str) -> List[Tuple[int, str, str]]:
    """Return list of (page_num, page_text, section_title) tuples."""
    doc = fitz.open(path)
    toc = doc.get_toc(simple=True) or []

    page_to_section = {}
    for _, title, page in toc:
        # PyMuPDF TOC uses 1-indexed pages
        page_to_section[max(0, page - 1)] = title

    current_section = ""
    out: List[Tuple[int, str, str]] = []
    for i in range(len(doc)):
        if i in page_to_section:
            current_section = page_to_section[i]
        text = doc[i].get_text("text") or ""
        out.append((i, text, current_section))
    return out


def list_pdfs() -> List[Tuple[str, str]]:
    """Return [(tier, path), ...] for all PDFs in core/optional."""
    pairs: List[Tuple[str, str]] = []
    for tier, root in [("core", CORE_DIR), ("optional", OPTIONAL_DIR)]:
        for p in glob.glob(os.path.join(root, "**", "*.pdf"), recursive=True):
            pairs.append((tier, p))
    return pairs


def build_index():
    os.makedirs(INDEX_DIR, exist_ok=True)

    client = chromadb.PersistentClient(
        path=INDEX_DIR,
        settings=Settings(anonymized_telemetry=False),
    )
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    col = client.get_or_create_collection(COLLECTION_NAME, embedding_function=embed_fn)

    all_docs, all_metas, all_ids = [], [], []

    pdfs = list_pdfs()
    if not pdfs:
        print(f"[WARN] No PDFs found. Expected folders: {CORE_DIR}/ and/or {OPTIONAL_DIR}/")
        return

    for tier, p in tqdm(pdfs, desc="PDFs"):
        try:
            pages = read_pdf_pages_with_sections(p)
        except Exception as e:
            print(f"[WARN] Failed to open {p}: {e}")
            continue

        for page_num, page_text, section in pages:
            page_text = (page_text or "").strip()
            if not page_text:
                continue

            chunks = chunk_text(page_text, n_words=900, overlap=180)
            for j, ch in enumerate(chunks):
                all_docs.append(ch)
                all_metas.append(
                    {
                        "source": os.path.basename(p),
                        "type": "pdf",
                        "tier": tier,          # <-- core vs optional
                        "page": page_num,
                        "section": section,
                    }
                )
                all_ids.append(f"{tier}::{os.path.basename(p)}::p{page_num}::{j}")

    # Add to vector index (batched)
    B = 256
    for i in tqdm(range(0, len(all_docs), B), desc="Indexing"):
        col.add(
            documents=all_docs[i : i + B],
            metadatas=all_metas[i : i + B],
            ids=all_ids[i : i + B],
        )

    # Mirror for lexical / BM25 usage
    jpath = os.path.join(INDEX_DIR, "docs.jsonl")
    with open(jpath, "w", encoding="utf-8") as f:
        for _id, doc, meta in zip(all_ids, all_docs, all_metas):
            rec = {"id": _id, "text": doc, "meta": meta}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote lexical corpus mirror: {jpath}")
    print("Done.")


def main():
    build_index()


if __name__ == "__main__":
    main()

