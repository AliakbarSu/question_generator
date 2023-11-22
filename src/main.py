from pprint import pprint

# from colorama import Fore, Back, Stytle
from termcolor import colored, cprint

from InquirerPy import prompt

from chat_gpt import connect as connect_to_chatgpt, ask_question
from model import connect_to_db, list_questions, save_question
from question import Question, Option, load_local_question


def interface():
    questions = [
        {
            "type": "list",
            "name": "user_option",
            "message": "Do you want to save the generated question?",
            "choices": ["Save", "Retry", "list", "Exit"],
        }
    ]

    answers = prompt(questions)
    return answers.get("user_option")
    # return answers


def main():
    # connect_to_chatgpt()
    # ask_question("What is the meaning of life?")
    connect_to_db()

    option_1 = Option(alpha="A", text="Option A", is_correct=True)
    option_2 = Option(alpha="B", text="Option B", is_correct=False)
    question = Question(text="This is a question", options=[option_1, option_2])

    user_answer = interface()
    if user_answer == "Exit":
        return cprint("Exiting", "red")
    elif user_answer == "list":
        cprint(list_questions(), "green", "on_white")
        user_answer = interface()
    while user_answer == "Retry":
        user_answer = interface()
    else:
        print("Saving question")
        save_question(question)
        print("Question saved")


if __name__ == "__main__":
    main()
