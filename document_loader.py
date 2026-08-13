
from pypdf import PdfReader
from docx import Document


def read_file(upload_file):

    file_name = upload_file.name.lower()

    if file_name.endswith(".pdf"):
        document=[]
        pdf_reader = PdfReader(upload_file)

        for page_number, page in enumerate( pdf_reader.pages,start=1):

            page_text = page.extract_text()

            if page_text and page_text.strip():
                document.append({
                    "text": page_text,
                    "source": upload_file.name,
                    "page": page_number
                })
        return document

    elif file_name.endswith(".docx"):

        document = Document(upload_file)

        file_text = ""

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                file_text = file_text + paragraph.text + "\n"

        if file_text.strip():
            return[{
                "text":file_text,
                "source":upload_file.name,
                "page":1
            }]
        return []

    elif file_name.endswith(".txt"):

        file_text= upload_file.read().decode("utf-8")
        if file_text.strip():
            return[{
                "text":file_text,
                "source":upload_file.name,
                "page":1
                  }]
        return []
    return []

