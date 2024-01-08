from openai import OpenAI
import os

client = None


def connect():
    global client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


discussion = []


def ask_question(question: str = None, response: str = None):
    if client:
        if response:
            discussion.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )
        if question:
            discussion.append(
                {
                    "role": "user",
                    "content": question,
                }
            )
        else:
            discussion.append(
                {
                    "role": "user",
                    "content": get_context(),
                }
            )
        chat_completion = client.chat.completions.create(
            messages=discussion,
            model="gpt-3.5-turbo",
        )

        return chat_completion
    else:
        raise Exception("OpenAI client not initialized")


def get_context():
    with open("src/context.txt", "r") as f:
        return f.read()
