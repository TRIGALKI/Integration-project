import requests
import json

# --- Конфигурация ---
API_URL = 'http://172.17.0.2:5000'
ENDPOINT_PREDICT = '/predict'

# Пример данных для предсказания (замените на реальные)
# Ключи должны быть отсортированы по алфавиту,
# чтобы соответствовать логике preprocess_input в вашем Flask-приложении
payload_data  = {
    #"model_version": "v2", # Указываем версию по умолчанию
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
    "PAY_AMT4": 6500,
    "PAY_AMT5": 6200,
    "PAY_AMT6": 5800
}

if __name__ == '__main__':
    # Часть 1: Проверка доступности сервиса
    print("--- [Шаг 1] Проверка здоровья сервиса ---")
    health_response = requests.get(f'{API_URL}/health')
    print(f"Статус проверки здоровья: {health_response.status_code}")
    
    if health_response.status_code != 200:
        print("Сервис недоступен. Не удалось провести тестирование.")
        exit()
        
    loaded_models = health_response.json().get('loaded_models', [])
    print(f"Доступные версии моделей на сервере: {loaded_models}\n")

    # Убедимся, что нужные нам версии доступны
    required_versions = ['1', '2']
    for version in required_versions:
        if version not in loaded_models:
            print(f"Версия модели '{version}' не найдена на сервере. Тестирование невозможно.")
            exit()

    # Часть 2: Отправка запросов к моделям v1 и v2
    print("--- [Шаг 2] Сравнение предсказаний моделей v1 и v2 ---")

    results = {}
    for model_ver in required_versions:
        print(f"\n- Запрос к модели версии: {model_ver}")
        payload = {"model_version": model_ver, **payload_data}
        
        try:
            response = requests.post(f'{API_URL}{ENDPOINT_PREDICT}', json=payload)
            
            print(f"  Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                result_json = response.json()
                # Сохраняем ключевые метрики для сравнения
                results[model_ver] = {
                    'prediction': result_json['prediction'],
                    'probability': result_json['probability']
                }
                print(f"  Предсказание: {result_json['prediction']}, Вероятность дефолта: {result_json['probability']:.4f}")
            else:
                print(f"  Ошибка сервера: {response.text}")
                
        except Exception as e:
            print(f"  Произошла ошибка при запросе: {e}")

    # Часть 3: Вывод сравнительного результата
    print("\n--- [Шаг 3] Итоговое сравнение ---")
    if '1' in results and '2' in results:
        prob_v1 = results['1']['probability']
        prob_v2 = results['2']['probability']
        diff = prob_v2 - prob_v1

        print(f"Сравнение вероятностей:")
        print(f"  Модель v1: {prob_v1:.4f}")
        print(f"  Модель v2: {prob_v2:.4f}")
        print(f"  Разница (v2 - v1): {diff:.4f}")

        if diff > 0:
            print("Результат: Новая модель (v2) оценивает риск дефолта как более высокий.")
        elif diff < 0:
            print("Результат: Новая модель (v2) оценивает риск дефолта как более низкий.")
        else:
            print("Результат: Обе модели выдали одинаковую оценку вероятности.")