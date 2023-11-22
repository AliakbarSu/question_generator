from openai import OpenAI
import os

client = None

def connect():
    global client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ask_question(question: str):
    if client:
        if len(question) == 0:
            return "Please ask a question."
        
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gpt-3.5-turbo")
        
        return chat_completion
    else:
        raise Exception("OpenAI client not initialized")
    

def get_context():
    return "This is a context"