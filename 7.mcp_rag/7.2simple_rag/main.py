from rag import retriever, llm

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
