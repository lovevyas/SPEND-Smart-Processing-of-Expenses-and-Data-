import re

def extract_total_amount(text: str) -> float | None:
    """
    Extracts the final payable amount from receipt text.
    Looks for keywords like AMOUNT or TOTAL.
    """

    lines = text.splitlines()

    for line in lines:
        if "AMOUNT" in line.upper():
            match = re.search(r'\$\s*([\d]+\.\d{2})', line)
            if match:
                return float(match.group(1))

    return None

def extract_subtotal(text: str) -> float | None:
    lines = text.splitlines()
    for line in lines:
        if "SUBTOTAL" in line.upper():
            match = re.search(r'\$\s*([\d]+\.\d{2})', line)
            if match:
                return float(match.group(1))
    return None


def extract_tax(text: str) -> float | None:
    lines = text.splitlines()
    for line in lines:
        if "TAX" in line.upper():
            match = re.search(r'\$\s*([\d]+\.\d{2})', line)
            if match:
                return float(match.group(1))
    return None

def classify_document(text: str) -> str:
    upper_text = text.upper()

    if "UPI" in upper_text and "PAID" in upper_text:
        return "UPI_PAYMENT"

    if "SUBTOTAL" in upper_text or "TAX" in upper_text:
        return "RECEIPT"

    return "UNKNOWN"

def extract_upi_payment(text: str) -> dict:
    data = {}

    # Amount (₹300)
    amount_match = re.search(r'(₹|RS|R S|Z)\s*([\d,]+)', text)
    if amount_match:
        data["amount"] = float(amount_match.group(2).replace(",", ""))
    

    # Merchant (To:)
    to_match = re.search(r'To:\s*(.+)', text)
    if to_match:
        data["merchant"] = to_match.group(1).strip()

    # Account source (From:)
    from_block = re.search(r'From:\s*(.+)\n(.+)', text)
    if from_block:
        data["source_account"] = (
            from_block.group(1).strip() + " " + from_block.group(2).strip()
        )


    # UPI reference
    ref_match = re.search(r'UPI Ref No[:\s]*([\d]+)', text)
    if ref_match:
        data["upi_ref"] = ref_match.group(1)

    # Date & time
    datetime_match = re.search(
        r'(\d{1,2}:\d{2}\s*[AP]M).*?(\d{1,2}\s+\w+\s+\d{4})',
        text
    )
    if datetime_match:
        data["time"] = datetime_match.group(1)
        data["date"] = datetime_match.group(2)

    data["payment_method"] = "UPI"

    return data
