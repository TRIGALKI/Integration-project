from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
import glob
import logging

# Настройка логгера для более информативных сообщений об ошибках
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Глобальный словарь для хранения загруженных моделей
# Ключи - версии ('1', '2'), значения - сами объекты моделей
LOADED_MODELS = {}

def load_models():
    """
    Ищет и загружает все файлы моделей в формате 'model_*.pkl' из папки '../models/'.
    Возвращает словарь с моделями, где ключ - версия модели.
    """
    models_dir = '../models/'
    models = {}
    try:
        # Находим все файлы, соответствующие шаблону
        model_files = glob.glob(os.path.join(models_dir, 'model_*.pkl'))
        
        if not model_files:
            logging.warning(f"Нет файлов моделей, найденных в папке {models_dir}")
            return models

        for model_file in model_files:
            # Извлекаем номер версии из имени файла (например, из 'model_2.pkl' -> '2')
            version = os.path.basename(model_file).replace('model_', '').replace('.pkl', '')
            
            logging.info(f"Загрузка модели версии {version} из файла {model_file}...")
            with open(model_file, 'rb') as f:
                models[version] = pickle.load(f)
        
        logging.info(f"Успешно загружены модели: {list(models.keys())}")
        return models

    except FileNotFoundError as e:
        logging.error(f"Папка с моделями не найдена: {e}")
        return models
    except Exception as e:
        logging.error(f"Произошла ошибка при загрузке моделей: {e}")
        return models

# --- Загрузка моделей при старте приложения ---
# Вызываем функцию и сохраняем результат в глобальную переменную
LOADED_MODELS = load_models()


@app.route('/predict', methods=['POST'])
def predict():
    """Эндпоинт для предсказания с выбором версии модели."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Запрос не содержит JSON-данных'}), 400

        # Получаем версию модели из запроса. По умолчанию - первая доступная.
        # Если модели не загружены, default будет None.
        model_version = data.get('model_version', next(iter(LOADED_MODELS), None))

        if not model_version or model_version not in LOADED_MODELS:
            available_versions = list(LOADED_MODELS.keys())
            return jsonify({
                'error': f'Модель версии {model_version} не найдена. Доступные версии: {available_versions}.'
            }), 400

        # Извлекаем данные для предсказания, исключая служебный параметр
        input_data = {k: v for k, v in data.items() if k != 'model_version'}
        features = preprocess_input(input_data)

        selected_model = LOADED_MODELS[model_version]

        prediction = selected_model.predict(features)
        probability = selected_model.predict_proba(features)[0][1]

        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'model_version': model_version
        })

    except Exception as e:
        app.logger.error(f"Ошибка при обработке запроса: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервиса и доступности моделей."""
    if LOADED_MODELS:
        return jsonify({'status': 'healthy', 'loaded_models': list(LOADED_MODELS.keys())}), 200
    else:
        return jsonify({'status': 'unhealthy', 'error': 'Модели не загружены'}), 503


def preprocess_input(data):
    """Преобразует словарь входных данных в numpy-массив."""
    # Сортировка ключей важна для сохранения порядка признаков!
    features = np.array([data[key] for key in sorted(data.keys())]).reshape(1, -1)
    return features


if __name__ == '__main__':
    # Модели загружаются здесь один раз при запуске скрипта
    app.run(host='0.0.0.0', port=5000, debug=False)