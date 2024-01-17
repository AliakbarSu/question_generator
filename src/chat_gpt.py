from openai import OpenAI
import os
import json

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


def get_existing_questions():
    with open("questions.json", "r") as f:
        questions_list = json.load(f)
        question_string = ", ".join(
            [f"\"{questions_list['text']}\"" for questions_list in questions_list][0:10]
        )
        return question_string


def get_context():
    existing_questions = get_existing_questions()
    with open("context.txt", "r") as f:
        context = f.read()
        return f"{context}. The following questions have already been generated {existing_questions}"
