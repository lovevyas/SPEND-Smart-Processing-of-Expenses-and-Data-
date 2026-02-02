def calculate_confidence(transaction: dict, ocr_text: str) -> float:
    """
    Combine LLM confidence with system-level validation.
    """

    score = transaction.get("confidence", 0.0)

    # 1️⃣ Required fields check
    required_fields = ["amount", "merchant", "date"]
    for field in required_fields:
        if not transaction.get(field):
            score -= 0.2

    # 2️⃣ OCR quality heuristic
    if len(ocr_text.strip()) < 50:
        score -= 0.1

    # Clamp between 0 and 1
    score = max(0.0, min(1.0, score))

    return round(score, 2)
