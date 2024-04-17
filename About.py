import streamlit as st
from streamlit_lottie import st_lottie
import requests

col1, col2 = st.columns([1, 1])

with col1:
    # Page title and team members
    st.title("Invoice OCR 🔍")
    st.subheader("_Prototype by team: MIRAGE")

    # Home page content
    st.markdown("<p style='color: orange;'>Welcome to the Invoice OCR application!</p>", unsafe_allow_html=True)

    st.markdown("This project helps :violet[businesses] extract key information from **invoices** :green[quickly] and :blue[efficiently]. ️ Simply upload an invoice image and our AI model will automatically extract data and save it to realtime database. 🪄")
    st.markdown(":green[Navigate to the ***'Home'*** page to get started!] 🚀")
    st.caption("The application utilizes Google's Generative AI model and Streamlit for a user-friendly experience. ")

with col2:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_hello = load_lottieurl("https://lottie.host/b7e226d3-a329-439b-8967-9d9fdd8804c7/WLt0EEr6RN.json")

    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",
        width=400,
        key=None,
    )
