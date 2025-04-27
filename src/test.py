from extract_image_info import extract_image_info

# 1. 파일 열기
with open("images/test1.JPEG", "rb") as f:
    image_bytes = f.read()

# 2. 메타데이터 추출
info = extract_image_info(image_bytes)

# 3. 결과 출력
print("추출 결과:")
print(info)