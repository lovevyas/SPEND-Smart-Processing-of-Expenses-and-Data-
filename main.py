import json
import pytesseract
import time
from ocr.image_utils import preprocess_image
from llm.prompt import build_spend_prompt
from llm.gemini_client import parse_financial_text, extract_json_from_llm
from core.normalizer import normalize_transaction
from core.confidence import calculate_confidence
from storage.db import init_db, insert_transaction
from google.genai.errors import ClientError


# -----------------------------
# Global config
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
)

OCR_CONFIG = (
    r"--oem 3 "
    r"--psm 4 "
    r"-c preserve_interword_spaces=1 "
)

# Initialize DB once
init_db()


# -----------------------------
# Core processing function
# -----------------------------
def process_image(image_path: str) -> dict:
    # OCR
    img = preprocess_image(image_path)
    text = pytesseract.image_to_string(img, config=OCR_CONFIG)

    prompt = build_spend_prompt(text)

    # ---- Gemini with rate-limit handling ----
    try:
        llm_output = parse_financial_text(prompt)
    except ClientError as e:
        if e.code == 429:
            # Respect free-tier limits
            time.sleep(8)
            llm_output = parse_financial_text(prompt)
        else:
            raise

    parsed = json.loads(extract_json_from_llm(llm_output))

    transaction = normalize_transaction(parsed)
    transaction["confidence"] = calculate_confidence(transaction, text)

    insert_transaction(transaction)
    return transaction


# -----------------------------
# Optional: local test run
# -----------------------------
if __name__ == "__main__":
    test_image = "data/samples/offline_bill.jpg"

    txn = process_image(test_image)

    print("=== TRANSACTION SAVED ===")
    print(txn)
