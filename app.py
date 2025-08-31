import numpy as np
import pickle
import streamlit as st
from PIL import Image
import base64

# Hide Streamlit header
st.markdown("""
<style>
header[data-testid="stHeader"] {
    display: none;
}
.stApp > header {
    display: none;
}
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Load model
loaded_model = pickle.load(open('trained_model.sav', 'rb'))

# Function to set background image
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{get_base64_image()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 10px;
            margin-top: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_base64_image():
    try:
        with open("Parkinsons-Disease-600x404-1.jpg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Prediction function
def parkinsons_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    
    if prediction[0] == 0:
        return 'The person does not have Parkinsons disease'
    else:
        return 'The person has Parkinsons disease'

def main():
    set_background()
    
    st.title('Parkinsons Disease Prediction')
    
    # Input fields for all features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')
        fhi = st.text_input('MDVP:Fhi(Hz)')
        flo = st.text_input('MDVP:Flo(Hz)')
        jitter_percent = st.text_input('MDVP:Jitter(%)')
        jitter_abs = st.text_input('MDVP:Jitter(Abs)')
        rap = st.text_input('MDVP:RAP')
        ppq = st.text_input('MDVP:PPQ')
        jitter_ddp = st.text_input('Jitter:DDP')
    
    with col2:
        shimmer = st.text_input('MDVP:Shimmer')
        shimmer_db = st.text_input('MDVP:Shimmer(dB)')
        shimmer_apq3 = st.text_input('Shimmer:APQ3')
        shimmer_apq5 = st.text_input('Shimmer:APQ5')
        apq = st.text_input('MDVP:APQ')
        shimmer_dda = st.text_input('Shimmer:DDA')
        nhr = st.text_input('NHR')
        hnr = st.text_input('HNR')
    
    with col3:
        rpde = st.text_input('RPDE')
        dfa = st.text_input('DFA')
        spread1 = st.text_input('spread1')
        spread2 = st.text_input('spread2')
        d2 = st.text_input('D2')
        ppe = st.text_input('PPE')
    
    # Prediction
    diagnosis = ''
    
    if st.button('Parkinsons Test Result'):
        try:
            diagnosis = parkinsons_prediction([float(fo), float(fhi), float(flo), float(jitter_percent), float(jitter_abs),
                                             float(rap), float(ppq), float(jitter_ddp), float(shimmer), float(shimmer_db),
                                             float(shimmer_apq3), float(shimmer_apq5), float(apq), float(shimmer_dda),
                                             float(nhr), float(hnr), float(rpde), float(dfa), float(spread1), float(spread2),
                                             float(d2), float(ppe)])
        except ValueError:
            diagnosis = 'Please enter valid numeric values for all fields'
    
    st.success(diagnosis)

if __name__ == '__main__':
    main()