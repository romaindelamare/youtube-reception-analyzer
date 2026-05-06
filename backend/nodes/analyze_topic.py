from langchain_core.prompts import ChatPromptTemplate

from state import AnalysisState
from schemas.analysis import BatchAnalysis
from services.mistral_service import build_mistral_llm

BATCH_SIZE = 50

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a topic analyst. Your job is to analyze viewer opinions about the SUBJECT/TOPIC being discussed in the video, "
        "NOT about the video itself or the creator.\n\n"
        "Focus exclusively on:\n"
        "- Opinions about the subject matter (e.g., AI, machine learning, a technology, product, etc.)\n"
        "- Viewer concerns, criticism, or praise directed at the topic itself\n"
        "- How viewers feel about the broader subject, not the presentation\n\n"
        "Ignore or deprioritize:\n"
        "- Comments about video quality, creator style, or explanation clarity\n"
        "- Technical feedback about the video production\n"
        "- Only count production feedback if it relates to understanding the topic\n\n"
        "Return a JSON object with:\n"
        "- sentiments: list of 'positive', 'neutral', or 'negative' — one per comment, in order, "
        "based on how the viewer feels about the TOPIC/SUBJECT (not the video)\n"
        "- complaints: list of distinct recurring criticisms about the topic itself (max 10, deduplicated)\n"
        "- highlights: list of distinct recurring positives about the topic itself (max 10, deduplicated)\n"
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


def analyze_topic(state: AnalysisState) -> dict:
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
        "topic_sentiment": sentiment,
        "topic_complaints": dedupe(all_complaints)[:10],
        "topic_highlights": dedupe(all_highlights)[:10],
    }
