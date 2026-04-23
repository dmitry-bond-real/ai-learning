
# Команды и ИИ Запросы

шаг 0:
```
python -m venv .venv
```

шаг 1:
```
role: python developer expert
task: prepare requirements.txt file for this folder
```



# Errors

## Problem activate venv

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& w:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\.venv\Scripts\Activate.ps1)
ParserError: 
Line |
   1 |  … ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& w: …
     |                                                                ~
     | Unexpected token ')' in expression or statement.
PS W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning> 
```

Retarted VsCode - problem gone


## Strange syntax error

```
g\.venv\Scripts\Activate.ps1)
(.venv) PS W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning> python .\src\generate_dataset.py
  File "W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\src\generate_dataset.py", line 24
    answer = f"{a}+{b} равно {a+b}"
                                   ^
IndentationError: unindent does not match any outer indentation level
```

Python увидел строку с отступом, который не совпадает ни с одним из “уровней” отступа выше по коду.
Чаще всего причина: смешаны Tab и пробелы, или у одной строки “кривое” количество пробелов.


## Problem with TabSize

G-AI: vscode tab size setting

2. Language-Specific Settings
You can define different tab sizes for different programming languages (e.g., 2 for JavaScript, 4 for Python): 

Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P).
Search for "Preferences: Configure Language Specific Settings..." and select your language.
Add the following to the JSON file:

```json
"[python]": {
    "editor.tabSize": 2
}
```

## vscode python formatter

Install autopep8 extension

Все переехал форматировщиком - стало заметно лучше


## Problem with saved *.JSONL file

```
как сделать чтобы команда with open("dataset.jsonl", "w") as f: сохранила оригинальный кирилической текст, не кодируя его в \uXXX последовательности
```

Вот такой код:
```
def save(dataset):
    with open("dataset.jsonl", "w", encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
```

Объяснение:

# ensure_ascii=False в json.dumps() — это сохраняет кириллицу как обычный текст вместо Unicode escape последовательности
# encoding='utf-8' при открытии файла — явно указывает кодировку для сохранения символов


## Strange runtime error - TypeError: 'NoneType' object is not iterable

```
 File "W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\src\generate_dataset.py", line 57, in <module>
    save(data)
    ~~~~^^^^^^
  File "W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\src\generate_dataset.py", line 51, in save
    for item in dataset:
                ^^^^^^^
TypeError: 'NoneType' object is not iterable
```

Нужно исправить на:
```
def generate_dataset(n=300):
    return [generate_sample() for _ in range(n)]
```

Похоже `return` потерялся при редактировании, где-то ИИ его убрал пока я код правил и нажатие Tab это закрепило...


## Check if CUDA available

```
(.venv) PS W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning> python -c "import torch; print('cuda_available=', torch.cuda.is_available()); print('torch_cuda=', torch.version.cuda); print('device_count=', torch.cuda.device_count()); print('device0=', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"
cuda_available= False
torch_cuda= None
device_count= 0
device0= none
```

G-AI: install pytorch with cuda
  - https://pytorch.org/get-started/locally/
  - https://developer.nvidia.com/cuda-downloads
  - https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

Переустановка PyTorch:
```
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 
```

### error: Could not find a version that satisfies the requirement torch (from versions: none)

```
role: Python expert

context:
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 
  ERROR: Could not find a version that satisfies the requirement torch (from versions: none)
  ERROR: No matching distribution found for torch

task: объясни - почему такая ошибка возникает
```

Aha!
Нужно использовать другой Python! 3.12 (а лучше - 3.11)
```
py install 3.12
py -3.12 -m venv .venv312
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 
pip install -r requirements.txt
```

Ого! Размер среды - почти 5 Gb!...


## Problem: Запуск python .\src\training.py молча быстро завершается

ИИ:
```
role: Python developer
role: Python developer
task: инциализировать виртуальную среду для Python 3.12
```

Нашел проблему - завершается на строчке:

	from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, TrainerCallback

Пересоздал venv для 3.12...
команды:
```
python --version; py -3.12 --version 2>$null; python3.12 --version 2>$null
```

потом:
```
py -3.12 -m venv .venv
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
```

Похоже, не идет тренировка...

потом:
```
py -3.11 -m venv .venv
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
```

Запустил...
Все равно - оно вроде как висит...

