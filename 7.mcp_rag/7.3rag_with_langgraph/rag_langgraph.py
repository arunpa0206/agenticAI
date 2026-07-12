from typing import TypedDict

from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic

load_dotenv()

# -------------------------------------------------------
# Load document
# -------------------------------------------------------

loader = TextLoader("data.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# -------------------------------------------------------
# Embeddings
# -------------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(chunks, embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -------------------------------------------------------
# Claude
# -------------------------------------------------------

llm = ChatAnthropic(
    model="claude-sonnet-5"
)

# -------------------------------------------------------
# Graph State
# -------------------------------------------------------

class GraphState(TypedDict):
    question: str
    context: str
    answer: str

# -------------------------------------------------------
# Node 1 - Retrieve
# -------------------------------------------------------

def retrieve(state: GraphState):

    docs = retriever.invoke(state["question"])

    context = "\n".join(doc.page_content for doc in docs)

    return {
        "context": context
    }

# -------------------------------------------------------
# Node 2 - Generate
# -------------------------------------------------------

def generate(state: GraphState):

    prompt = f"""
You are a document question answering assistant.

Answer ONLY using the context below.

If the answer is not in the context, reply exactly:

I couldn't find that information in the provided documents.

Context:
{state["context"]}

Question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }

# -------------------------------------------------------
# Build Graph
# -------------------------------------------------------

graph = StateGraph(GraphState)

graph.add_node("Retrieve", retrieve)
graph.add_node("Generate", generate)

graph.set_entry_point("Retrieve")

graph.add_edge("Retrieve", "Generate")
graph.add_edge("Generate", END)

app = graph.compile()

# -------------------------------------------------------
# Chat Loop
# -------------------------------------------------------

if __name__ == "__main__":
    print("===== LangGraph RAG Chatbot =====")

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        result = app.invoke(
            {
                "question": question
            }
        )

        print("\nAnswer:")
        print(result["answer"])