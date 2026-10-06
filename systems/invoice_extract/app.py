"""Rule-based extraction of a small, explicit invoice schema from text."""
from __future__ import annotations
import re
import json
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation

MONEY = r"\$?\s*([0-9,]+\.\d{2})"

@dataclass
class Invoice:
    vendor: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    subtotal: str | None = None
    tax: str | None = None
    total: str | None = None
    errors: list[str] | None = None

    def to_dict(self):
        return asdict(self)


def extract(text: str) -> Invoice:
    def one(pattern):
        m = re.search(pattern, text, re.I | re.M)
        return m.group(1).strip() if m else None
    invoice = Invoice(
        vendor=one(r"^Vendor:\s*(.+)$"),
        invoice_number=one(r"^Invoice(?:\s+(?:No\.?|Number))?:\s*([\w-]+)"),
        invoice_date=one(r"^Date:\s*(\d{4}-\d{2}-\d{2})"),
        subtotal=one(r"^Subtotal:\s*" + MONEY),
        tax=one(r"^Tax:\s*" + MONEY),
        total=one(r"^Total:\s*" + MONEY),
        errors=[],
    )
    for field in ("vendor", "invoice_number", "invoice_date", "subtotal", "tax", "total"):
        if getattr(invoice, field) is None:
            invoice.errors.append(f"missing:{field}")
    if invoice.invoice_date:
        try:
            from datetime import date
            date.fromisoformat(invoice.invoice_date)
        except ValueError:
            invoice.errors.append("invalid:invoice_date")
    if invoice.subtotal and invoice.tax and invoice.total:
        try:
            if Decimal(invoice.subtotal) + Decimal(invoice.tax) != Decimal(invoice.total):
                invoice.errors.append("mismatch:total")
        except InvalidOperation:
            invoice.errors.append("invalid:amount")
    return invoice

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    from dataclasses import asdict
    print(json.dumps(asdict(extract(args.file.read_text())), indent=2))
