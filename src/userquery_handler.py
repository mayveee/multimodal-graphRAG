import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_rag_needed(query: str) -> bool:
    """
    자연어 질의가 RAG 처리가 필요한지 판단
    """
    system_prompt = """
    너는 neo4j에 사용자 이미지 기반 데이터를 가지고 있어.
    질의가 llm이 생성가능한 답변인지 아니면 neo4j 검색이 필요한지 판단해서 대답해줘.
    필요하면 true, 아니면 false로 대답해줘
    """
    user_prompt = f"질의: \"{query}\" → true or false 로만 답해줘."

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=1000,
    )
    answer = response.choices[0].message.content.strip().lower()

    if(answer == 'true'):
        return True
    else:
        return False
    