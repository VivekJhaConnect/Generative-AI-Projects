import chainlit as cl
from src.llm import ask_order, message 

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    message.append({"role": "user", "content": message.content})
    response = ask_order(message)
    message.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()

