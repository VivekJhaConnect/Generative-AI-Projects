from openai import OpenAI

client = OpenAI()

message = [
    {"role": 'System', "content": system_instruction}
]
def ask_order(message, model='gpt-3.5-turbo', temperature=0.5):
    response = client.chat.completions.create(
        model = model,
        message = [
            
        ]
    )