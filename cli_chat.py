from chat_gpt_wrapper import ChatGptWrapper
from context_providers import WikiContextProvider

wrapper = ChatGptWrapper(WikiContextProvider())

print("Welcome to wiki chat gpt!")

while True:
    user_input = input("You: ")
    if user_input == "exit" or user_input == "q":
        break
    response = wrapper.sync_get_response(user_input)
    print("Bot: " + response)
