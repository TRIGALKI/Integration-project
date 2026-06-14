# Integration-project

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Project with model implementation for mifi task

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         integration_project and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── integration_project   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes integration_project a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------
## Быстрый старт (локальный запуск)

### 1. Установка зависимостей

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Обучить модели

Прогоняем ноутбук [`notebooks/Models fitting vers.ipynb`](Models fitting vers.ipynb)

Результат: `models/model_v1.plk`, `models/model_v2.pkl`в папке 'models'

### 3. Запустить сервис

```bash
python app/api.py
```


---
## Примеры запросов к API (curl-команды).
```
curl -X GET http://172.17.0.2:5000/health
ответ {"loaded_models":["2","1"],"status":"healthy"}

curl -X POST http://172.17.0.2:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "model_version": "1",
           "LIMIT_BAL": 20000,
           "SEX": 2,
           "EDUCATION": 2,
           "MARRIAGE": 1,
           "AGE": 35,
           "PAY_0": -1,
           "PAY_2": -1,
           "PAY_3": -1,
           "PAY_4": -1,
           "PAY_5": -1,
           "PAY_6": -1,
           "BILL_AMT1": 10000,
           "BILL_AMT2": 15000,
           "BILL_AMT3": 12000,
           "BILL_AMT4": 14000,
           "BILL_AMT5": 13000,
           "BILL_AMT6": 11000,
           "PAY_AMT1": 5000,
           "PAY_AMT2": 6000,
           "PAY_AMT3": 5500,
         }'"PAY_AMT6": 5800,
ответ {"model_version":"1","prediction":1,"probability":1.0}

curl -X POST http://172.17.0.2:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "model_version": "2",
           "LIMIT_BAL": 20000,
           "SEX": 2,
           "EDUCATION": 2,
           "MARRIAGE": 1,
           "AGE": 35,
           "PAY_0": -1,
           "PAY_2": -1,
           "PAY_3": -1,
           "PAY_4": -1,
           "PAY_5": -1,
           "PAY_6": -1,
           "BILL_AMT1": 10000,
           "BILL_AMT2": 15000,
           "BILL_AMT3": 12000,
           "BILL_AMT4": 14000,
           "BILL_AMT5": 13000,
           "BILL_AMT6": 11000,
           "PAY_AMT1": 5000,
           "PAY_AMT2": 6000,
           "PAY_AMT3": 5500,
         }'"PAY_AMT6": 5800,
ответ {"model_version":"2","prediction":0,"probability":0.46}
```


## API: формат запросов и ответов
- Описание заросов и ответов приложения: [`API_doc.md`](API_doc.md)

## Docker

### Сборка и запуск одного образа



### Docker Hub

Страница образа на Docker Hub: [https://hub.docker.com/repository/docker/trigalki/web_app_v2/general]
```
docker pull trigalki/web_app_v2:latest
```

## Модели

| Версия | Алгоритм | Описание |
|---|---|---|
| v1 | LogisticRegression | Базовая интерпретируемая модель, быстрый инференс |
| v2 |RandomForestClassifier | Более сложная модель используется как challenger в A/B-тесте |


---

## Архитектура,метрики,Млопс инструменты, A/B-тест

- Подробное обоснование архитектурных решений: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- Описание Млопс интсрументов [`MLOPS.md`](MLOPS.md.md)
- Обосонвоание по выбору бизнес метрик [`Metrics.md`](Metrics.md)
- План A/B-тестирования: [`AB_TEST_PLAN.md`](AB_TEST_PLAN.md)

## Скриншоты работы приложения 
Клиентская часть (запуск скрипта test.py)
<img width="787" height="524" alt="image" src="https://github.com/user-attachments/assets/e0fb5ddb-8b44-4d07-bfe8-60015c860334" />

Запуск контейнера и логи работы серверной часть 
<img width="1377" height="567" alt="image" src="https://github.com/user-attachments/assets/1dbc7818-a721-4ede-bc56-676ecbc71b2f" />


