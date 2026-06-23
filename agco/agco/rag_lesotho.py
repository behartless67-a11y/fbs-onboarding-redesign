import json
import os
import re
from collections import defaultdict
from typing import Iterable, Optional, Sequence, Set

import chromadb
import pandas as pd
import requests
import streamlit as st
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi

# ---------------- Config ----------------
INDEX_DIR = os.environ.get("INDEX_DIR", "index")
LLAMA_API_BASE = os.environ.get("LLAMA_API_BASE", "http://127.0.0.1:8080/v1").rstrip("/")
LLM_MODEL = os.environ.get("LLM_MODEL", "agco-lesotho")
COLLECTION = os.environ.get("CHROMA_COLLECTION", "course")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")

REQUEST_TIMEOUT = (10, 300)
RECENT_CHAT_MESSAGES = 6
MAX_MEMORY_CHARS = 1400
MAX_CONTEXT_CHARS_PER_CHUNK = 900

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
ANALYSIS_BLOCK_RE = re.compile(r"<\|channel\|>analysis<\|message\|>.*?(?:<\|end\|>|$)", re.DOTALL)
FOLLOWUP_PREFIXES = (
    "and",
    "what about",
    "how about",
    "what if",
    "why",
    "when",
    "where",
    "which",
    "that",
    "those",
    "these",
    "it",
    "they",
    "them",
    "this",
    "he",
    "she",
)
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "if",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "them",
    "there",
    "these",
    "they",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
}
CONTROL_INTENT_TOKENS = {
    "control",
    "deal",
    "dealing",
    "fight",
    "fighting",
    "kill",
    "killing",
    "manage",
    "management",
    "prevent",
    "prevention",
    "protect",
    "reduce",
    "stop",
    "stopping",
    "treat",
    "treatment",
}
PEST_HINT_TOKENS = {
    "aphid",
    "aphids",
    "beetle",
    "beetles",
    "borer",
    "borers",
    "bug",
    "bugs",
    "cutworm",
    "cutworms",
    "fly",
    "flies",
    "fungal",
    "fungus",
    "insect",
    "insects",
    "locust",
    "locusts",
    "moth",
    "moths",
    "pest",
    "pests",
    "termite",
    "termites",
    "weevil",
    "weevils",
    "worm",
    "worms",
}
CURATED_FALLBACKS = [
    {
        "label": "bagrada-bug",
        "aliases": ["bagrada", "bagrada bug", "bagrada bugs", "bagrada hilaris"],
        "queries": [
            (
                "curated-bagrada-control",
                "bagrada bug bagrada hilaris insect pests pest control integrated pest management crop rotation intercropping botanical pesticide lesotho",
                0.96,
            )
        ],
        "note": (
            "The documents identify Bagrada bug as an important pest in Lesotho, "
            "but they may only provide general insect-pest control guidance rather than "
            "Bagrada-specific treatment steps. If that happens, say so plainly and then give the general guidance."
        ),
    },
    {
        "label": "stem-borer",
        "aliases": [
            "stem borer",
            "stem borers",
            "stalk borer",
            "stalk borers",
            "stock borer",
            "stock borers",
            "busseola busca",
            "busseola fusca",
        ],
        "queries": [
            (
                "curated-stem-borer-control",
                "stem borer stalk borer busseola insect pest control intercropping early sowing crop residue integrated pest management",
                0.94,
            )
        ],
        "note": (
            "If exact stem-borer treatment steps are thin, answer with the best documented general cereal-pest control guidance in the context."
        ),
    },
    {
        "label": "aphids",
        "aliases": ["aphid", "aphids", "greenfly", "greenflies", "nsabwe"],
        "queries": [
            (
                "curated-aphid-control",
                "aphids greenflies insect pest control intercropping weeding botanical pesticide integrated pest management",
                0.9,
            )
        ],
        "note": "If the context names aphids but lacks a precise treatment recipe, use the general insect-pest control guidance from the documents.",
    },
    {
        "label": "cutworms",
        "aliases": ["cutworm", "cutworms"],
        "queries": [
            (
                "curated-cutworm-control",
                "cutworms insect pest control seed dressing host destruction foliar spray integrated pest management",
                0.9,
            )
        ],
        "note": "If the context only partly covers cutworms, use the general pest-control guidance that is explicitly documented.",
    },
]

SYSTEM_PROMPT = (
    "You are an agricultural document assistant focused on Lesotho.\n"
    "Use the conversation history only to resolve follow-up references and user intent.\n"
    "Every factual claim in your answer must be grounded in the CURRENT CONTEXT excerpts.\n"
    "If the CURRENT CONTEXT does not support the answer, say exactly:\n"
    "\"I can't find this in the documents I have. If you add a relevant document or enable Optional documents, I can try again.\"\n"
    "Do not invent facts, citations, or recommendations.\n"
    "Cite supporting sentences immediately with the provided tags like [3] or [3][7].\n"
    "Do not use markdown tables. Prefer a short heading and bullet points.\n"
    "If the documents name a specific pest or problem but only provide general control guidance rather than a species-specific treatment, say that plainly and then give the general guidance.\n"
    "Assume the answer will be read on a tablet in the field.\n"
    "Default to 3-5 short bullets and keep the full answer around 80-140 words unless the user asks for more detail.\n"
    "Focus on the most useful actions first, not every possible detail.\n"
    "If key details are missing, ask at most 1 short follow-up question."
)

st.set_page_config(page_title="AgCo (Lesotho)", layout="wide")
st.title("Ag(ricultural) Co(mpendium), Lesotho")

st.markdown(
    """
    <style>
    [data-testid^="chatAvatarIcon-"] {
        display: none !important;
    }

    [data-testid="stChatMessageContent"] {
        margin-left: 3px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def tokenize_text(text: str) -> list[str]:
    return [tok.lower() for tok in TOKEN_RE.findall(text or "")]


def normalize_llm_math(text: str) -> str:
    text = re.sub(
        r"\\\[(.+?)\\\]",
        lambda match: f"\n$$\n{match.group(1).strip()}\n$$\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\\\((.+?)\\\)",
        lambda match: f"${match.group(1).strip()}$",
        text,
        flags=re.DOTALL,
    )
    return text


def normalize_display_spaces(text: str) -> str:
    return (
        text.replace("\u202f", " ")
        .replace("\u00a0", " ")
        .replace("\u2007", " ")
        .replace("\u2009", " ")
    )


def strip_model_control_tokens(text: str, trim: bool = False) -> str:
    if not text:
        return ""

    cleaned = ANALYSIS_BLOCK_RE.sub("", text)
    replacements = (
        "<|start|>assistant<|channel|>final<|message|>",
        "<|channel|>final<|message|>",
        "<|start|>assistant<|channel|>commentary<|message|>",
        "<|channel|>commentary<|message|>",
        "<|return|>",
        "<|end|>",
        "<|message|>",
        "<|start|>assistant",
    )
    for marker in replacements:
        cleaned = cleaned.replace(marker, "")

    cleaned = re.sub(r"<\|[^>]+\|>", "", cleaned)
    cleaned = normalize_display_spaces(cleaned)
    return cleaned.strip() if trim else cleaned


if "chat" not in st.session_state:
    st.session_state.chat = []


def shorten_line(text: str, max_chars: int = 220) -> str:
    text = normalize_whitespace(text)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def shorten_context_chunk(text: str, max_chars: int = MAX_CONTEXT_CHARS_PER_CHUNK) -> str:
    text = normalize_whitespace(text)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def build_memory_summary(chat: Sequence[dict], keep_last: int = RECENT_CHAT_MESSAGES) -> str:
    older = list(chat[:-keep_last]) if len(chat) > keep_last else []
    if not older:
        return ""

    lines = []
    for msg in older[-8:]:
        content = shorten_line(msg.get("content", ""))
        if not content:
            continue
        role = "User" if msg.get("role") == "user" else "Assistant"
        lines.append(f"- {role}: {content}")

    if not lines:
        return ""

    summary = "Earlier in this session:\n" + "\n".join(lines)
    if len(summary) <= MAX_MEMORY_CHARS:
        return summary

    trimmed = []
    total = len("Earlier in this session:\n")
    for line in reversed(lines):
        if total + len(line) + 1 > MAX_MEMORY_CHARS:
            break
        trimmed.append(line)
        total += len(line) + 1

    trimmed.reverse()
    return "Earlier in this session:\n" + "\n".join(trimmed)


def build_retrieval_query(question: str, prior_chat: Sequence[dict]) -> str:
    question_clean = normalize_whitespace(question)
    question_tokens = tokenize_text(question_clean)
    if not prior_chat:
        return question_clean

    lowered = question_clean.lower()
    looks_like_followup = (
        len(question_tokens) <= 8
        or lowered.startswith(FOLLOWUP_PREFIXES)
        or any(tok in {"it", "they", "them", "that", "those", "this", "these"} for tok in question_tokens[:4])
    )
    if not looks_like_followup:
        return question_clean

    previous_user_turns = [msg["content"] for msg in prior_chat if msg.get("role") == "user" and msg.get("content")]
    if not previous_user_turns:
        return question_clean

    anchor = normalize_whitespace(previous_user_turns[-1])
    if not anchor:
        return question_clean
    return f"{anchor} {question_clean}"


def normalize_question_for_model(question: str) -> str:
    question = normalize_whitespace(question)
    question = re.sub(r"\bkill(?:ing)?\b", "control", question, flags=re.IGNORECASE)
    question = re.sub(r"\bget rid of\b", "control", question, flags=re.IGNORECASE)
    question = re.sub(r"\bwipe out\b", "control", question, flags=re.IGNORECASE)
    return question


def get_curated_fallback_matches(question: str) -> list[dict]:
    lowered = question.lower()
    matches = []
    for item in CURATED_FALLBACKS:
        if any(alias in lowered for alias in item["aliases"]):
            matches.append(item)
    return matches


def build_support_queries(question: str) -> list[tuple[str, str, float]]:
    support_queries = []
    for item in get_curated_fallback_matches(question):
        support_queries.extend(item["queries"])

    tokens = tokenize_text(question)
    has_control_intent = any(token in CONTROL_INTENT_TOKENS for token in tokens)
    has_pest_hint = any(token in PEST_HINT_TOKENS for token in tokens)
    if not has_control_intent or not has_pest_hint:
        return support_queries

    named_terms = [
        token
        for token in tokens
        if len(token) >= 4
        and token not in STOPWORDS
        and token not in CONTROL_INTENT_TOKENS
        and token not in PEST_HINT_TOKENS
    ]

    if named_terms:
        support_queries.append(
            (
                "control-backup",
                " ".join(
                    named_terms[:3]
                    + [
                        "pest",
                        "control",
                        "integrated",
                        "pest",
                        "management",
                        "crop",
                        "rotation",
                        "intercropping",
                    ]
                ),
                0.82,
            )
        )
    else:
        support_queries.append(
            (
                "control-backup",
                "insect pest control integrated pest management crop rotation intercropping pesticide",
                0.72,
            )
        )

    return support_queries


def build_guidance_notes(question: str) -> list[str]:
    notes = []
    for item in get_curated_fallback_matches(question):
        note = item.get("note")
        if note:
            notes.append(note)
    return notes


def merge_ranked_hits(weighted_hit_sets: Sequence[tuple[str, float, Sequence[tuple]]]):
    merged = defaultdict(
        lambda: {
            "score": 0.0,
            "text": None,
            "meta": None,
            "query_sources": set(),
        }
    )

    for label, weight, hits in weighted_hit_sets:
        for rank, (score, text, meta) in enumerate(hits):
            key = candidate_key(meta, text)
            weighted_score = max(0.0, score * weight - rank * 0.002)
            if weighted_score >= merged[key]["score"]:
                merged[key]["score"] = weighted_score
                merged[key]["text"] = text
                merged[key]["meta"] = dict(meta)
            merged[key]["query_sources"].add(label)

    out = []
    for item in merged.values():
        meta = dict(item["meta"] or {})
        meta["query_sources"] = sorted(item["query_sources"])
        out.append((item["score"], item["text"], meta))

    out.sort(key=lambda row: -row[0])
    return out


# ---------------- Chroma + BM25 ----------------
@st.cache_resource
def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)


@st.cache_resource
def get_chroma():
    return chromadb.PersistentClient(
        path=INDEX_DIR,
        settings=Settings(anonymized_telemetry=False),
    )


@st.cache_resource
def get_collection():
    client = get_chroma()
    return client.get_or_create_collection(COLLECTION, embedding_function=get_embedding_function())


@st.cache_resource
def load_bm25_corpus():
    path = os.path.join(INDEX_DIR, "docs.jsonl")
    if not os.path.exists(path):
        return None, None, None

    with open(path, "r", encoding="utf-8") as handle:
        blob = handle.read().strip()

    texts, metas = [], []
    decoder = json.JSONDecoder()
    idx, length = 0, len(blob)
    while idx < length:
        while idx < length and blob[idx].isspace():
            idx += 1
        if idx >= length:
            break
        obj, idx = decoder.raw_decode(blob, idx)
        texts.append(obj["text"])
        metas.append(obj["meta"])

    if not texts:
        return None, None, None

    tokenized = [tokenize_text(text) for text in texts]
    return BM25Okapi(tokenized), texts, metas


client = get_chroma()
coll = get_collection()
bm25, bm_texts, bm_metas = load_bm25_corpus()

if bm25 is None:
    st.warning("No index found. Run `python ingest.py` to rebuild the corpus index.")


def normalize_scores(items):
    if not items:
        return []
    values = [score for score, _, _ in items]
    lo, hi = min(values), max(values)
    width = (hi - lo) or 1.0
    return [((score - lo) / width, text, meta) for score, text, meta in items]


def candidate_key(meta: dict, text: str):
    return (meta.get("source"), meta.get("page"), text[:120])


def bm25_query(q: str, topk: int = 20, allowed_sources: Optional[Set[str]] = None):
    query_tokens = tokenize_text(q)
    if bm25 is None or not query_tokens:
        return []

    scores = bm25.get_scores(query_tokens)
    ranked = sorted(range(len(scores)), key=lambda ii: -scores[ii])

    out = []
    for idx in ranked:
        meta = bm_metas[idx]
        if allowed_sources and meta.get("source", "") not in allowed_sources:
            continue
        out.append((float(scores[idx]), bm_texts[idx], meta))
        if len(out) >= topk:
            break
    return out


def semantic_query(q: str, topk: int = 10, allowed_sources: Optional[Set[str]] = None):
    if not q:
        return []

    sample_size = max(topk * 3, topk)
    res = coll.query(query_texts=[q], n_results=sample_size)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    out = []
    for doc, meta, dist in zip(docs, metas, dists):
        if allowed_sources and meta.get("source", "") not in allowed_sources:
            continue
        out.append((1.0 - float(dist), doc, meta))
        if len(out) >= topk:
            break
    return out


def literal_query(q: str, topk: int = 20, allowed_sources: Optional[Set[str]] = None):
    if not q or not bm_texts:
        return []

    phrase = normalize_whitespace(q)
    phrase_rx = None
    if len(phrase) >= 5:
        phrase_rx = re.compile(re.escape(phrase), re.IGNORECASE)

    terms = []
    seen_terms = set()
    for token in tokenize_text(q):
        if len(token) < 3 or token in STOPWORDS or token in seen_terms:
            continue
        seen_terms.add(token)
        terms.append(token)

    if not phrase_rx and not terms:
        return []

    term_patterns = [
        (term, re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE))
        for term in terms[:12]
    ]

    rows = []
    for text, meta in zip(bm_texts, bm_metas):
        if allowed_sources and meta.get("source", "") not in allowed_sources:
            continue

        score = 0.0
        if phrase_rx:
            score += 4.0 * len(phrase_rx.findall(text))

        for term, pattern in term_patterns:
            hits = len(pattern.findall(text))
            if hits:
                score += min(hits, 4) * (1.0 + min(len(term), 10) / 10.0)

        if score > 0:
            rows.append((score, text, meta))

    rows.sort(key=lambda item: -item[0])
    return rows[:topk]


def hybrid_query(
    q: str,
    k_sem: int = 12,
    k_bm: int = 24,
    k_lit: int = 24,
    w_sem: float = 0.35,
    allowed_sources: Optional[Set[str]] = None,
):
    sem = semantic_query(q, k_sem, allowed_sources=allowed_sources)
    bm = bm25_query(q, k_bm, allowed_sources=allowed_sources)
    lit = literal_query(q, k_lit, allowed_sources=allowed_sources)

    sem_weight = max(0.0, min(1.0, w_sem))
    lexical_weight = 1.0 - sem_weight
    bm_weight = lexical_weight * 0.45
    lit_weight = lexical_weight * 0.55

    sem_norm = normalize_scores(sem)
    bm_norm = normalize_scores(bm)
    lit_norm = normalize_scores(lit)

    agg = defaultdict(
        lambda: {
            "sem": 0.0,
            "bm": 0.0,
            "lit": 0.0,
            "text": None,
            "meta": None,
            "signals": set(),
        }
    )

    for score, text, meta in sem_norm:
        key = candidate_key(meta, text)
        agg[key]["sem"] = max(agg[key]["sem"], score)
        agg[key]["text"] = text
        agg[key]["meta"] = meta
        agg[key]["signals"].add("semantic")

    for score, text, meta in bm_norm:
        key = candidate_key(meta, text)
        agg[key]["bm"] = max(agg[key]["bm"], score)
        if agg[key]["text"] is None:
            agg[key]["text"] = text
            agg[key]["meta"] = meta
        agg[key]["signals"].add("bm25")

    for score, text, meta in lit_norm:
        key = candidate_key(meta, text)
        agg[key]["lit"] = max(agg[key]["lit"], score)
        if agg[key]["text"] is None:
            agg[key]["text"] = text
            agg[key]["meta"] = meta
        agg[key]["signals"].add("literal")

    scored = []
    for item in agg.values():
        agreement_bonus = 0.0
        if item["bm"] > 0 and item["lit"] > 0:
            agreement_bonus += 0.08
        if item["sem"] > 0 and item["lit"] > 0:
            agreement_bonus += 0.04

        score = (
            sem_weight * item["sem"]
            + bm_weight * item["bm"]
            + lit_weight * item["lit"]
            + agreement_bonus
        )
        meta = dict(item["meta"] or {})
        meta["retrieval_signals"] = sorted(item["signals"])
        scored.append((score, item["text"], meta))

    scored.sort(key=lambda row: -row[0])
    return scored


def page_finder(q: str, topn: int = 5, w_sem: float = 0.35, allowed_sources: Optional[Set[str]] = None):
    hits = hybrid_query(q, k_sem=18, k_bm=50, k_lit=50, w_sem=w_sem, allowed_sources=allowed_sources)
    bucket = defaultdict(list)
    for score, text, meta in hits:
        bucket[(meta.get("source", ""), meta.get("page"), meta.get("section", ""))].append((score, text, meta))

    rows = []
    for (source, page, section), chunks in bucket.items():
        best = max(chunks, key=lambda item: item[0])
        snippet = best[1][:240].replace("\n", " ") + ("..." if len(best[1]) > 240 else "")
        rows.append(
            {
                "source": source,
                "page": page,
                "section": section,
                "score": round(best[0], 3),
                "signals": ", ".join(best[2].get("retrieval_signals", [])),
                "snippet": snippet,
            }
        )

    rows.sort(key=lambda row: -row["score"])
    return rows[:topn]


# ---------------- Non-LLM tools ----------------
def find_mentions(
    pattern: str,
    allowed_sources: Optional[Set[str]],
    whole_word: bool,
    case_sensitive: bool,
    use_regex: bool,
    topn: int = 50,
):
    if not pattern or not bm_texts:
        return []

    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pat = pattern if use_regex else re.escape(pattern)
        if whole_word and not use_regex:
            pat = r"\b" + pat + r"\b"
        rx = re.compile(pat, flags)
    except re.error as exc:
        return [
            {
                "source": "(error)",
                "page": None,
                "section": "",
                "matches": 0,
                "snippet": f"Invalid regex: {exc}",
            }
        ]

    rows = []
    for text, meta in zip(bm_texts, bm_metas):
        source = meta.get("source", "")
        if allowed_sources and source not in allowed_sources:
            continue

        matches = list(rx.finditer(text))
        if not matches:
            continue

        start = max(0, matches[0].start() - 120)
        end = min(len(text), matches[0].end() + 120)
        snippet = text[start:end].replace("\n", " ")
        rows.append(
            {
                "source": source,
                "page": meta.get("page"),
                "section": meta.get("section", ""),
                "matches": len(matches),
                "snippet": ("..." if start > 0 else "") + snippet + ("..." if end < len(text) else ""),
            }
        )

    rows.sort(key=lambda row: (-row["matches"], row["source"], (row["page"] or 0)))
    return rows[:topn]


def corpus_search(q: str, allowed_sources: Optional[Set[str]], topn: int = 15):
    hits = bm25_query(q, topn * 3, allowed_sources=allowed_sources)
    out = []
    for score, text, meta in hits:
        snippet = text[:240].replace("\n", " ") + ("..." if len(text) > 240 else "")
        out.append(
            {
                "score": round(score, 3),
                "source": meta.get("source", ""),
                "page": meta.get("page"),
                "section": meta.get("section", ""),
                "snippet": snippet,
            }
        )
        if len(out) >= topn:
            break
    return out


def build_chat_messages(
    question: str,
    context_blocks: Sequence[str],
    prior_chat: Sequence[dict],
    guidance_notes: Optional[Sequence[str]] = None,
) -> list[dict]:
    recent_chat = list(prior_chat[-RECENT_CHAT_MESSAGES:])
    memory_summary = build_memory_summary(prior_chat)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if memory_summary:
        messages.append({"role": "system", "content": memory_summary})
    if guidance_notes:
        messages.append({"role": "system", "content": "Question-specific guidance:\n- " + "\n- ".join(guidance_notes)})

    for msg in recent_chat:
        messages.append({"role": msg["role"], "content": msg["content"]})

    context_text = "\n\n".join(context_blocks)
    messages.append(
        {
            "role": "user",
            "content": (
                "CURRENT CONTEXT:\n"
                f"{context_text}\n\n"
                "CURRENT QUESTION:\n"
                f"{question}\n\n"
                "Answer now using only the current context. "
                "Use the conversation history only to resolve follow-up references."
            ),
        }
    )
    return messages


def format_http_error(exc: requests.HTTPError) -> str:
    response = exc.response
    if response is None:
        return str(exc)

    body = ""
    try:
        body = response.text.strip()
    except Exception:
        body = ""

    if body:
        return f"{exc} | {body[:400]}"
    return str(exc)


def stream_chat_completion(
    messages: Sequence[dict],
    model: str,
    api_base: str,
    temperature: float,
    reasoning_format: str = "deepseek",
) -> Iterable[str]:
    url = f"{api_base.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer no-key",
    }
    payload = {
        "model": model,
        "messages": list(messages),
        "stream": True,
        "temperature": temperature,
        "top_p": 0.9,
        "max_tokens": 320,
        "reasoning_format": reasoning_format,
        "chat_template_kwargs": {"enable_thinking": False},
    }

    with requests.post(
        url,
        headers=headers,
        json=payload,
        stream=True,
        timeout=REQUEST_TIMEOUT,
    ) as response:
        response.raise_for_status()
        response.encoding = "utf-8"

        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue

            line = raw_line.strip()
            if line.startswith("data:"):
                line = line[5:].lstrip()
            if line == "[DONE]":
                break

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            choices = obj.get("choices") or []
            if not choices:
                continue

            delta = choices[0].get("delta", {})
            token = delta.get("content")
            if token:
                cleaned = strip_model_control_tokens(token, trim=False)
                if cleaned:
                    yield cleaned


def fetch_chat_completion(
    messages: Sequence[dict],
    model: str,
    api_base: str,
    temperature: float,
    reasoning_format: str = "none",
) -> dict:
    url = f"{api_base.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer no-key",
    }
    payload = {
        "model": model,
        "messages": list(messages),
        "stream": False,
        "temperature": temperature,
        "top_p": 0.9,
        "max_tokens": 320,
        "reasoning_format": reasoning_format,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    response = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def extract_visible_answer(response_json: dict) -> str:
    choices = response_json.get("choices") or []
    if not choices:
        return ""

    message = choices[0].get("message", {}) or {}
    content = message.get("content") or ""
    if not content:
        return ""
    return normalize_llm_math(strip_model_control_tokens(content, trim=True))


# ---------------- Sidebar controls ----------------
with st.sidebar:
    st.markdown("### Tools")
    mode = st.radio("Mode", ["Chat", "Regex Mentions", "Corpus Search", "Page Finder"], horizontal=False)
    w_sem = st.slider("Semantic weight", 0.0, 1.0, 0.35, 0.05)
    topk = st.slider("Top-k context chunks", 3, 20, 8, 1)

    st.markdown("### LLM")
    api_base = st.text_input("API base", value=LLAMA_API_BASE)
    model_name = st.text_input("Model alias", value=LLM_MODEL)

    tone = st.selectbox("Answer tone", ["Strict", "Balanced", "Creative"], index=1)
    temp_map = {"Strict": 0.1, "Balanced": 0.25, "Creative": 0.45}
    temperature = temp_map[tone]

    if st.button("Clear chat"):
        st.session_state.chat = []
        st.rerun()

    st.caption("Chat mode automatically blends semantic, BM25, and literal/regex-style retrieval.")

    st.markdown("### Mode options")
    if mode == "Regex Mentions":
        whole_word = st.checkbox("Whole word", value=True)
        case_sensitive = st.checkbox("Case sensitive", value=False)
        use_regex = st.checkbox("Use regex (advanced)", value=False)
    elif mode == "Corpus Search":
        topn_search = st.slider("Top-N results", 5, 50, 25, 1)


# ---------------- Reference pool ----------------
core_sources: Set[str] = set()
optional_sources: Set[str] = set()

for meta in (bm_metas or []):
    if meta.get("type") != "pdf":
        continue
    source = meta.get("source", "")
    if not source:
        continue
    if meta.get("tier", "core") == "optional":
        optional_sources.add(source)
    else:
        core_sources.add(source)

core_sources_sorted = sorted(core_sources)
optional_sources_sorted = sorted(optional_sources)

with st.sidebar:
    st.markdown("### Reference pool")
    st.markdown(f"Core ({len(core_sources_sorted)} documents)")
    include_optional = st.checkbox(f"Optional ({len(optional_sources_sorted)} documents)", value=True)


def current_allowed_sources() -> Optional[Set[str]]:
    allowed: Set[str] = set(core_sources_sorted)
    if include_optional:
        allowed |= set(optional_sources_sorted)
    return allowed or None


# ---------------- Main UI ----------------
if mode == "Chat":
    for msg in st.session_state.chat[-12:]:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    q = st.chat_input("Ask a question about the corpus...")
    go = bool(q)
else:
    q = st.text_input("Query")
    go = st.button("Go")

if go and q:
    allowed = current_allowed_sources()

    if mode == "Regex Mentions":
        rows = find_mentions(
            q,
            allowed_sources=allowed,
            whole_word=whole_word,
            case_sensitive=case_sensitive,
            use_regex=use_regex,
            topn=100,
        )
        st.subheader(f'Occurrences of "{q}"')
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    elif mode == "Corpus Search":
        rows = corpus_search(q, allowed_sources=allowed, topn=topn_search)
        st.subheader("Top matches (BM25, corpus-only)")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    elif mode == "Page Finder":
        rows = page_finder(q, topn=8, w_sem=w_sem, allowed_sources=allowed)
        st.subheader("Likely relevant pages")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    else:
        prior_chat = list(st.session_state.chat)
        llm_question = normalize_question_for_model(q)
        retrieval_query = build_retrieval_query(llm_question, prior_chat)
        support_queries = build_support_queries(llm_question)
        guidance_notes = build_guidance_notes(llm_question)

        st.session_state.chat.append({"role": "user", "content": q})
        with st.chat_message("user"):
            st.markdown(q)

        primary_hits = hybrid_query(
            retrieval_query,
            k_sem=24,
            k_bm=80,
            k_lit=80,
            w_sem=w_sem,
            allowed_sources=allowed,
        )
        weighted_hit_sets = [("primary", 1.0, primary_hits)]
        for label, support_query, weight in support_queries:
            weighted_hit_sets.append(
                (
                    label,
                    weight,
                    hybrid_query(
                        support_query,
                        k_sem=16,
                        k_bm=50,
                        k_lit=50,
                        w_sem=min(w_sem, 0.3),
                        allowed_sources=allowed,
                    ),
                )
            )

        hits = merge_ranked_hits(weighted_hit_sets)[:topk]

        if not hits:
            with st.chat_message("assistant"):
                st.warning("No context found. Try widening your source selection or switching modes.")
            st.session_state.chat.append({"role": "assistant", "content": "No context found."})
        else:
            context_blocks = []
            citations = []
            for idx, (_, text, meta) in enumerate(hits, start=1):
                source = meta.get("source", "")
                page = meta.get("page", "?")
                tier = meta.get("tier", "core")
                signals = ", ".join(meta.get("retrieval_signals", []))
                query_sources = ", ".join(meta.get("query_sources", []))
                citations.append(f"[{idx}] ({tier}; {signals}; {query_sources}) {source} p{page}")
                context_blocks.append(f"[{idx}] ({tier}) ({source} p{page}) {shorten_context_chunk(text)}")

            messages = build_chat_messages(llm_question, context_blocks, prior_chat, guidance_notes=guidance_notes)

            with st.chat_message("assistant"):
                stream_target = st.empty()

                st.session_state.chat.append({"role": "assistant", "content": ""})
                assistant_idx = len(st.session_state.chat) - 1

                try:
                    def token_stream():
                        chunks = []
                        for token in stream_chat_completion(messages, model_name, api_base, temperature):
                            chunks.append(token)
                            st.session_state.chat[assistant_idx]["content"] = "".join(chunks)
                            yield token

                    raw_answer = stream_target.write_stream(token_stream())
                    final_answer = normalize_llm_math(strip_model_control_tokens(raw_answer or "", trim=True))
                    if len(final_answer.strip()) < 24:
                        fallback_json = fetch_chat_completion(
                            messages,
                            model_name,
                            api_base,
                            temperature,
                            reasoning_format="none",
                        )
                        fallback_answer = extract_visible_answer(fallback_json)
                        if fallback_answer:
                            final_answer = fallback_answer
                    st.session_state.chat[assistant_idx]["content"] = final_answer
                    if final_answer != (raw_answer or ""):
                        stream_target.markdown(final_answer)

                except requests.HTTPError as exc:
                    error = f"(LLM error: {format_http_error(exc)})"
                    st.session_state.chat[assistant_idx]["content"] = error
                    stream_target.write(error)

                except Exception as exc:
                    error = f"(LLM error: {exc})"
                    st.session_state.chat[assistant_idx]["content"] = error
                    stream_target.write(error)

                with st.expander("Context, Citations, and Memory"):
                    st.markdown(f"**Primary retrieval query:** `{retrieval_query}`")
                    if llm_question != q:
                        st.markdown(f"**Model-facing question:** `{llm_question}`")
                    if support_queries:
                        st.markdown("**Support retrieval queries**")
                        for label, support_query, weight in support_queries:
                            st.markdown(f"- `{label}` ({weight:.2f}): `{support_query}`")
                    if guidance_notes:
                        st.markdown("**Guidance notes**")
                        for note in guidance_notes:
                            st.markdown(f"- {note}")
                    memory_summary = build_memory_summary(prior_chat)
                    if memory_summary:
                        st.markdown("**Session memory**")
                        st.text(memory_summary)
                    st.markdown("**Citation keys**")
                    st.markdown("\n".join(citations))
                    for idx, (score, text, meta) in enumerate(hits, start=1):
                        signals = ", ".join(meta.get("retrieval_signals", []))
                        query_sources = ", ".join(meta.get("query_sources", []))
                        st.markdown(
                            f"**[{idx}]** ({meta.get('tier', 'core')}; {signals}; {query_sources}) "
                            f"{meta.get('source')} p{meta.get('page', '?')} - score {score:.3f}"
                        )
                        st.write(text[:1200] + ("..." if len(text) > 1200 else ""))
