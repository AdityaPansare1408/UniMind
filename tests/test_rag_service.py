from src.services.rag_service import RAGService


def main():
    rag = RAGService()

    question = input("Ask a question: ")

    result = rag.ask(question)

    print("\nAnswer:\n")
    print(result.answer)

    print("\nRetrieved Documents:", len(result.documents))


if __name__ == "__main__":
    main()