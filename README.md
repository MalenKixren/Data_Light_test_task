# Тестовое задание Python Data Engineering

Скрипты запускаются из корневой папки проекта. Виртуальное окружение должно быть активировано. Используется только стандартная библиотека Python 

pipenv shell - для активации окружения

## Задание 1: XML

Исходные XML находятся в `task_train\task_train`.

Запуск:

1) Скрипт 1: Общая статистика - `python .\task1\general_statistics.py --input-dir ".\task_train\task_train"`
2) Скрипт 2: Статистика по классам - `python .\task1\class_statistics.py --input-dir ".\task_train\task_train"`
3) Скрипт 3*: Статистика по типам фигур - `python .\task1\figure_type_statistics.py --input-dir ".\task_train\task_train"`
4) Скрипт 4: Модификация XML-файлов `python .\task1\modify_xml.py --input-dir ".\task_train\task_train" --output-dir ".\task1\modified_xml"`


## Задание 2: COCO-датасет


Исходные файлы СОСО датасета находятся в папке: `task_train\task_train\task_train_coco 1.0`


Запуск:

 `set "COCO=task_train\task_train\task_train_coco 1.0" `

1) Скрипт 1: Реструктуризация датасета -  `python task2\restructure_dataset.py --images-dir "%COCO%\images\train" --annotations "%COCO%\annotations\instances_train.json" --output-dir "task2\restructured_dataset" `

2) Скрипт 2: Валидация и отчет по датасету -  `python task2\validate_dataset.py --dataset-dir "task2\restructured_dataset" `

3) Скрипт 3*: Преобразование в формат YOLO -  `python task2\coco_to_yolo.py --dataset-dir "task2\restructured_dataset" --output-dir "task2\yolo_dataset" `
