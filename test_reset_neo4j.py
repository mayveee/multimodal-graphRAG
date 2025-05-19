import src.neo4j_runner as db

def reset_neo4j():
    try:
        db.run_query("MATCH (n) DETACH DELETE n")
    except Exception as e:
        print("❌ 쿼리 실행 중 오류 발생:", e)


if __name__ == "__main__":
    reset_neo4j()
