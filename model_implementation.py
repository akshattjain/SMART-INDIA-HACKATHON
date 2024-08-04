from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
import joblib

model = tf.keras.models.load_model("Model/saved_model/my_model")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    scaler = joblib.load("scaler.save") 

    latitude = float(request.form('LAT'))
    longitude = float(request.form('LONG'))
    location = list(request.form('LOC')).split(',')
    city = location[-3]
    state = location[-2]

    andhra = 0
    telangana = 0
    kerala = 0
    tamil = 0

    if(state.lower() == 'andhra pradesh'):
        andhra = 1
    elif state.lower() == 'telangana':
        telangana = 1
    elif state.lower() == 'kerala':
        kerala = 1
    elif state.lower() == 'tamil nadu':
        tamil = 1

    l = ['Allapuzha', 'Chennai',
       'Cuddalore', 'Dharmapuri', 'Dindigul',
       'Dindugal', 'Ernakkulam', 'Hyderabad',
       'Idukki', 'Kancheepuram', 'Kannur',
       'Kanyakumari', 'Kasargod', 'Kollam',
       'Kottayam', 'Kozhikode', 'Krishnagiri',
       'Madurai', 'Malappuram', 'Medak',
       'Palakkad', 'Pathanamthitta', 'Ranga Reddy',
       'Salem', 'Theni', 'Thiruvannamalai',
       'Tirunelveli', 'Tiruvallur', 'Trissur',
       'Trivandrum', 'Tuticorin', 'Vellore',
       'Villupuram', 'Virudhunagar',
       'Visakhapatnam', 'Wayanad']
    
    dic = {i:0 for i in l}

    
    for i in dic.keys:
        if i.lower() in city.lower():
            dic.values[i] = 1
    
    input_data = np.array(latitude, longitude, andhra, kerala, tamil, telangana)
    input_data = np.append(input_data, list(dic.values()))
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    prediction = scaler.inverse_transform(prediction)

    output_ph = '{0:{1}f}'.format(prediction[0][0])
    output_EC = '{0:{1}f}'.format(prediction[0][1])
    output_CO3 = '{0:{1}f}'.format(prediction[0][2])
    output_HCO3= '{0:{1}f}'.format(prediction[0][3])
    output_Cl= '{0:{1}f}'.format(prediction[0][4])
    output_SO4='{0:{1}f}'.format(prediction[0][5])
    output_NO3='{0:{1}f}'.format(prediction[0][6])
    output_PO4='{0:{1}f}'.format(prediction[0][7])
    output_TH='{0:{1}f}'.format(prediction[0][8])
    output_Ca='{0:{1}f}'.format(prediction[0][9])
    output_Mg='{0:{1}f}'.format(prediction[0][10])
    output_Na='{0:{1}f}'.format(prediction[0][11])
    output_K='{0:{1}f}'.format(prediction[0][12])
    output_F='{0:{1}f}'.format(prediction[0][13])
    output_U_ppb='{0:{1}f}'.format(prediction[0][14])
    

    return jsonify({'pH': float(prediction[0][0])},
                   {'EC': float(prediction[0][1])},
                   {'CO3': float(prediction[0][2])},
                   {'HCO3': float(prediction[0][3])},
                   {'Cl': float(prediction[0][4])},
                   {'SO4': float(prediction[0][5])},
                   {'NO3': float(prediction[0][6])},
                   {'PO4': float(prediction[0][7])},
                   {'TH': float(prediction[0][8])},
                   {'Ca': float(prediction[0][9])},
                   {'Mg': float(prediction[0][10])},
                   {'Na': float(prediction[0][11])},
                   {'K': float(prediction[0][12])},
                   {'F': float(prediction[0][13])},
                   {'U(ppb)': float(prediction[0][14])},)

if __name__ == '__main__':
    app.run(debug=True)