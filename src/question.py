from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class Option:
    id: str = field(init=False)
    alpha: str
    text: str
    is_correct: str
    explanation: str

    def __post_init__(self):
        self.id = str(uuid.uuid4())


@dataclass(kw_only=True)
class Question:
    uuid: str = field(init=False)
    text: str
    type: str
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
        self.uuid = str(uuid.uuid4())

    def get_correct_option(self):
        for option in self.options:
            if option.is_correct:
                return option
