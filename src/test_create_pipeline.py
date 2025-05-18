import json
from extract_image_info import extract_image_info
from llm_query import generate_create_query
import neo4j_runner as db

def test():
    # 테스트 파일 읽기
    with open("images/test1.JPEG", "rb") as f:
        image_bytes = f.read()

    # 이미지 정보 추출
    imageinfo = extract_image_info(image_bytes)
    print("이미지 정보:", imageinfo)

    # 이미지 ID 임시 생성 및 추가(나중에는 받는걸로)
    image_id = 'img1234'
    imageinfo["image_id"] = image_id

    # 정보로 쿼리 생성   
    query = generate_create_query(imageinfo)
    print("최종결과", query)

    # Neo4j aura저장
    try:
        results, summary = db.run_query(query)
        print("추가된 노드의 개수", summary.counters.nodes_created)
    except Exception as e:
        print("❌ 쿼리 실행 중 오류 발생:", e)

    db.close_driver()


if __name__ == "__main__":
    test()
