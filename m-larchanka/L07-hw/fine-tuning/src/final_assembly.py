from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "./tinyllama-json"
output_path = "./tinyllama-merged"

print("Loading base model...")

tokenizer = AutoTokenizer.from_pretrained(base_model_name)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    device_map="auto"
)

print("Loading LoRA adapter...")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("Merging weights...")❌ Плохие признаки:
merged_model = model.merge_and_unload()

print("Saving merged model...")
merged_model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)

print("DONE ✔ Model saved to:", output_path)
