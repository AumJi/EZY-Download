# uvicorn backend.app.main:app --reload
from fastapi import FastAPI , Response, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
from bing_image_downloader import downloader
import zipfile ,shutil
import os, io

app = FastAPI()

# CORS: กลไกความปลอดภัยของเบราว์เซอร์ ที่ควบคุมการสื่อสารระหว่าง Frontend และ Backend เมื่ออยู่คนละโดเมน
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Item(BaseModel):
    title : str
    type : str
    amount : int

def download_images_with_extension(query, limit, extension=None, output_dir="downloads"):
    try:
        # สร้าง directory พร้อมตรวจสอบสิทธิ์
        os.makedirs(output_dir,exist_ok=True)
        
        # ทดสอบการเขียนไฟล์
        test_file = os.path.join(output_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        
        downloader.download(
            query,
            limit=limit,
            output_dir=output_dir,
            adult_filter_off=True,
            force_replace=False,
            filter=extension,
            timeout=1
        )

        print(f"ดาวน์โหลดเสร็จสิ้น: {query} ({limit} รูปภาพ)")
    except PermissionError:
        print(f"ไม่มีสิทธิ์เขียนไฟล์ใน directory: {output_dir}")
        print("โปรดระบุ directory อื่นหรือแก้ไขสิทธิ์การเข้าถึง")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))



# ตั้งค่าโฟลเดอร์ดาวน์โหลด
STORAGE_PATH = "./backend/app/storage"
DOWNLOAD_DIR = "./backend/app/storage/temp_download"
DOWNLOAD_ZIP = "./backend/app/storage/download.zip"

@app.post("/api/download")
def download_images(request: Item):    
        try:
            if os.listdir(STORAGE_PATH):
                shutil.rmtree(STORAGE_PATH)
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            
            # ตัวอย่างการใช้งาน
            lst = [i.strip() for i in request.title.split(',')]
            for i in lst:
                download_images_with_extension(i, request.amount, request.type, DOWNLOAD_DIR)

            if request.type != 'NaN':
                for i in os.listdir(DOWNLOAD_DIR):
                    folder_path = os.path.join(DOWNLOAD_DIR, i)
                    for j in os.listdir(folder_path):
                        if not j.endswith(DOWNLOAD_DIR):
                            os.rename(os.path.join(folder_path,j),os.path.join(folder_path,j.split('.')[0]+ request.type))

            shutil.make_archive('backend/app/storage/download','zip',DOWNLOAD_DIR)

            return FileResponse(
                path=DOWNLOAD_ZIP,
                media_type="application/zip",
                # headers={"Content-Disposition": f"attachment; filename={'download'}.zip"}
                filename="download.zip"
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/hello")
async def read_root():
    return {
        "message": "Welcome to EXY-Download API",
        "version": "1.0",
        "docs": "/docs",
        "endpoints": {
            "download": "/api/download (POST)"
        }}