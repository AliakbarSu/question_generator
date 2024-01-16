from pymongo import MongoClient
from pymongo.server_api import ServerApi
from question import Question, Option
import os
import json

client = None


def connect_to_db():
    global client
    """Connects to the specific database."""
    uri = os.environ.get("MONGODB_URI", "localhost")
    client = MongoClient(uri, server_api=ServerApi("1"))
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def list_questions():
    """
    List all questions in the database.
    """
    if client:
        db = client.get_database(name="Questions")
        questions = db.get_collection(name="questions").find()
        questions_list: list[Question] = []
        for question in questions:
            options = question.get("options")
            questions_list.append(
                Question(
                    text=question.get("text"),
                    type=question.get("type"),
                    options=[
                        Option(
                            text=option.get("text"),
                            alpha=option.get("alpha"),
                            is_correct=option.get("is_correct"),
                            explanation=option.get("explanation"),
                        )
                        for option in options
                    ],
                )
            )
        return questions_list
    else:
        raise Exception("MongoDB client not initialized")


def save_question(question: Question):
    """
    Save a question to the database.
    """
    if client:
        db = client.get_database(name="Questions")
        print("Saving question in the database")
        db.get_collection(name="questions").insert_one(question.__dict__())

    save_question_to_file(question)


def save_question_to_file(question: Question):
    """
    Save a question to a file.
    """
    questions_list = []
    with open("questions.json", "r") as f:
        questions_list = json.load(f)
        questions_list.append(question.__dict__())

    with open("questions.json", "w") as f:
        json.dump(questions_list, f, indent=4)
