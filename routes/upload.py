from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from typing import List
import hashlib
import os
from typing import List
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.background import BackgroundTasks
from src.dbquery_generator import generate_create_query
from src.image_info_extractor import extract_image_info
import src.neo4j_runner as db

router = APIRouter()

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def after_upload_process(saved_paths: List[str]):
    for path in saved_paths:
        try:
            # 테스트 파일 읽기
            with open(path, "rb") as f:
                image_bytes = f.read()

            # 이미지 정보 추출
            imageinfo = extract_image_info(image_bytes)
            print("이미지 정보:", imageinfo)

            # hash id 생성
            image_id = os.path.splitext(os.path.basename(path))[0]
            imageinfo["image_id"] = image_id

            # 정보로 쿼리 생성   
            query = generate_create_query(imageinfo)
            print("최종결과", query)

            # Neo4j aura저장
            results, summary = db.run_query(query)
            print("추가된 노드의 개수", summary.counters.nodes_created)
        except Exception as e:
            print(f"{path} 처리 중 오류")

def generate_file_id(file_bytes: bytes) -> str:
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    return file_hash[:12]

@router.post("/upload")
async def upload_images(
    background_tasks: BackgroundTasks,
    images: List[UploadFile] = File(...)
):
    results = []
    saved_paths = []

    for image in images:
        content = await image.read()
        file_id = generate_file_id(content)

        ext = os.path.splitext(image.filename)[1]
        filename = f"{file_id}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        saved_paths.append(file_path)
        results.append({
            "id": file_id,
            "filename": filename,
            "path": f"/{UPLOAD_DIR}/{filename}"
        })

    background_tasks.add_task(after_upload_process, saved_paths)

    return JSONResponse(content={"uploaded": results})
