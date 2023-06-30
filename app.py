import streamlit as st
import requests
import os
from streamlit_lottie import st_lottie
import whisper
import openai
from dotenv import load_dotenv

#openai
load_dotenv()
openai.api_key = os.getenv('OPEN_AI_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


st.set_page_config(page_title="Speech Ordering", page_icon="🍜",layout='wide')

##Header Section
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Welcome to the Speech Ordering Restaurant!</h1>
    </div>
    """,
    unsafe_allow_html=True
)
##lottie
def load_lottieurl(url):
    r= requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

##LOAD GIF
lotties= load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_3GIrwN3h0z.json")

#whisper
model = whisper.load_model('base')


with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        audio_file = st.file_uploader("Upload Audio", type=['mp3'])
        if st.button('Transcribe Audio'):
            if audio_file is not None:
                st.success('Transcribing Audio', icon="✅")
                with st.spinner('Preparing order'):
                    transcription = model.transcribe(audio_file.name)
                    print(audio_file)
                    texts= transcription['text']

                    prompt=f"""From the following items from the order_text:
                    - Food items quantity for chef
                    - Order Summary for customer

                    order_text : '''{texts}'''
                    """
                    response = get_completion(prompt)
                    st.markdown(response)
            else:
                st.error('please upload audio .mp3 file')

    with col2:
        st_lottie(lotties,height=300, key="coding")




st.write("Enjoy your meal!")

