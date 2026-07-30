from src.rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "What is the salary offered?"
)

print(f"\nRetrieved {len(results)} documents\n")

for i, doc in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print("=" * 60)

    print(doc.page_content[:500])

    print("\nMetadata:")
    print(doc.metadata)
    print()