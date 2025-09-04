# app/services/reporting.py
import csv, io
from app.utils.pdf import expenses_to_pdf

def expenses_to_csv_bytes(rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["spent_on", "amount", "currency", "category", "note"])
    for r in rows:
        writer.writerow([r.get("spent_on"), float(r.get("amount", 0)), r.get("currency", ""), r.get("category", ""), (r.get("note") or "")])
    return output.getvalue().encode("utf-8")

def save_report_files(rows, title, out_csv_path, out_pdf_path):
    csv_bytes = expenses_to_csv_bytes(rows)
    with open(out_csv_path, "wb") as f:
        f.write(csv_bytes)
    pdf_bytes = expenses_to_pdf(rows, title=title)
    with open(out_pdf_path, "wb") as f:
        f.write(pdf_bytes)
