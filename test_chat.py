from src.chat import chat
from src.utils.chat_memory import print_memory
from test_match_pipeline import test_match

session_id = "1234"

while True:
    query = input("You: ")
    if query == "exit":
        break
    test_match(query)

print_memory("1234")