from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter()

IMAGE_DIR = "images"

@router.get("/list-images")
async def list_images():
    try:
        files = os.listdir(IMAGE_DIR)
        image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]
        return JSONResponse(content={"images": image_files})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
