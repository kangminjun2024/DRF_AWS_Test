from api_pjt.settings import OPENAI_API_KEY
from openai import OpenAI

CLIENT = OpenAI( api_key = OPENAI_API_KEY )

#번역하는 봇
def translate_bot(user_message):
        system_instructions = """
        영어는 한글로 번역하고, 한글은 영어로 번역하는것이 너의 임무이다.
        """

        completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {
                    "role": "system", 
                    "content": system_instructions
                },
                {
                    "role": "user", 
                    "content": user_message
                },
            ],
        )
        return completion.choices[0].message.content

#뭐 딴거 추천하는봇
'''
pass
'''


#뭐 딴거 작업하는봇
'''
pass
'''

# 이런식으로 만들면 된다