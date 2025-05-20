from src.answer_generator import generate_answer
import src.neo4j_runner as db
from src.dbquery_generator import generate_match_query
from src.userquery_handler import is_rag_needed


def test_match(user_query:str):
    
    # RAG 여부 검사
    if(is_rag_needed(user_query)):
        # match query 생성
        match_query = generate_match_query(user_query)
        print('결과 쿼리: ', match_query)
        # match query 실행
        records, summary = db.run_query(match_query)
        print('records: ', records)
        # 질의, 결과로 응답 생성
        answer = generate_answer(user_query, records)
    else:
        # RAG 필요없으면 그냥 응답
        answer = generate_answer(user_query)

    print('최종 응답:', answer)

if __name__ == "__main__":
    user_query = '크림 우동 먹은 날짜를 알려줘~'
    test_match(user_query)