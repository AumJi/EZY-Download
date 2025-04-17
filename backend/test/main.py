from fastapi import FastAPI,Response
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import io

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["GET", "POST"],
    # allow_headers=["Content-Type"],
)
@app.post("/generate-zip")
async def generate_zip(data: dict):
    username = data["username"]
    
    # สร้างไฟล์ ZIP ในหน่วยความจำ
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # เพิ่มไฟล์ตัวอย่างลงใน ZIP
        zip_file.writestr(f"{username}_data.txt", f"ข้อมูลสำหรับผู้ใช้: {username}")
    
    # ส่งไฟล์ ZIP กลับไปให้ผู้ใช้
    zip_buffer.seek(0)
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={username}.zip"}
    )