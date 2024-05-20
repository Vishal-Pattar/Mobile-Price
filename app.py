import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('mobile_model.pkl')

# DataFrame containing column names, min, and max values
column_data = {
    'column_name': ['Battery Power', 'Bluetooth', 'Clock Speed', 'Dual Sim', 'Front Camera Mega Pixel', '4G', 
                    'Interal Memory in GB', 'Mobile Depth in cm', 'Mobile weight', 'Number of Cores', 'Rear Camera Mega Pixels', 'Pixel Resolution Height', 
                    'Pixel Resolution Width', 'RAM in MB', 'Screen Height in cm', 'Screen Width in cm', 'Talk Time in hours', '3G', 
                    'Touch Screen', 'WiFi'],
    'min_value': [500, 0, 0.5, 0, 0, 0, 2, 0.1, 80, 1, 0, 0, 501, 263, 5, 0, 2, 0, 0, 0],
    'max_value': [1999, 1, 3.0, 1, 19, 1, 64, 1, 200, 8, 20, 1907, 1998, 3989, 19, 18, 20, 1, 1, 1]
}

column_df = pd.DataFrame(column_data)

# Create a sidebar for user input
st.sidebar.title('Enter Phone Features')

# List to store user inputs
user_inputs = []

for index, row in column_df.iterrows():
    col_name = row['column_name']
    min_val = row['min_value']
    max_val = row['max_value']
    print([min_val, max_val])
    if col_name in ['Bluetooth', 'Dual Sim', '4G', '3G', 'Touch Screen', 'WiFi']:
        option_values = ["No", "Yes"]
        value = option_values.index("No")  # Default value is "No"
        user_input = st.sidebar.selectbox(col_name, option_values, index=value)
        # Convert "Yes" to 1 and "No" to 0
        user_input = 1 if user_input == "Yes" else 0
    elif col_name in ['Clock Speed', 'Mobile Depth in cm']:
        user_input = st.sidebar.number_input(col_name, min_value=min_val, max_value=max_val, value=(min_val + max_val) / 2, step=0.1)
    else:
        user_input = st.sidebar.number_input(col_name, min_value=int(min_val), max_value=int(max_val), value=int(min_val), step=1, format='%d')
    user_inputs.append(user_input)

print("User inputs => ", user_inputs)
# Make prediction
prediction = model.predict([user_inputs])[0]

prediction_labels = ["Budget", "Mid-range", "High-end", "Premium"]

# Display prediction
st.title('Phone Price Prediction')
st.write('Predicted Price:', prediction_labels[prediction])
