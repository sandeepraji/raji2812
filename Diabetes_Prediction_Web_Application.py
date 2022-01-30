# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 14:18:41 2022

@author: sandeep_n
"""

import numpy as np
import pickle
import streamlit as st
from PIL import Image


# loading the saved model
loaded_model = pickle.load(open('C:/Users\sandeep_n/.spyder-py3/trained_model1.sav', 'rb'))
image = Image.open("C:/Users/sandeep_n/.spyder-py3/Piramal_Swathya_logo.png")

#creating the funtion for prediction

def diabetes_prediction(input_data):

    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
      return 'The person is not diabetic'
    else:
      return 'The person is diabetic'
    


def main():
    
    # giving the title 
    st.image(image, caption=None, width=250, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    st.title('Sakhi Application',anchor=None)
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 28px;">Diabetes Prediction</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    
    # getting the input data from the user
    
    Pregnancies =st.text_input("Number of Pregnencies")
    Glucose =st.text_input("Glucose level")
    BloodPressure =st.text_input("BloodPressure value")
    SkinThickness =st.text_input("Enter the SkinThickness")
    Insulin =st.text_input("Insulin value")
    BMI =st.text_input("BMI value")
    DiabetesPedigreeFunction =st.text_input("DiabetesPedigreeFunction value")
    Age =st.text_input("Age of the Person")
    
    # Code for Prediction
    
    Diagnosis = ''
    
    # Creating the button for prediction
    
    if  st.button('Diabetes Test Result'):
        
        Diagnosis =diabetes_prediction([Pregnancies,Glucose,BloodPressure,
                                        SkinThickness,Insulin,BMI,
                                        DiabetesPedigreeFunction,Age])
        
    st.success(Diagnosis)


if __name__ == '__main__':
    main()
    
    
        
        
    
    
    
    
