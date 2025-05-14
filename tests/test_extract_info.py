from feature_upload.extract_image_info import extract_image_info

with open("images/test1.JPEG", "rb") as f:
    image_bytes = f.read()

info = extract_image_info(image_bytes)

print("추출 결과:")
print(info)