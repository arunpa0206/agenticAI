# RAGAS Evaluation Metrics

## Faithfulness
Measures whether the generated answer is fully supported by the retrieved context. A high faithfulness score indicates that the answer is grounded in the provided documents and does not contain unsupported or hallucinated information.

## Answer Relevancy
Measures how well the generated answer addresses the user's question. A high answer relevancy score indicates that the response is directly relevant to the query and provides the requested information.

## Context Precision
Measures how relevant the retrieved documents are to the user's query. A high context precision score indicates that the retriever returned mostly useful and relevant documents while minimizing irrelevant information.

## Context Recall
Measures whether the retriever fetched all the information required to answer the user's question. A high context recall score indicates that the retrieved context contains all the necessary information needed to generate a complete answer.
```