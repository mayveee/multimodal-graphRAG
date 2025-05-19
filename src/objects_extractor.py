import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_objects(image_bytes: bytes) -> dict:
    """
    GPT API로 이미지에서 객체, 관계 추출
    Returns:
        {
            "objects": [
                {
                    "label": "label_name",
                },
                ...
            ],
            "relationships": [
                {
                    "subject": "label",
                    "predicate": "relationship_type",
                    "object": "label"
                },
                ...
            ]
        }
    """
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    system_prompt= """
    당신은 사진에서 찍은 의도를 파악해 주요 객체와 관계들을 찾아주는 도우미입니다.
    찾은 객체와 관계들은 나중에 사진을 찾는데 쓰입니다.
    """
    prompt = """
    다음 이미지를 보고 이미지 내에 존재하는 주요 객체들과 관계를 JSON 형식으로 정리해주세요.
    최소 단위의 개별 사물 말고 의미 있는 범주 수준에서 5개 이하의 주요 객체들을 뽑아주세요.
    형식은 다음과 같습니다:

    {
    "objects": [
        {
        "label": "label_name",
        },
        ...
    ],
    "relationships": [
        {
        "subject": "label",
        "predicate": "relationship_type",
        "object": "label"
        },
        ...
    ]
    }
    json만 응답에 포함시켜주세요.
    가능한 경우 건물, 간판, 상호, 사람, 브랜드 등도 포함해주세요.
    영어로 응답을 주세요.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},

            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]}
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    result = response.choices[0].message.content

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {}