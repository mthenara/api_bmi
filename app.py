from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
  <title>BMI Calculator</title>
</head>
<body>
  <h2>BMI Calculator</h2>
  <form method="POST" action="/bmi">
    <label>Weight (kg):</label><br>
    <input type="number" name="weight" step="0.1" required><br><br>
    <label>Height (cm):</label><br>
    <input type="number" name="height" step="0.1" required><br><br>
    <button type="submit">Calculate BMI</button>
  </form>
  {% if bmi %}
    <h3>Result:</h3>
    <p>BMI: {{ bmi }}</p>
    <p>Category: {{ category }}</p>
  {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the BMI Calculator API!"})

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    if request.method == 'POST':
        try:
            # Coba ambil dari form dulu
            weight = float(request.form.get('weight', 0))
            height = float(request.form.get('height', 0))
        except:
            return "Invalid input.", 400

        if not weight or not height:
            return "Both weight and height are required.", 400

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

        return render_template_string(HTML_FORM, bmi=bmi, category=category)

    # GET method – just show form
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
