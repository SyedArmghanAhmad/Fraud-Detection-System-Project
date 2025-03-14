from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# Prompt for regular explanations
prompt_template = PromptTemplate(
    input_variables=["transaction", "fraud_result", "patterns"],
    template="""
    **Role**: You are a senior fraud analyst at a major bank. Analyze this transaction.

    **Chain-of-Thought Instructions**:
    1. Start by identifying key transaction features (e.g., V2=3.5).
    2. Compare against these fraud patterns (ordered by relevance):
    {patterns}
    3. Explain why patterns do/don't apply using banking regulations.
    4. Qualify confidence using Basel III risk categories.

    **Transaction**: {transaction}

    **Model Prediction**: {fraud_result}

    **Examples**:
    - Good Analysis: "While V2 exceeds 3.0 (pattern: high-velocity fraud), the lack of corroborating evidence in V4/V17 suggests this might be a false positive."
    - Bad Analysis: "It's fraud because the model said so."

    **Your Analysis**:
    """
)

# Prompt for borderline cases
borderline_prompt_template = PromptTemplate(
    input_variables=["transaction", "fraud_result", "patterns"],
    template="""
    **Role**: You are a senior fraud analyst at a major bank. This transaction is borderline, and the model is unsure. Analyze it carefully.

    **Chain-of-Thought Instructions**:
    1. Start by identifying key transaction features (e.g., V2=3.5).
    2. Compare against these fraud patterns (ordered by relevance):
    {patterns}
    3. Explain why patterns do/don't apply using banking regulations.
    4. Qualify confidence using Basel III risk categories.
    5. Make a final judgment: Is this transaction fraudulent or legitimate?

    **Transaction**: {transaction}

    **Model Prediction**: {fraud_result}

    **Examples**:
    - Good Analysis: "While V2 exceeds 3.0 (pattern: high-velocity fraud), the lack of corroborating evidence in V4/V17 suggests this might be a false positive."
    - Bad Analysis: "It's fraud because the model said so."

    **Your Analysis**:
    """
)

def process_transaction(transaction, fraud_result, patterns, is_borderline=False):
    # Format patterns for the prompt
    formatted_patterns = "\n".join([
        f"- {p['feature']} {p['condition']}: {p['description']}"
        for p in patterns
    ])
    
    # Choose the appropriate prompt
    if is_borderline:
        prompt = borderline_prompt_template.format(
            transaction=transaction,
            fraud_result=fraud_result,
            patterns=formatted_patterns
        )
    else:
        prompt = prompt_template.format(
            transaction=transaction,
            fraud_result=fraud_result,
            patterns=formatted_patterns
        )
    
    # Invoke the LLM
    return llm.invoke(prompt).content