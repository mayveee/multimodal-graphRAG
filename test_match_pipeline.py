from src.answer_generator import generate_answer
import src.neo4j_runner as db
from src.dbquery_generator import generate_match_query
from src.userquery_handler import is_rag_needed


def test_match(user_query:str):
    
    if(is_rag_needed(user_query)):
        match_query = generate_match_query(user_query)
        print('결과 쿼리: ', match_query)
        records, summary = db.run_query(match_query)
        print('records: ', records)       
        answer = generate_answer(user_query, records)
    else:
        answer = generate_answer(user_query)

    print('최종 응답:', answer)

if __name__ == "__main__":
    user_query = '크림 우동 먹은 날짜를 알려줘~'
    test_match(user_query)