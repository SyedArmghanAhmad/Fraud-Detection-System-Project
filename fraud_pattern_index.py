from llama_index.core import Document  # Add this import
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
import pandas as pd

# Load aligned fraud patterns
fraud_patterns = pd.read_csv("models/aligned_fraud_patterns.csv")

# Create structured documents using LlamaIndex Document objects
documents = []
for _, row in fraud_patterns.iterrows():
    text = f"""
    **Pattern Type**: {row['fraud_type']}
    **Feature**: {row['feature']}
    **Condition**: {row['condition']}
    **Risk Level**: {row['risk_level']}
    **Description**: {row['description']}
    """
    # Create Document instance instead of dict
    documents.append(Document(
        text=text,
        metadata=row.to_dict(),
        excluded_llm_metadata_keys=["feature", "condition"]  # Optional: exclude technical fields
    ))

# Build and save index
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    show_progress=True
)
index.storage_context.persist(persist_dir="data/fraud_patterns_index")
print("✅ Fraud pattern index updated successfully!")