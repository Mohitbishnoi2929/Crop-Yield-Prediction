from flask import Blueprint, request, render_template
import numpy as np
import pickle

# Create Blueprint
predict_bp = Blueprint('predict', __name__)

# Load models
Rs = pickle.load(open('Rs.pkl','rb'))
preprocessor = pickle.load(open('preprocessor.pkl','rb'))

@predict_bp.route('/predict', methods=['POST'])
def predict():
    Area = request.form['Area']
    Item = request.form['Item']
    Year = request.form['Year']
    Rainfall = request.form['average_rain_fall_mm_per_year']
    Temp = request.form['avg_temp']
    Pesticide = request.form['Pesticide_in_tonnes']

    features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
    transformed = preprocessor.transform(features)
    prediction = Rs.predict(transformed)

    return render_template('index.html', predicted_value=prediction[0])
