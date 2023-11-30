from PIL import Image
from click import File
import requests
from fastapi import Depends, FastAPI, Form, Request, UploadFile, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from io import BytesIO
import models
import torch

from transformers import CLIPProcessor, CLIPModel
from fastapi.responses import FileResponse, JSONResponse
from typing import List

import uvicorn

# DB관련 변수 또는 모듈 import
from database import SessionLocal, engine
from sqlalchemy.orm import Session

# models에 정의한 모든 클래스를 연결한 DB엔진에 테이블로 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        # yield 키워드는 FastAPI가 함수의 실행을 일시 중지하고 데이터베이스 세션을 호추자에게 반환하도록 지시
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# api
# @app.post("/predict")
# async def predict(files: List[UploadFile]):
    # # 첫 번째 파일을 선택
    # file = files[0]
    # # 이미지 업로드 및 처리
    # image = Image.open(BytesIO(await file.read()))
    # # CLIP 모델 입력 생성
    # inputs = processor(text=["Human","Animal","Food","Document","Landscape"], images=image, return_tensors="pt", padding=True)
    # # 모델 실행
    # outputs = model(**inputs)
    # # 결과 처리
    # logits_per_image = outputs.logits_per_image
    # probs = logits_per_image.softmax(dim=1)
    # result = {"file_name": file.filename, "probs": probs.tolist()}
    # return result


# 템플릿 엔진 설정
templates = Jinja2Templates(directory="templates")

# 정적 파일을 제공할 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="static/img"), name="img")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload( data: dict = Form(...), db: Session = Depends(get_db)):
    print(data)
    # test = models.Image(Image=image_list)
    # print("upload: ", test)
    for image in data:
        print(image)
        db.add(image)
    db.commit()
    url = app.url_path_for("read_root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# @app.post("/files/")
# async def create_file(file: bytes = File(), fileb: UploadFile = File(), token: str = Form()):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }

# @app.post("/predict")
# async def predict(request: Request, db: Session = Depends(get_db)):
   
#     for idx in range(len(Image)):
#         categoreyes=categoreyes_list[idx]
#         # 1. make buffer from bytes
#         buffer = io.BytesIO(categoreyes.data)

#         # 2. decode image form buffer
#         image = Image.open(buffer)
        
#         inputs = processor(text=class_name, images=image, return_tensors="pt", padding=True)
#         outputs = model(**inputs)
#         logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
#         probs = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities

#         result = class_dict[class_name[probs.argmax()]]
#         image_data = base64.b64encode(categoreyes.data).decode('utf-8')

#         predictions.append({"filename": categoreyes.filename, "result": result,"img":image_data})
#         classified[result].append(idx)

#     return templates.TemplateResponse("predicted.html",
#                                       {"request": request,
#                                        "predictions": predictions,
#                                        "classified":classified})    

if __name__== "__main__":
    uvicorn.run("main:app", reload=True)