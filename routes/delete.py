import os
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import src.neo4j_runner as db
from src.dbquery_generator import generate_delete_query

router = APIRouter()
IMAGE_DIR = "images"

@router.delete("/delete/{image_id}")
async def delete_image(image_id: str):
    try:
        # 확장자 찾기 (jpg/png 등)
        files = os.listdir(IMAGE_DIR)
        target = next((f for f in files if f.startswith(image_id)), None)

        if not target:
            return JSONResponse(status_code=404, content={"error": "이미지 없음"})
        
        # delete query 생성
        query, params = generate_delete_query(image_id)

        print('생성된 쿼리: ', query)
        print('생성된 param: ', params)
        
        # delete 쿼리 실행
        result, summary = db.run_query(query, params)
        print("삭제된 노드 수:", summary.counters.nodes_deleted)

        os.remove(os.path.join(IMAGE_DIR, target))
        return JSONResponse(content={"message": "삭제 완료"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})