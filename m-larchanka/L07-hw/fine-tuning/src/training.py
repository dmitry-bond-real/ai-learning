print("Start...", flush=True)

import time

import os
import torch
# Максимально использовать все ядра CPU
# там капец какой-то с этими ядрами! Похоже он просто запускает кучу копий этого скрипта
_cpu_count = (os.cpu_count() or 1) - 1
torch.set_num_threads(_cpu_count)
torch.set_num_interop_threads(_cpu_count)
print(f"CPU threads: {_cpu_count}, torch threads: {torch.get_num_threads()}/{torch.get_num_interop_threads()}", flush=True)

print("Start.1", flush=True)

# <- может повиснуть здесь!
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, TrainerCallback, logging
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

print("Continue...", flush=True)

#model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


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


def main():
    # ==== tokenizer ====
    print("Creating tokenizer...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    print(f"✓ Tokenizer loaded from {model_name}", flush=True)

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

    # ==== model ====
    print(f"Loading model from Hugging Face: {model_name}...", flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="cpu",
        cache_dir="model_cache"
    )
    print(f"✓ Model loaded successfully! Parameters: {model.num_parameters():,}", flush=True)
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
        
        eval_strategy="no", #evaluation_strategy="no",  # Не выполнять оценку во время обучения
        do_train=True,
        do_eval=False, # Также убедитесь, что do_eval установлен в False
        
        dataloader_pin_memory=False,
        dataloader_num_workers=0,
        #dataloader_num_workers=max(1, 14) # (_cpu_count := os.cpu_count() or 1) - 1),    
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


if __name__ == "__main__":
    main()
    