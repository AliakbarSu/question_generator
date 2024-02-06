import time
import uuid
from dataclasses import dataclass, field


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
    field: str
    options: list[Option]
    correct_option: Option = field(init=False)
    available: bool = field(init=False)
    demo: bool = field(init=False)
    created_at: str = field(init=False)
    updated_at: str = field(init=False)

    def __dict__(self):
        return {
            "text": self.text,
            "options": [option.__dict__ for option in self.options],
            "type": self.type,
            "field": self.field,
            "correct_option": self.correct_option.__dict__,
            "available": self.available,
            "demo": self.demo,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __post_init__(self):
        self.correct_option = self.get_correct_option()
        self.uuid = str(uuid.uuid4())
        self.available = True
        self.demo = False
        self.created_at = str(time.time())
        self.updated_at = str(time.time())

    def get_correct_option(self):
        for option in self.options:
            if option.is_correct:
                return option
