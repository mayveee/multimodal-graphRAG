from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import src.neo4j_runner as db
from src.dbquery_generator import generate_delete_query

router = APIRouter()

class DeleteRequest(BaseModel):
    image_id: str

@router.post("/delete")
async def delete_image(request: DeleteRequest):
    image_id = request.image_id

    query, params = generate_delete_query(image_id)

    result, summary = db.run_query(query, params)
    deleted_count = summary.counters.nodes_deleted

    return JSONResponse(content={
        "message": "삭제 완료",
        "deleted_nodes": deleted_count
    })
