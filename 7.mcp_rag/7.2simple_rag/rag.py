from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic

load_dotenv()

# -----------------------------
# Load the document
# -----------------------------
loader = TextLoader("data.txt")
documents = loader.load()

# -----------------------------
# Split into chunks
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# -----------------------------
# Create embeddings
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Create FAISS Vector Store
# -----------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)

# -----------------------------
# Create Retriever
# -----------------------------
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -----------------------------
# Claude LLM
# -----------------------------
llm = ChatAnthropic(
    model="claude-sonnet-5"
)

if __name__ == "__main__":
    print("===== Simple RAG Chatbot =====")

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        # Retrieve relevant documents
        docs = retriever.invoke(question)

        # Build context
        context = "\n".join(doc.page_content for doc in docs)

        # Prompt Claude
        prompt = f"""
You are a document question-answering assistant.

Answer ONLY using the context below.

If the answer is not found in the context, reply exactly:

I couldn't find that information in the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        print("\nAnswer:")
        print(response.content)