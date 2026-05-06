from langgraph.graph import StateGraph, START, END

from state import AnalysisState
from nodes.scrape_comments import scrape_comments
from nodes.analyze_comments import analyze_comments
from nodes.analyze_topic import analyze_topic
from nodes.generate_report import generate_report
from nodes.generate_topic_report import generate_topic_report


def build_graph():
    builder = StateGraph(AnalysisState)

    builder.add_node("scrape_comments", scrape_comments)
    builder.add_node("analyze_comments", analyze_comments)
    builder.add_node("analyze_topic", analyze_topic)
    builder.add_node("generate_report", generate_report)
    builder.add_node("generate_topic_report", generate_topic_report)

    builder.add_edge(START, "scrape_comments")
    builder.add_edge("scrape_comments", "analyze_comments")
    builder.add_edge("scrape_comments", "analyze_topic")
    builder.add_edge("analyze_comments", "generate_report")
    builder.add_edge("analyze_topic", "generate_topic_report")
    builder.add_edge("generate_report", END)
    builder.add_edge("generate_topic_report", END)

    return builder.compile()


graph = build_graph()
