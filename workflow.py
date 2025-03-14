from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional, Annotated
from fraud_detector import FraudDetector
from llm_chain import process_transaction
import json

# Initialize components
detector = FraudDetector()

# Define state schema
class FraudCheckState(TypedDict):
    transaction: dict
    fraud_result: Optional[dict]
    patterns: Optional[List[dict]]
    explanation: Optional[str]
    error: Optional[bool]  # Add an error field to the state

# Define nodes
def detect_fraud(state: FraudCheckState) -> FraudCheckState:
    try:
        fraud_result = detector.predict(state["transaction"])
        return {
            **state,
            "fraud_result": fraud_result,
            "error": False
        }
    except Exception as e:
        return {
            **state,
            "error": True
        }

def retrieve_patterns(state: FraudCheckState) -> FraudCheckState:
    try:
        patterns = detector.get_relevant_patterns(state["transaction"])
        return {
            **state,
            "patterns": patterns,
            "error": False
        }
    except Exception as e:
        return {
            **state,
            "error": True
        }

def generate_explanation(state: FraudCheckState) -> FraudCheckState:
    try:
        explanation = process_transaction(
            state["transaction"],
            state["fraud_result"],
            state["patterns"]
        )
        return {
            **state,
            "explanation": explanation,
            "error": False
        }
    except Exception as e:
        return {
            **state,
            "error": True
        }

def handle_error(state: FraudCheckState) -> FraudCheckState:
    return {
        **state,
        "explanation": "Error: Failed to process transaction"
    }

# Build workflow
workflow = StateGraph(FraudCheckState)

# Add nodes
workflow.add_node("detect_fraud", detect_fraud)
workflow.add_node("retrieve_patterns", retrieve_patterns)
workflow.add_node("generate_explanation", generate_explanation)
workflow.add_node("handle_error", handle_error)

# Define edges
workflow.add_edge("detect_fraud", "retrieve_patterns")
workflow.add_edge("retrieve_patterns", "generate_explanation")
workflow.add_edge("generate_explanation", END)

# Add conditional edges for error handling
def decide_next_node(state: FraudCheckState):
    if state.get("error"):
        return "handle_error"
    else:
        return END

workflow.add_conditional_edges("detect_fraud", decide_next_node)
workflow.add_conditional_edges("retrieve_patterns", decide_next_node)
workflow.add_conditional_edges("generate_explanation", decide_next_node)

# Set the entry point
workflow.set_entry_point("detect_fraud")

# Compile
fraud_workflow = workflow.compile()