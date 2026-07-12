from rag_langgraph import app

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
