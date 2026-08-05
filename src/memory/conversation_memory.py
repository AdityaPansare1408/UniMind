from collections import deque


class ConversationMemory:
    """
    Stores the most recent conversation exchanges.

    The memory is intentionally small to avoid
    sending excessively long prompts to the LLM.
    """

    def __init__(
        self,
        max_history: int = 5,
    ):

        self.history = deque(maxlen=max_history)

    # --------------------------------------------------
    # Add Exchange
    # --------------------------------------------------

    def add_exchange(
        self,
        question: str,
        answer: str,
    ) -> None:

        self.history.append(
            {
                "question": question,
                "answer": answer,
            }
        )

    # --------------------------------------------------
    # Get History
    # --------------------------------------------------

    def get_history(self):

        return list(self.history)

    # --------------------------------------------------
    # Build Prompt History
    # --------------------------------------------------

    def build_history(self) -> str:

        if not self.history:
            return ""

        parts = []

        for exchange in self.history:

            parts.append(
                f"""User:
{exchange["question"]}

Assistant:
{exchange["answer"]}
"""
            )

        return "\n".join(parts)

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear(self):

        self.history.clear()