import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "당신은 Cypher 쿼리를 생성하는 Neo4j 전문가입니다. 바로 실행 가능한 문자열 Cypher 쿼리만 리턴해주세요."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
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
        2. `DateTime`, `Latitude`, `Longitude`, `address_info`는 Image 노드에 직접 넣지 마.
        3. `Time` 노드를 따로 만들고 datetime에서 앞부분은 `date`로 뒷부분은 `time` 속성으로 저장해
        4. `Location` 노드를 따로 만들고, `address_info`를 넣어.
        5. `Image` 노드는 `Time`과 `TAKEN_AT_TIME`, `Location`과 `TAKEN_AT_LOCATION` 관계로 연결해.
        6. 각 객체는 Object노드로 만들고 속성으로 (label: 객체 이름), (type: 객체 종류) 를 가져. type은 food 같이 판단해서 적어줘. 
        7. `Image` 노드는 각 객체 노드들과 contains 관계로 연결해.

        {info_json_str}
        """
    return call_llm(prompt)

def generate_match_query(userQuery: str) -> str:
    """
    자연어 질의를 받고 LLM으로 필요한 쿼리들을 생성하는 함수
    """
    from datetime import date
    today = date.today()
    prompt = f"""\
        다음 유저의 자연어 질의에 답하기 위한 Cypher 쿼리를 생성해줘
        여러개의 다중 쿼리를 생성해도 돼.
        조건:
        - 조건에 맞는 Image 노드를 먼저 매칭한다.
        - 조건에 해당하는 Image 노드를 중심으로 관련된 모든 서브 노드 (Object, Time, Location) 및 관계를 포함해서 전체 서브그래프를 반환하는 쿼리를 생성해 줘.
        - 단, Object와 Object 사이에 관계가 있을 경우, 해당 관계도 포함해줘.
        - obj간 관계를 임의로 만들지 말고 와일드카드로 전부 가져오되 collect를 해줘
        - 만약 object의 label을 비교하는 경우 contains로 비교해줘.
        - 최종 리턴은 img, time, location, obj, relationship 형식으로 해줘.
        오늘은 {today}야

        neo4j DB 구조는 다음과 같아
        Image 노드: image_id-이미지 고유 id
        obj:Object 노드(이미지에 포함된 객체): label-영어로된 이름, type-객체 종류
        t:Time 노드: date-2025-03-23 같은 양식, time-12:36:42 같은 양식
        loc:Location 노드: address_info 속성에 "문화원로, 봉명동, 온천1동, 유성구, 대전광역시, 34184, 대한민국" 와 같이 저장
        (Image)-[:contains]->(Object) 관계 반드시 있음.
        (Image)-[:TAKEN_AT_TIME]->(Time) 관계 있음.
        (Image)-[:TAKEN_AT_LOCATION]->(Location) 관계 있음.
        (Ojbect) 와 (Object) 사이의 관계가 있으면 관계로 연결됨.
        {userQuery}
        """
    return call_llm(prompt)

def generate_delete_query(image_id: str) -> tuple[str, dict]:
    """
    주어진 id를 가진 노드를 삭제하는 Cypher 쿼리와 파라미터 반환

    Args:
        id (str): 삭제할 노드의 고유 ID

    Returns:
        tuple[str, dict]: Cypher 쿼리 문자열과 파라미터 딕셔너리
    """
    query = """
    MATCH (n:Image {image_id: $image_id})-[]-(m)
    DETACH DELETE n, m
    DETACH DELETE n
    """
    parameters = {"image_id": image_id}
    return query, parameters