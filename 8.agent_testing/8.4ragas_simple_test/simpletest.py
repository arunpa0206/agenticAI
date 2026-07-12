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
from ragas.metrics import faithfulness, answer_relevancy

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

# Sample data
dataset = Dataset.from_dict(
    {
        "question": [
            "What is the capital of France?"
        ],
        "answer": [
            "The capital of France is Paris."
        ],
        "contexts": [[
            "France is a country in Europe. Its capital is Paris."
        ]],
        "ground_truth": [
            "Paris"
        ],
    }
)

result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
    ],
    llm=ragas_llm,
    embeddings=ragas_embeddings,
)

print(result)