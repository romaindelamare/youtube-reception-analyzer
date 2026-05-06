from langchain_core.prompts import ChatPromptTemplate

from state import AnalysisState
from schemas.analysis import BatchAnalysis
from services.mistral_service import build_mistral_llm

BATCH_SIZE = 50

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a YouTube comment analyst. Your job is to evaluate how viewers received the VIDEO ITSELF — "
        "not the subject matter or topic being discussed in the video.\n\n"
        "Focus EXCLUSIVELY on the CREATOR'S CHOICES and PRESENTATION:\n"
        "- The creator's explanation style, clarity, and teaching ability\n"
        "- How the creator chose to present, structure, or organize the content\n"
        "- Video production quality (editing, pacing, tone, humor level, length, audio)\n"
        "- The creator's tone, authenticity, enthusiasm, credibility, or personality\n"
        "- Sponsorships, ads, or monetization methods in the video\n"
        "- Whether the creator was engaging, boring, confusing, or misleading in their delivery\n"
        "- Production issues or suggestions for improvement\n"
        "- How well the creator explained or covered the topic\n\n"
        "EXPLICITLY IGNORE AND EXCLUDE:\n"
        "- Factual accuracy or debate about the subject itself\n"
        "- What's missing or overlooked in the actual subject matter or reality\n"
        "- Viewer's own expert knowledge or opinions about the topic\n"
        "- Philosophical disagreements with the subject\n"
        "- Only count factual corrections if criticizing HOW the creator presented it, not the facts themselves\n\n"
        "Return a JSON object with:\n"
        "- sentiments: list of 'positive', 'neutral', or 'negative' — one per comment, in order, "
        "based on how the viewer feels about the VIDEO/CREATOR (not the topic)\n"
        "- complaints: list of distinct recurring criticisms about the video or creator (max 10, deduplicated)\n"
        "- highlights: list of distinct recurring positives about the video or creator (max 10, deduplicated)\n"
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
