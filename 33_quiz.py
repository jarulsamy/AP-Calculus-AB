import json
import random

from PyInquirer import prompt
from PyInquirer import style_from_dict
from PyInquirer import Token


class QA(object):
    def __init__(self, question, correct_answer, incorrect=None, type_="D"):
        self.question = question
        self.correct = correct_answer
        self.incorrect = []
        if self.incorrect is None:
            self.incorrect = []
        else:
            self.incorrect = incorrect

        if type_ == "D":
            self.type = "Derive"
        elif type_ == "I":
            self.type = "Integrate"

    def __str__(self):
        ret = f"""
        Question: {self.type} {self.question}
        Correct: {self.correct_answer}
        Incorrect: {self.incorrect}
        """
        return ret

    def __repr__(self):
        return self.__srt__()


def load_data(filename: str):
    with open(filename) as f:
        data = json.load(f)
    return data


def derive_set(filename="33.json"):
    data = load_data(filename)

    derive = data["Derive"]
    question_answer_set = []

    keys = list(derive.keys())
    values = list(derive.values())

    for k, v, in zip(keys, values):
        k_set = keys[:]
        v_set = values[:]
        k_set.remove(k)
        v_set.remove(v)

        incorrect = random.sample(v_set, 3)
        question_answer_set.append(QA(k, v, incorrect, type_="D"))

    while len(question_answer_set) > 0:
        ret = random.choice(question_answer_set)
        question_answer_set.remove(ret)
        yield ret


def integral_set(filename="33.json"):
    data = load_data(filename)

    integrate = data["Integrate"]
    question_answer_set = []

    keys = list(integrate.keys())
    values = list(integrate.values())

    for k, v in zip(keys, values):
        k_set = keys[:]
        v_set = values[:]
        k_set.remove(k)
        v_set.remove(v)

        incorrect = random.sample(v_set, 3)
        question_answer_set.append(QA(k, v, incorrect, type_="I"))

    while len(question_answer_set) > 0:
        ret = random.choice(question_answer_set)
        question_answer_set.remove(ret)
        yield ret


def qa_session(gen):
    for i in gen():
        correct = i.correct
        set_ = i.incorrect[:]
        set_.append(correct)
        q = [{"name": i} for i in set_]
        q.append("Quit")

        question = [
            {
                "type": "list",
                "message": f"{i.type} {i.question}",
                "name": "answer",
                "choices": q,
            }
        ]
        answers = prompt(question, style=style)

        if answers["answer"] == i.correct:
            print("Well Done!")
        elif answers["answer"] == "Quit":
            exit(0)
        else:
            print(f"Incorrect, correct answer: {i.correct}")


if __name__ == "__main__":
    style = style_from_dict(
        {
            Token.Separator: "#cc5454",
            Token.QuestionMark: "#673ab7 bold",
            Token.Selected: "#cc5454",
            Token.Pointer: "#673ab7 bold",
            Token.Instruction: "",
            # Token.Answer: '#f44336 bold',
            Token.Answer: "#ff6600 bold",
            Token.Question: "",
        }
    )

    try:
        qa_session(derive_set)
        qa_session(integral_set)

    except KeyboardInterrupt:
        exit(0)
