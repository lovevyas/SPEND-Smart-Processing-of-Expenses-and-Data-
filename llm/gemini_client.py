import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_financial_text(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    return response.text

def extract_json_from_llm(text: str) -> str:
    """
    Safely extract JSON object from LLM output.
    Handles ```json fences and extra text.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in LLM output")

    return text[start:end + 1]