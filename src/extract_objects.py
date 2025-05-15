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

    prompt = """
    다음 이미지를 보고 이미지 내에 존재하는 주요 객체들과 관계를 JSON 형식으로 정리해주세요.
    사진의 의도와 관련없는 너무 세세한 객체는 제외해주세요.
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