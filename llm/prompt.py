def build_spend_prompt(ocr_text: str) -> str:
    return f"""
You are a financial document parser.

Your task:
- Analyze the OCR text below
- Extract structured financial information
- Output ONLY valid JSON
- Do NOT add explanations or extra text

Rules:
- If a field is missing, use null
- Amount must be a number (no currency symbols)
- Dates should be in YYYY-MM-DD format if possible
- Items should be an empty list if not applicable
- Include UPI_wallet only if it is a UPI transaction.
- UPI_wallet should only be name of UPI app used only.

Supported document types:
- RECEIPT
- UPI_PAYMENT
- BANK_MESSAGE

JSON schema (STRICT):
{{
  "document_type": "RECEIPT | UPI_PAYMENT | BANK_MESSAGE",
  "UPI_wallet": string | null
  "merchant": string | null,
  "amount": number | null,
  "currency": string | null,
  "payment_method": string | null,
  "source_account": string | null,
  "items": [
    {{
      "name": string,
      "price": number
    }}
  ],
  "date": string | null,
  "time": string | null,
  "confidence": number
}}

OCR TEXT:
\"\"\"
{ocr_text}
\"\"\"
"""
