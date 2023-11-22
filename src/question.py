from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Option:
    alpha: str
    text: str
    is_correct: str


@dataclass(kw_only=True)
class Question:
    text: str
    options: list[Option]
    correct_option: Option = field(init=False)

    def __dict__(self):
        return {
            "text": self.text,
            "options": [option.__dict__ for option in self.options],
            "correct_option": self.correct_option.__dict__,
        }

    def __post_init__(self):
        self.correct_option = self.get_correct_option()

    def get_correct_option(self):
        for option in self.options:
            if option.is_correct:
                return option


def save_question(question: Question):
    """
    Save a question to the database.
    """
    print(f"Saving question: {question}")


def load_local_question():
    """
    Load a question from the local file system.
    """
    print("Loading local question")
