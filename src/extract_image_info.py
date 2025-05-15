import extract_metadata
import extract_objects

def extract_image_info(image_bytes: bytes) -> dict:
    """
    이미지에서 메타데이터와 객체/관계 정보를 추출하여 하나의 dict로 반환

    """
    # 정보 1 메타데이터
    metadata = extract_metadata(image_bytes)
    print("추출된 metadata", metadata)

    # 정보 2 객체/관계
    objects = extract_objects(image_bytes)
    print("추출된 오브젝트/관계", objects)

    info = {
        "objects": objects.get("objects", []),
        "relationships": objects.get("relationships", []),
        "metadata": metadata
    }

    return info


