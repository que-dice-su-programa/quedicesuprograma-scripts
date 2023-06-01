import PyPDF2

def read_pdf(party):
    with open(f"./input/{party}.pdf", 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text
