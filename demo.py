import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



st.title("Hello, welcome to SpecScraper!")

st.write("Enter two GPU's to compare below..")

gpu_1 = st.text_input("GPU 1:")
gpu_2 = st.text_input("GPU 2:")


if gpu_1.strip() and gpu_2.strip():     #.strip() will ignore whitespace, this control flow will only trigger once both parameters are entered
    if st.button(f"Compare {gpu_1} and {gpu_2}"): # button might be unnessacararary or however you spell it
        st.write(f"Comparing {gpu_1} and {gpu_2}")

