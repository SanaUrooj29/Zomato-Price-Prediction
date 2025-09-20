import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os

app = Flask(__name__)

# Load model with error handling
try:
    if os.path.exists('model.pkl'):
        model = pickle.load(open('model.pkl', 'rb'))
    else:
        print("Warning: model.pkl not found. Please run model.py to generate the model.")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if model is None:
        return render_template('index.html', prediction_text='Error: Model not loaded. Please contact administrator.')
    
    try:
        features = [int(x) for x in request.form.values()]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        output = round(prediction[0], 1)

        return render_template('index.html', prediction_text='Your Rating is: {}'.format(output))
    except Exception as e:
        return render_template('index.html', prediction_text='Error: Invalid input or prediction failed.')

if __name__ == "__main__":
    app.run(debug=True)