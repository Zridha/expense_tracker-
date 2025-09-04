from fpdf import FPDF
from datetime import date 

def expenses_to_pdf(rows: list[dict], title: str = "Monthly Report") -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(40, 8, "Date")
    pdf.cell(25, 8, "Amount")
    pdf.cell(25, 8, "Curr")
    pdf.cell(40, 8, "Category")
    pdf.cell(0, 8, "Note", ln=True)
    pdf.set_font("Helvetica", size=10)
    for r in rows:
        pdf.cell(40, 7, str(r["spent_on"]))
        pdf.cell(25, 7, str(r["amount"]))
        pdf.cell(25, 7, r["currency"])
        pdf.cell(40, 7, r["category"])
        pdf.cell(0, 7, (r.get("note") or "")[:60], ln=True)
    return pdf.output(dest="S").encode("latin1", "ignore")

