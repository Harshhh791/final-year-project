from flask import Flask, render_template, request
import joblib
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import RandomOverSampler
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, static_folder="static")

# ================== 🔥 Load Models & Firebase Setup ==================
MODEL_PATH = "H:/Last year/Scholarship_Prediction/Scholarship_Prediction/model.pkl"
SCALER_PATH = "H:/Last year/Scholarship_Prediction/Scholarship_Prediction/scaler_tensorflow.pkl"
LABEL_ENCODER_PATH = "H:/Last year/Scholarship_Prediction/Scholarship_Prediction/label_encoder.pkl"
TENSORFLOW_MODEL_PATH = "H:/Last year/Scholarship_Prediction/Scholarship_Prediction/my_model.h5"
FIREBASE_CONFIG_PATH = "H:/Last year/Scholarship_Prediction/Scholarship_Prediction/firebase_config.json"

with open(MODEL_PATH, 'rb') as f:
    loaded_model = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    loaded_scaler = pickle.load(f)

with open(LABEL_ENCODER_PATH, 'rb') as f:
    label_encoder = pickle.load(f)

tensorflow_model = tf.keras.models.load_model(TENSORFLOW_MODEL_PATH)

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CONFIG_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ================== 🔢 Preprocess Input Function ==================
def preprocess_input(input_dict):
    myList = []
    x = input_dict

    required_list = [
        'GPA', '10th Percentage', '12th Percentage', 'Family Income',
        'Extracurricular Activities_high', 'Extracurricular Activities_low', 'Extracurricular Activities_medium',
        'Essay Quality_excellent', 'Essay Quality_fair', 'Essay Quality_good', 'Essay Quality_poor',
        'Letters of Recommendation_moderate', 'Letters of Recommendation_strong', 'Letters of Recommendation_weak',
        'Financial Need_high', 'Financial Need_low', 'Financial Need_medium',
        'Major_Arts', 'Major_Business', 'Major_Engineering', 'Major_Medicine', 'Major_Science',
        'State of Residence_Delhi', 'State of Residence_Karnataka', 'State of Residence_Kerala',
        'State of Residence_Maharashtra', 'State of Residence_Tamil Nadu', 'State of Residence_Uttar Pradesh',
        'Leadership Experience_no', 'Leadership Experience_yes',
        'Volunteer Work_no', 'Volunteer Work_yes',
        'Work Experience_no', 'Work Experience_yes',
        'Family Background_high', 'Family Background_low', 'Family Background_medium'
    ]

    for cols in required_list:
        if cols in ['GPA', '10th Percentage', '12th Percentage', 'Family Income']:
            myList.append(float(x.get(cols, 0)))  # Convert to float, default 0 if missing
        elif cols.split("_")[0] in x:
            myList.append(1 if cols.split("_")[1] == x[cols.split("_")[0]] else 0)

    input_df_scaled = loaded_scaler.transform([myList])
    return input_df_scaled

# ================== 🌐 Routes ==================
@app.route('/')
def start():
    return render_template("login.html")

@app.route('/prediction.html')
def prediction():
    return render_template("prediction.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/faq.html')
def faq():
    return render_template("faq.html")

@app.route('/login.html')
def login():
    return render_template("login.html")

@app.route('/signup.html')
def signup():
    return render_template("signup.html")

# ================== 🎯 Prediction Route ==================
@app.route('/predict', methods=['POST'])
def predict():
    student_data = request.form.to_dict()
    input_data_scaled = preprocess_input(student_data)
    predictions = tensorflow_model.predict(input_data_scaled)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_class_label = label_encoder.inverse_transform([predicted_class])[0]
    return render_template("prediction.html", prediction=predicted_class_label)

# ================== 📌 Scholarships Route ==================
@app.route('/scholarships.html')
def scholarships():
    scholarships_ref = db.collection("scholarship")  # Ensure correct Firestore collection
    docs = scholarships_ref.stream()
    scholarships_list = [doc.to_dict() for doc in docs]
    return render_template("scholarships.html", scholarships=scholarships_list)

# ================== 🚀 Run Flask ==================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
