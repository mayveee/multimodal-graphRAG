import extract_metadata

def extract_image_info(image_bytes: bytes) -> dict:
    # 정보 1 메타데이터
    metadata = extract_metadata(image_bytes)

    # 정보 2 라벨링 //TODO
    
    return metadata


