import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "당신은 Cypher 쿼리를 생성하는 Neo4j 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    return response.choices[0].message.content

def generate_create_query(info) -> str:
    """
    llm 호출하여 CREATE query 생성
    input: {imageId, }
    """
    prompt = f"다음 정보를 기반으로 Cypher CREATE 쿼리를 생성해줘:\n{info}"
    return call_llm(prompt)

def generate_match_query(info) -> str:
    prompt = f"다음 정보를 기반으로 Cypher match 쿼리를 생성해줘:\n{info}"
    return call_llm(prompt)

def generate_delete_query(info) -> str:
    prompt = f"다음 정보를 기반으로 Cypher CREATE 쿼리를 생성해줘:\n{info}"
    return call_llm(prompt)