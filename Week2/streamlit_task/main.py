import streamlit as st
import joblib
import pandas as pd

@st.cache(allow_output_mutation=True)
def load_model():
    # Load your trained model
    model = joblib.load("C:/Users/PC/Desktop/task2/regression_model.joblib")
    return model

def predict_charges(age, sex, bmi, children, smoker, region, model):
    # Convert input values to dataframe
    region_mapping = {'southwest': 3, 'southeast': 2, 'northwest': 1}
    data = pd.DataFrame({
        'age': [age],
        'sex': [0 if sex == 'female' else 1],
        'bmi': [bmi],
        'children': [children],
        'smoker': [1 if smoker == 'yes' else 0],
        'region': [region_mapping.get(region, 0)]  # Assign 0 if region is not one of the specified options
    })

    # Make prediction using the model
    prediction = model.predict(data)[0]

    # Return the predicted charges
    return prediction

# Create the Streamlit web app
def main():
    st.title("Medical Charges Prediction")
    st.write("Enter the following information to predict medical charges:")

    # Load the model
    model = load_model()

    # Get user input
    age = st.number_input("Age", min_value=1, max_value=100, value=30)
    sex = st.selectbox("Sex", ["male", "female"])
    bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
    children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

    if st.button("Predict Charges"):
        # Perform prediction
        charges = predict_charges(age, sex, bmi, children, smoker, region, model)

        # Display result
        st.write("Predicted Charges: $", round(charges, 2))

# Run the app
if __name__ == "__main__":
    main()