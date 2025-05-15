from extract_objects import extract_objects 

with open("images/test1.JPEG", "rb") as f:
    image_bytes = f.read()

info = extract_objects(image_bytes)

print("추출 결과:")
print(info)