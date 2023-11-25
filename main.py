from fastapi import FastAPI
import PyPDF2

app = FastAPI()

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.numPages

        for page_number in range(num_pages):
            page = pdf_reader.getPage(page_number)
            text += page.extractText()

    return text

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-pdf")
async def upload_pdf(file_path: str):
    text_content = pdf_to_text(file_path)
    return {"text_content": text_content}
