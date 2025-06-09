from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def hitung_bmi(weight, height):
    if not weight or not height:
        return None, "Both weight and height are required."
    try:
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        return {"bmi": bmi, "category": category}, None
    except Exception as e:
        return None, str(e)

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    if request.method == 'POST':
        data = request.get_json()
        weight = data.get('weight')
        height = data.get('height')
    else:  # GET
        weight = request.args.get('weight', type=float)
        height = request.args.get('height', type=float)

    result, error = hitung_bmi(weight, height)

    if error:
        return jsonify({"error": error}), 400
    return jsonify(result)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to BMI API. Use /bmi via GET or POST with weight and height."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
