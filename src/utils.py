import PyPDF2
import io

def extract_text_from_pdf(pdf_data):
    """Extrai o texto de um arquivo PDF.

    Args:
        pdf_data: Dados do arquivo PDF em bytes.

    Returns:
        str: Texto extraído do PDF.
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))

    pdf_text = ""
    
    for page in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page].extract_text()
    return pdf_text