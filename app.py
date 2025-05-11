import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time


#should put these in a utils include
from rapidfuzz import process # for querying df
from millify import millify


# going to ease a manual list of dictionaries for now, before building the web scraping bot
# each index of the list is a dictionary that represents a gpu
# each gpu will have a name, vram, cuda cores, boos clock, power usage, etc. (performance specs only, no release year etc.)

# SHOULD be easier to convert this stuff to json or whatever and however that works


    # {
    #     "name": "",
    #     "boost_clock (ghz)": ,
    #     "base_clock": , 
    #     "vram (gb)": ,
    #     "cuda_cores": ,
    #     "power (watts)": 
    # },


# i want to add a picutre too^^^ AND MSRP
# average fps across games

gpu_specs = [

    {
        "name": "NVIDIA Geforce RTX 5070",
        "boost_clock (ghz)": 2.51,
        "base_clock": 2.33, 
        "vram (gb)": 12,
        "cuda_cores": 6144,
        "power (watts)": 650
    },
    {
        "name": "NVIDIA Geforce RTX 5070 Ti",
        "boost_clock (ghz)": 2.45,
        "base_clock": 2.3, 
        "vram (gb)": 16,
        "cuda_cores": 8960,
        "power (watts)": 750
    },
    {
        "name": "NVIDIA GeForce RTX 1060",
        "boost_clock (ghz)": 1.70,
        "base_clock": 1.50, 
        "vram (gb)": 6,
        "cuda_cores": -1,
        "power (watts)": 300
    },
    {
        "name": "AMD Radeon RX 9070 XT",
        "boost_clock (ghz)": 2.97,
        "base_clock": 2.40, 
        "vram (gb)": 16,
        "cuda_cores": -1,
        "power (watts)": 750
    }
]

# will change this a json import later
df = pd.DataFrame(data=gpu_specs).set_index("name")
names = df.index.tolist()

# save this for later, could be cool for a chatbot
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# === Application ===


st.title("Hello, welcome to :blue[SpecScraper]! :wave:", anchor=None)

st.write("Enter two GPUs to compare below..")




left, right = st.columns(2)

# using st's selectbox query, finds strings of each gpu

gpu_1 = left.selectbox(
            "empty1",
            names, 
             placeholder="Enter a GPU...", 
             label_visibility="collapsed"
             )

gpu_2 = right.selectbox(
            "empty2",
            names, 
             placeholder="Enter a GPU...", 
             label_visibility="collapsed"
             )



if gpu_1.strip() and gpu_2.strip():     #.strip() will ignore whitespace, this control flow will only trigger once both parameters are entered
    
    # st.write(f"Comparing {gpu_1} and {gpu_2}")
 
    specs_1 = df.loc[gpu_1].to_dict() # convert each series to a python dict
    specs_2 = df.loc[gpu_2].to_dict()

    # === Comparing dashboard happens here ===

    # delta = percent difference between two specs, calculated with max(left, right) / min(left, right)

    st.write("Boost Clock Speed")
    left, right = st.columns(2) # must be reset for rendering purposes

    # boost clock frequency

    boost_1 = specs_1["boost_clock (ghz)"]
    boost_2 = specs_2["boost_clock (ghz)"]

    delta = ( ( max(boost_1, boost_2) / min(boost_1, boost_2) ) - 1 ) * 100.0
    delta = round(delta, 2)

    if boost_1 > boost_2:
        left.metric(label="", label_visibility="collapsed", value=str(boost_1) + " GHz",  delta=str(delta) + "%")
        right.metric(label="", label_visibility="collapsed", value=str(boost_2) + " GHz",  delta="")
    elif boost_1 < boost_2:
        left.metric(label="", label_visibility="collapsed", value=str(boost_1) + " GHz",  delta="")
        right.metric(label="", label_visibility="collapsed", value=str(boost_2) + " GHz", delta=str(delta) + "%")
    else:
        left.metric(label="", label_visibility="collapsed", value=str(boost_1) + " GHz", )
        right.metric(label="", label_visibility="collapsed", value=str(boost_2) + " GHz",)


    # cuda cores

    st.write("Other Spec")
    left, right = st.columns(2) # must be reset for rendering purposes
    
    left.metric("CUDA Cores", millify( specs_1["cuda_cores"] , precision=2), border=True)
    right.metric("CUDA Cores", millify( specs_2["cuda_cores"] , precision=2), border=True)

    