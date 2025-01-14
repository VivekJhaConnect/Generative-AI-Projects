from openai import OpenAI
from src.prompt import system_instruction

client = OpenAI()

message = [
    {"role": 'System', "content": system_instruction}
]
def ask_order(message, model='gpt-3.5-turbo', temperature=0.5):
    response = client.chat.completions.create(
        model = model,
        message = message,
        temperature=0.5
    )

    return response.choices[0].message.content