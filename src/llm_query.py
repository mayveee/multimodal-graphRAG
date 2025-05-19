import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "당신은 Cypher 쿼리를 생성하는 Neo4j 전문가입니다. 바로 실행가능한 Cypher 쿼리만 리턴해주세요."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    return response.choices[0].message.content

def generate_create_query(info) -> str:
    """
    LLM 호출하여 CREATE 쿼리 생성
    """
    info_json_str = json.dumps(info, indent=2, ensure_ascii=False)
    prompt = f"""\
        아래 JSON을 기반으로 Cypher CREATE 쿼리를 작성해줘.

        반드시 다음 규칙을 지켜야 해
        1. `Image` 노드는 `image_id`만 속성으로 가져야 해.
        2. `DateTime`, `Latitude`, `Longitude`, `시`, `구`, `동`, `로`는 Image 노드에 직접 넣지 마.
        3. `Time` 노드를 따로 만들고, `datetime` 속성만 포함해.
        4. `Location` 노드를 따로 만들고, 나머지 장소 관련 속성들을 넣어.
        5. `Image` 노드는 `Time`과 `TAKEN_AT_TIME`, `Location`과 `TAKEN_AT_LOCATION` 관계로 연결해.
        6. `Image` 노드는 각 객체 노드들과 contains 관계로 연결해.


        {info_json_str}
        """
    return call_llm(prompt)

def generate_match_query(info) -> str:
    prompt = f"다음 정보를 기반으로 Cypher match 쿼리를 생성해줘:\n{info}"
    return call_llm(prompt)

def generate_delete_query(info) -> str:
    prompt = f"다음 정보를 기반으로 Cypher CREATE 쿼리를 생성해줘:\n{info}"
    return call_llm(prompt)