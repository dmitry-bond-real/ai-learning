from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import json
import re

# ==== CONFIG ====
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH = "./tinyllama-json"
QUESTIONS = [
    "Что такое интернет?",
    "Как работает компьютер?",
    "Кто такой Илон Маск?",
    "Объясни гравитацию",
    "Что такое нейросеть?",
    "Как работает алгоритм сортировки?",
    "Почему небо голубое?",
    "Что такое программирование?",
    "Как устроен CPU?",
    "Объясни искусственный интеллект"
]

# ==== LOAD MODEL ====
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    device_map="auto"
)

model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
model.eval()print("Model loaded ✔")

# ==== JSON EXTRACTOR ====


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except:
        return None

# ==== GENERATION ====


def generate(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)


# ==== STRESS TEST ====
valid_json = 0
total = len(QUESTIONS)
print("\n===== STRESS TEST START =====\n")
for i, q in enumerate(QUESTIONS, 1):
    prompt = f"""### Instruction:
Ответь строго в JSON формате
### Input:
{q}
### Response:
"""
    result = generate(prompt)
    parsed = extract_json(result)
    print(f"Q{i}: {q}")
    print("RAW OUTPUT:")
    print(result)
    if parsed:
        print("JSON VALID ✔")
        valid_json += 1
    else:
        print("JSON INVALID ❌ ")
    print("-" * 60)

# ==== RESULTS ====
print("\n===== FINAL RESULT =====")
print(f"Valid JSON: {valid_json}/{total}")
print(f"Accuracy: {valid_json / total * 100:.2f}%")
