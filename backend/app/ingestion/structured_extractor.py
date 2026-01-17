import re
from typing import Dict


def extract_structured_fields(text: str) -> Dict[str, str]:
    """
    Extract key invoice fields using regex + heuristics.
    This is deterministic and safe (no LLM).
    """

    fields = {}

    # -------- Invoice Number --------
    invoice_no_patterns = [
        r"invoice\s*no[:\s]*([A-Z0-9\-\/]+)",
        r"invoice\s*number[:\s]*([A-Z0-9\-\/]+)",
    ]

    for pattern in invoice_no_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields["invoice_number"] = match.group(1)
            break

    # -------- Invoice Date --------
    date_patterns = [
        r"date[:\s]*([0-9]{2}[\/\-][0-9]{2}[\/\-][0-9]{4})",
        r"date[:\s]*([0-9]{4}[\/\-][0-9]{2}[\/\-][0-9]{2})",
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields["invoice_date"] = match.group(1)
            break

    # -------- Total Amount --------
    total_patterns = [
        r"total\s*amount[:\s₹$]*([0-9,]+\.\d{2})",
        r"grand\s*total[:\s₹$]*([0-9,]+\.\d{2})",
        r"total[:\s₹$]*([0-9,]+\.\d{2})",
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields["total_amount"] = match.group(1)
            break

    # -------- Vendor Name (heuristic) --------
    # Assume vendor is in first 5 lines
    lines = text.split("\n")[:5]
    for line in lines:
        if len(line.strip()) > 3 and not re.search(r"invoice|date|gst", line, re.IGNORECASE):
            fields["vendor"] = line.strip()
            break

    return fields
