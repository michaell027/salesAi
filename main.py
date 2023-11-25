import PyPDF2
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_unique_filename(folder_path, filename):
    base_name, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(folder_path, unique_filename)):
        unique_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return unique_filename


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Check for valid file format
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")

    folder_path = "./pdf"
    os.makedirs(folder_path, exist_ok=True)

    unique_filename = get_unique_filename(folder_path, file.filename)
    file_location = os.path.join(folder_path, unique_filename)

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return JSONResponse(status_code=200,
                        content={"message": "File uploaded successfully with filename: " + unique_filename})


@app.get("/pdf")
async def pdf_to_text():
    text = ""
    pdf_path = "./pdf/RFPDOC_43752.pdf"
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
