from extract_image_info import extract_image_info
from llm_query import generate_create_query
import src.neo4j_runner as db



def test():
    # 테스트 파일 읽기
    with open("images/test1.JPEG", "rb") as f:
        image_bytes = f.read()

    # 이미지 정보 추출
    imageinfo = extract_image_info(image_bytes)
    # 정보로 쿼리 생성
    query = generate_create_query(imageinfo)
    
    print(query)
    """
    try:
        results = db.run_query(query)
        print("✅ 결과:")
        for row in results:
            print(row)
    except Exception as e:
        print("❌ 쿼리 실행 중 오류 발생:", e)
    """

if __name__ == "__main__":
    try:
        test()
    finally:
        db.close_driver()
