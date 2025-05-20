import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def generate_answer(user_query: str, data: dict | None = None) -> str:
    """
    자연어 쿼리를 바탕으로 LLM이 자연어 응답 생성(생성 정보 있으면 파라미터로)
    - data가 있을 경우: RAG 기반 응답
    - 빈 dict일 경우: 정보 없음 안내
    - None일 경우: RAG 없이 질의만으로 응답
    """
    system_prompt = """
    너는 챗봇 AI야.
    조건1: 사용자와 대화하듯이 사용자와 비슷한 말투로 응답해줘!
    조건2: 질의는 주어지고 응답에 필요한 배경정보가 있다면 제공될거야.
    조건3: 응답에 필요한 배경 정보가 없다면 정보나 관련 이미지를 찾을 수 없다는 식으로 응답해줘!
    """

    """
    TODO: 챗봇 처럼 하려면 앞 대화를 messages에 같이 넘겨주던가 해야 맥락 이해 가능.
    1. 클라 캐시에 저장 해뒀다가 보내는 방법
    2. redis 같이 서버 메모리에 userid/sessionid 기반으로 저장해두는 방법
    """

    answer = ''
    if isinstance(data, dict) and len(data) == 0:
        data = {
            "time": "정보 없음",
            "location": "정보 없음",
            "objects": [],
            "relations": []
        }
    
    if data is None:
        user_prompt = f"[질문]\n{user_query}"    
    else:
        import json
        context_str = json.dumps(data, ensure_ascii=False, indent=2)
        user_prompt = f"[질문]\n{user_query}\n\n[배경 정보]\n{context_str}"
    
    print('생성된 프롬프트: ', user_prompt)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    
    answer = response.choices[0].message.content

    return answer