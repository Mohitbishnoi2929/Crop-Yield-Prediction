from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle

#loading models
Rs=pickle.load(open('Rs.pkl','rb'))
preprocessor=pickle.load(open('preprocessor.pkl','rb'))

# creating flask app

app= Flask(__name__)

@app.route('/')
def index() :
    return  render_template('index.html')
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        Area = request.form['Area']
        Item = request.form['Item']
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        avg_temp =request.form['avg_temp']
        Pesticide_in_tonnes = request.form['Pesticide_in_tonnes']

        features = np.array([[Area, Item, Year, average_rain_fall_mm_per_year, avg_temp, Pesticide_in_tonnes]],
                            dtype=object)

        transformed_features = preprocessor.transform(features)
        predicted_value = Rs.predict(transformed_features).reshape(1, -1)

        return render_template('index.html',predicted_value=predicted_value)


#python main

if __name__=='__main__':
    app.run(debug=True)
