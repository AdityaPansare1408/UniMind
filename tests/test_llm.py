from src.llm.gemini_llm import GeminiLLM

llm = GeminiLLM()

response = llm.invoke("Say hello.")

print(response)