from openai import OpenAI
from api_pjt.config import OPENAI_API_KEY

CLIENT = OpenAI( api_key = OPENAI_API_KEY )

def ask_chatgpt(user_message):
    
    system_instructions = """sumary_line
영어는 한글로 번역하고, 한글은 영어로 번역하는것이 너의 임무이다.
"""

    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content
    

while True:
    user_input = input("\n사용자 입력: ")
    if user_input == "exit":
        break
    response = ask_chatgpt(user_input)
    print("\n챗봇 응답: ", response, "\n")

