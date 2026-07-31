from langchain_google_genai import ChatGoogleGenerativeAI

from src.config.settings import (
    GOOGLE_API_KEY,
    GOOGLE_CHAT_MODELS,
)


class GeminiLLM:
    """
    Wrapper around Gemini chat models.

    Features:
    - Multiple fallback models
    - Returns plain text
    - Easy to extend with retries/logging later
    """

    def __init__(self, temperature: float = 0.3):

        self.models = [
            (
                model_name,
                ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=GOOGLE_API_KEY,
                    temperature=temperature,
                ),
            )
            for model_name in GOOGLE_CHAT_MODELS
        ]

    def invoke(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini.

        Tries each configured model until one succeeds.
        Returns only the generated text.
        """

        last_error = None

        for model_name, model in self.models:

            try:
                response = model.invoke(prompt)

                content = response.content

                # Newer LangChain versions may return a string
                if isinstance(content, str):
                    return content.strip()

                # Some versions return a list of content blocks
                if isinstance(content, list):

                    text = ""

                    for block in content:

                        if isinstance(block, dict):
                            text += block.get("text", "")

                        elif hasattr(block, "text"):
                            text += block.text

                    return text.strip()

                # Fallback
                return str(content)

            except Exception as e:

                print(f"{model_name} failed: {e}")

                last_error = e

        raise RuntimeError(
            "All configured Gemini models failed."
        ) from last_error