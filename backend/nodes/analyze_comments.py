from langchain_core.prompts import ChatPromptTemplate

from state import AnalysisState
from schemas.analysis import BatchAnalysis
from services.mistral_service import build_mistral_llm

BATCH_SIZE = 50

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a YouTube comment analyst. "
        "Given a list of comments, return a JSON object with:\n"
        "- sentiments: list of 'positive', 'neutral', or 'negative' — one per comment, in order\n"
        "- complaints: list of distinct recurring issues or criticisms (max 10, deduplicated)\n"
        "- highlights: list of distinct recurring positives praised (max 10, deduplicated)\n"
        "Return only valid JSON matching the schema, nothing else."
    )),
    ("human", "Comments:\n{comments_text}"),
])


def _format_comments(comments: list[dict]) -> str:
    lines = []
    for i, c in enumerate(comments, 1):
        text = c.get("text") or c.get("comment") or ""
        if text.strip():
            lines.append(f"{i}. {text.strip()}")
    return "\n".join(lines)


def analyze_comments(state: AnalysisState) -> dict:
    comments = state["comments"]
    llm = build_mistral_llm()
    structured_llm = llm.with_structured_output(BatchAnalysis)
    chain = PROMPT | structured_llm

    all_sentiments: list[str] = []
    all_complaints: list[str] = []
    all_highlights: list[str] = []

    for i in range(0, len(comments), BATCH_SIZE):
        batch = comments[i : i + BATCH_SIZE]
        comments_text = _format_comments(batch)
        if not comments_text.strip():
            continue
        result: BatchAnalysis = chain.invoke({"comments_text": comments_text})
        all_sentiments.extend(result.sentiments)
        all_complaints.extend(result.complaints)
        all_highlights.extend(result.highlights)

    total = len(all_sentiments) or 1
    sentiment = {
        "positive": round(all_sentiments.count("positive") / total * 100, 1),
        "neutral": round(all_sentiments.count("neutral") / total * 100, 1),
        "negative": round(all_sentiments.count("negative") / total * 100, 1),
    }

    # Deduplicate while preserving order
    def dedupe(items: list[str]) -> list[str]:
        seen: set[str] = set()
        result = []
        for item in items:
            key = item.lower().strip()
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    return {
        "sentiment": sentiment,
        "complaints": dedupe(all_complaints)[:10],
        "highlights": dedupe(all_highlights)[:10],
    }
