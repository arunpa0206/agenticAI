import os
import sys
import types
from datasets import Dataset
from dotenv import load_dotenv

# Stub for missing vertexai module in newer langchain-community versions
try:
    import langchain_community.chat_models.vertexai
except ModuleNotFoundError:
    stub = types.ModuleType("langchain_community.chat_models.vertexai")
    stub.ChatVertexAI = type("ChatVertexAI", (object,), {})
    sys.modules["langchain_community.chat_models.vertexai"] = stub

from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings

from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# Load Anthropic API key from workspace root .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Claude LLM
llm = ChatAnthropic(
    model="claude-sonnet-5",
    temperature=None
)

ragas_llm = LangchainLLMWrapper(llm, bypass_temperature=True)

# Local embedding model (downloads automatically the first time)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

ragas_embeddings = LangchainEmbeddingsWrapper(embedding_model)

# Sample evaluation dataset
data = {
    "question": [
        "How many vacation days do employees receive each year?",
        "What should an employee do if they forget their password?",
        "When is technical support available?",
        "Can employees work remotely?"
    ],

    "answer": [
        "Employees receive 20 days of paid annual leave.",
        "Employees should reset their password using the self-service portal.",
        "Technical support is available Monday through Friday from 9 AM to 6 PM.",
        "Employees may work remotely up to three days per week."
    ],

    "contexts": [
        [
            "The company provides employees with 20 days of paid annual leave each calendar year."
        ],
        [
            "If an employee forgets their password, they should use the self-service password reset portal."
        ],
        [
            "IT support operates Monday through Friday between 9:00 AM and 6:00 PM."
        ],
        [
            "The hybrid work policy allows employees to work remotely for up to three days each week."
        ]
    ],

    "ground_truth": [
        "20 days of paid annual leave",
        "Use the self-service password reset portal",
        "Monday through Friday, 9 AM to 6 PM",
        "Employees may work remotely up to three days per week"
    ]
}

# Create Dataset
dataset = Dataset.from_dict(data)

# Evaluate using RAGAS
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
    llm=ragas_llm,
    embeddings=ragas_embeddings,
)

# Print Results
print("\n========== RAGAS Evaluation Results ==========\n")

for metric, score in result._repr_dict.items():
    print(f"{metric:<20}: {score:.3f}")