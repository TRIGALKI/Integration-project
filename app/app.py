from flask import Flask,request, jsonify 
import pickle 
import numpy as np
app = Flask(__name__)
# Загрузка подели при старте 
with open('../models/myfile.pkl', 'rb') as f: 
    model = pickle.load(f)
    
@app.route('/predict', methods=['POST'])
def predict():
    "- Эндпоинт Для предсказания дефолта-"
    try:
        data = request.get_json() 
        features = preprocess_input(data) 
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1]
        return jsonify ({'prediction': int(prediction[0]),
                         'probability': float(probability),
                         'model_version': 'v1'})
    except Exception as е:
        return jsonify({
            'error': str(e)}), 400
@app.route('/health', methods=['GET'])
def health():
    """Пpoвepкa здоровья сервиса"""
    return jsonify({'status': 'healthy'}), 200
    
def preprocess_input(data):
    "Предобработка входных данных"
    #Преобразование JS0N 6 numpy arra 
    features = np.array([data[key] for key in sorted(data.keys())]).reshape(1, -1) 
    return features
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)