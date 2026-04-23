import torch

print(torch.cuda.is_available())  # Должно вернуть True
print(torch.cuda.get_device_name(0)) # Имя вашей видеокарты

# output.1: 
#   AssertionError: Torch not compiled with CUDA enabled

# output.2:
#   True
#   NVIDIA GeForce RTX 3060