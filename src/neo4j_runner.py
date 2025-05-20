from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
print("✅ URI:", NEO4J_URI)
print("✅ USERNAME:", NEO4J_USERNAME)
print("✅ PASSWORD:", NEO4J_PASSWORD)

def run_query(query: str, parameters: dict = None) -> tuple[list[dict], object]:
    """
    Cypher 쿼리를 실행하고 결과를 list[dict], summary로 반환
    """
    with GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            records = [record.data() for record in result]
            summary = result.consume()
            return records, summary
