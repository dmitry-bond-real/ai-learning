
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

шаг 3:
```

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
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

Запустил...
Все равно - оно вроде как висит...


## Пишет
```
config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 608/608 [00:00<00:00, 606kB/s]
W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\.venv\Lib\site-packages\huggingface_hub\file_download.py:138: 
	UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files 
	but your machine does not support them in W:\edu\Larchanka\2026-04-06-AI\L07\fine-tuning\src\model_cache\models--TinyLlama--TinyLlama-1.1B-Chat-v1.0. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
```


## Пытался указать dataloader_num_workers=14

Оказывается оно тупо запускает кучу копий того же самого training.py в итоге выходит фигня!
Сначала пришлось переделать чтобы все занести внутрь функции main,
а потом все равно вернуть dataloader_num_workers=0


## Пытался указать torch.set_num_threads() и torch.set_num_interop_threads()

Ну да, оно создало процесс Python с кучей потоков. На старте оно использует 100% CPU, 
а потом откатывается на %5 CPU и так висит...

Папка tinyllama-json остается пустой...


## Что пишет TaskInfo

```
|Protocol| |State|       |Loc Name|   |Loc Port||Rem Name|                                    |Rem Port|
Tcp        ESTABLISHED   BtoTestWs        47648 server-108-138-51-21.waw51.r.cloudfront.net   https 
Tcp        CLOSE_WAIT    BtoTestWs        47649                                                
```

Куда-то оно ходит... зачем-то...


## Советуют intel-extension-for-pytorch

```
pip install intel-extension-for-pytorch
ERROR: Could not find a version that satisfies the requirement intel-extension-for-pytorch (from versions: none)
ERROR: No matching distribution found for intel-extension-for-pytorch
```

Другая команда:
```
python -m pip install intel-extension-for-pytorch --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

Info:
- Supported Versions: Generally Python 3.9, 3.10, 3.11, or 3.12.
- Check your version with python --version and ensure you are using a 64-bit installation.

Verify OS and Hardware
- Linux/WSL2: IPEX is primarily supported on Linux. Windows users should use WSL2 for full GPU (XPU) support.
- Native Windows: Native Windows support is limited to specific hardware like Intel® Arc™ GPUs. 

**Important Note:** Intel has announced that IPEX will be retired by **March 2026**, as its features are being upstreamed directly into [native PyTorch](https://pytorch.org/get-started/locally/). Moving forward, Intel recommends using standard PyTorch for Intel hardware support.


## CUDA validation

Python пишет - AssertionError: Torch not compiled with CUDA enabled


```
> nvcc.exe --version
C:\…gram Files\NVIDIA GPU Computing Toolkit\CUDA\v13.2\bin>nvcc.exe --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2026 NVIDIA Corporation
 #Built on Thu_Mar_19_22:28:55_Pacific_Daylight_Time_2026
Cuda compilation tools, release 13.2, V13.2.78
Build cuda_13.2.r13.2/compiler.37668154_0
```

Предлагает тоже самое:
```
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Теперь оно молча отваливается сразу после надписи "Creating tokenizer..."
Похоже это именно torch с поддержкой CUDA валиться...

