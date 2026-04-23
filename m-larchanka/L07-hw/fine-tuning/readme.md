
# Intro

На 7й лекции задали - выполнить fine-tuning для модели...


# Questions

## Где он берет указанную модель?! На каком сервисе?!

компонент: AutoTokenizer 
ответ: на HugginFace... и может кэшировать локально.


## Нужно ли установить torch чтобы использовал CUDA ?

Для Python 3.14 - нет, не поддерживается!
Только для 3.12, а лучще - 3.11


# Materials/See Also

- https://huggingface.co/docs/transformers/main_classes/trainer


