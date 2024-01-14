from pprint import pprint
import json

# from colorama import Fore, Back, Stytle
from termcolor import colored, cprint

from InquirerPy import prompt

from chat_gpt import connect as connect_to_chatgpt, ask_question
from model import connect_to_db, list_questions, save_question
from question import Question, Option


def interface():
    questions = [
        {
            "type": "list",
            "name": "user_option",
            "message": "Do you want to save the generated question?",
            "choices": ["Generate", "Save", "list", "Exit"],
        }
    ]

    answers = prompt(questions)
    return answers.get("user_option")


def main():
    connect_to_db()
    connect_to_chatgpt()

    user_answer = None
    response = None
    question = None
    while user_answer != "Exit":
        user_answer = interface()
        if user_answer == "Exit":
            return cprint("Exiting", "red")
        elif user_answer == "Generate":
            cprint("Generating question... it takes a while", "green")
            generated_question = ask_question(question=question, response=response)
            response = generated_question.choices[0].message.content
            question = "generate another one"
            print_question(response)
        elif user_answer == "Save":
            print("Saving question")
            parsed_question = parse_question(response)
            save_question(parsed_question)
            cprint("Question saved", "blue")
        elif user_answer == "list":
            cprint(list_questions(), "green", "on_white")
            user_answer = interface()


def print_question(question: str):
    cprint(f"Question: {question}", "green")


def parse_question(question: str):
    question_json = json.loads(question)
    options = question_json.get("options")
    option1 = Option(
        alpha=options[0].get("alpha"),
        text=options[0].get("text"),
        explanation=options[0].get("explanation"),
        is_correct=options[0].get("is_correct"),
    )
    option2 = Option(
        alpha=options[1].get("alpha"),
        text=options[1].get("text"),
        explanation=options[1].get("explanation"),
        is_correct=options[1].get("is_correct"),
    )
    option3 = Option(
        alpha=options[2].get("alpha"),
        text=options[2].get("text"),
        explanation=options[2].get("explanation"),
        is_correct=options[2].get("is_correct"),
    )
    option4 = Option(
        alpha=options[3].get("alpha"),
        text=options[3].get("text"),
        explanation=options[3].get("explanation"),
        is_correct=options[3].get("is_correct"),
    )
    question = Question(
        text=question_json.get("text"),
        type="amc",
        options=[option1, option2, option3, option4],
    )
    return question


if __name__ == "__main__":
    main()
