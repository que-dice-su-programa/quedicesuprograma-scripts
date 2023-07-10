import pdfplumber

def read_pdf(party):
    pdf = pdfplumber.open(f"./input/{party}.pdf")

    text = ''
    for page in pdf.pages:
        text += page.extract_text()

    return text
