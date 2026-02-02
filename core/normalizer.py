def normalize_transaction(raw: dict) -> dict:
    """
    Normalize Gemini output into SPEND's final transaction schema.
    """

    normalized = {
        "document_type": raw.get("document_type"),
        "merchant": raw.get("merchant"),
        "amount": raw.get("amount"),
        "currency": raw.get("currency"),
        "payment_method": raw.get("payment_method"),
        "source_account": raw.get("source_account"),
        "wallet_id": raw.get("UPI_wallet"),
        "items": raw.get("items", []),
        "date": raw.get("date"),
        "time": raw.get("time"),
        "confidence": raw.get("confidence", 0.0)
    }

    return normalized
