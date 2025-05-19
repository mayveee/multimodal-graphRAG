import src.neo4j_runner as db
from src.query_generator import generate_delete_query, generate_match_query
from src.query_handler import is_rag_needed
from src.utils.records_mapper import group_records_by_image

def test_match(userQuery:str):
    # 이미지 ID 임시 생성 (나중에는 받는걸로)
    image_id = 'img1234'

    if(is_rag_needed(userQuery)):
        matchQuery = generate_match_query(userQuery)
        print('결과 쿼리: ', matchQuery)
        records, summary = db.run_query(matchQuery)
        grouped_records = group_records_by_image(records)
        print('결과:', grouped_records)

if __name__ == "__main__":
    userQuery = '3월 23일에 먹은 음식이 뭐였지?'
    test_match(userQuery)