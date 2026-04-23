import random
import json

MODEL_NAME = "tinyllama"

INSTRUCTIONS = [
    "Ответь строго в JSON формате",
    "Верни только JSON объект",
]
math_templates = [
    "Сколько будет {a}+{b}?",
    "Чему равно {a} * {b}?"
]

generic_answers = [
    "Это базовое объяснение",
    "Это известный факт"
]


def generate_sample():
    a, b = random.randint(1, 50), random.randint(1, 50)
    print(f"a = {a}, b = {b}")

    question = f"Сколько будет {a}+{b}?"
    answer = f"{a}+{b} равно {a+b}"

    response_json = {
        "model": MODEL_NAME,
        "type": "response",
        "message": answer
    }

    text = f"""### Instruction:
{random.choice(INSTRUCTIONS)}
### Input:
{question}
### Response:
{json.dumps(response_json, ensure_ascii=False)}
"""

    return {"text": text}


def generate_dataset(n=300):
    return [generate_sample() for _ in range(n)]


def save(dataset):
    with open("dataset.jsonl", "w", encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    data = generate_dataset(300)
    save(data)
