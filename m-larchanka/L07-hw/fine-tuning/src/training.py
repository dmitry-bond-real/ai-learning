print("Start...", flush=True)

import time

print("Start.1", flush=True)

# <- может повиснуть здесь!
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, TrainerCallback, logging

print("Start.2", flush=True)

from peft import LoraConfig, get_peft_model

print("Start.3", flush=True)

from datasets import load_dataset

print("Continue...", flush=True)

#model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# ==== tokenizer ====
print("Creating tokenizer...", flush=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# ==== model ====
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto"
)
model.config.use_cache = False

# ==== LoRA ====
print("Configuring LoRA...", flush=True)
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# ==== dataset ====
print("Loading dataset...", flush=True)
dataset = load_dataset("json", data_files="dataset.jsonl")["train"]


class HeartbeatCallback(TrainerCallback):
    def __init__(self, interval_seconds=30):
        print("HeartbeatCallback.ctor...", flush=True)
        self.interval_seconds = interval_seconds
        self.last_beat = 0.0

    def on_train_begin(self, args, state, control, **kwargs):
        print("HeartbeatCallback.on_train_begin...", flush=True)
        self.last_beat = time.time()
        print("[heartbeat] training started", flush=True)

    def on_step_end(self, args, state, control, **kwargs):
        print("HeartbeatCallback.on_step_end...", flush=True)
        now = time.time()
        if now - self.last_beat >= self.interval_seconds:
            print(
                f"[heartbeat] alive | step={state.global_step} | epoch={state.epoch}",
                flush=True,
            )
            self.last_beat = now


def tokenize(example):
    print(f"Tokening({example})...", flush=True)
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

dataset = dataset.map(tokenize, remove_columns=["text"])


logging.set_verbosity_info()

# ==== training ====
print("Create trainingArgs...", flush=True)
training_args = TrainingArguments(
    output_dir="./tinyllama-json",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=2,
    learning_rate=2e-4,
    #logging_steps=10,
    save_strategy="epoch",
    report_to="none",
    fp16=False,

    logging_steps=1,  # Логировать каждые 10 шагов (по умолчанию 500)
    logging_strategy="steps",

    #per_device_train_batch_size=1,
    #gradient_accumulation_steps=4,
    #num_train_epochs=1,
    #learning_rate=2e-4,
    ##logging_steps=10,
    ##save_strategy="epoch",
    #report_to="none",
    #fp16=False,
    
    #logging_strategy="steps",
    #logging_steps=10,
    #logging_first_step=True,

    #save_strategy="steps",
    #save_steps=50,

    #disable_tqdm=False,    
    
    dataloader_pin_memory=False
)

print("Create trainer...", flush=True)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    callbacks=[HeartbeatCallback(interval_seconds=30)],
)

print("Start training...", flush=True)
trainer.train()

print("Saving pretrained...", flush=True)
model.save_pretrained("./tinyllama-json")
tokenizer.save_pretrained("./tinyllama-json")

print("Finished.", flush=True)

input("Нажмите Enter, чтобы выйти...")