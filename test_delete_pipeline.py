import src.neo4j_runner as db
from src.dbquery_generator import generate_delete_query

def test_delete():
    # 이미지 ID 임시 생성 (나중에는 받는걸로)
    image_id = 'img1234'

    # delete query 생성
    query, params = generate_delete_query(image_id)

    print('생성된 쿼리: ', query)
    print('생성된 param: ', params)
    
    # delete 쿼리 실행
    result, summary = db.run_query(query, params)
    print("삭제된 노드 수:", summary.counters.nodes_deleted)

if __name__ == "__main__":
    test_delete()