from langchain_core.prompts import ChatPromptTemplate

from state import AnalysisState
from schemas.analysis import ReportOutput
from services.mistral_service import build_mistral_llm

PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a topic sentiment analyst. "
        "Based on the provided sentiment data, complaints, and highlights, write a concise 2-3 sentence "
        "summary of what viewers think about the SUBJECT/TOPIC of the video (not the video itself). "
        "Classify the overall sentiment as 'Positive', 'Mixed', or 'Negative'.\n"
        "Return JSON with fields: summary (string), reception_label ('Positive'|'Mixed'|'Negative')."
    )),
    ("human", (
        "Sentiment breakdown about the topic:\n"
        "  Positive: {positive}%\n"
        "  Neutral: {neutral}%\n"
        "  Negative: {negative}%\n\n"
        "Top complaints about the topic:\n{complaints}\n\n"
        "Top highlights about the topic:\n{highlights}"
    )),
])


def generate_topic_report(state: AnalysisState) -> dict:
    llm = build_mistral_llm()
    structured_llm = llm.with_structured_output(ReportOutput)
    chain = PROMPT | structured_llm

    sentiment = state["topic_sentiment"]
    complaints_text = "\n".join(f"- {c}" for c in state["topic_complaints"]) or "None"
    highlights_text = "\n".join(f"- {h}" for h in state["topic_highlights"]) or "None"

    result: ReportOutput = chain.invoke({
        "positive": sentiment["positive"],
        "neutral": sentiment["neutral"],
        "negative": sentiment["negative"],
        "complaints": complaints_text,
        "highlights": highlights_text,
    })

    return {
        "topic_summary": result.summary,
        "topic_reception_label": result.reception_label,
    }
