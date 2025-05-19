from src.neo4j_runner import run_query
from src.query_generator import generate_delete_query


def test_delete():
    # 이미지 ID 임시 생성 및 추가(나중에는 받는걸로)
    image_id = 'img1234'
    query, params = generate_delete_query(image_id)
    result, summary = run_query(query, params)
    print("🗑 삭제된 노드 수:", summary.counters.nodes_deleted)

if __name__ == "__main__":
    test_delete()