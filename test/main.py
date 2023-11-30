from fastapi import Depends, FastAPI, Form, Request, UploadFile, status
import uvicorn
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = Path() / 'uploads'

UPLOAD_DIR = Path.cwd() / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 템플릿 엔진 설정
templates = Jinja2Templates(directory="templates")

# 정적 파일을 제공할 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="static/img"), name="img")

@app.post('/uploadfile/')
async def upload_file(file_uploads: List[UploadFile]):
    uploaded_files = []
    for file_upload in file_uploads:
        print(f"Received file: {file_upload.filename}")
        data = await file_upload.read()
        save_to = UPLOAD_DIR / file_upload.filename
        with open(save_to, 'wb') as f:
            f.write(data)
        uploaded_files.append(file_upload.filename)
        print(f"Saved file: {file_upload.filename}")
    print("File uploaded successfully!")
    # return {"filename" : [f.filename for f in file_uploads]}
    return {"filename" : uploaded_files}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__== "__main__":
    uvicorn.run("main:app", reload=True)