import pdfplumber


def extract_pages_from_pdf(file):
    """
    Extract text page-wise from uploaded PDF.
    Returning page numbers helps us show source/reference in answers.
    """
    pages = []

    with pdfplumber.open(file) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append({
                "page_number": index,
                "text": text.strip()
            })

    return pages
