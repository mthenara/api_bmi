from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the BMI Calculator API!"})

@app.route('/bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    weight = data.get('weight')  # in kg
    height = data.get('height')  # in cm

    if not weight or not height:
        return jsonify({"error": "Both weight (kg) and height (cm) are required!"}), 400

    try:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        return jsonify({
            "bmi": bmi,
            "category": category
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
