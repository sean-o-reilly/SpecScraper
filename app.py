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

# takes in a dict with each gpu's specs, and unit of measurement, spec name for writing
def compare_spec(s1, s2, query_index, unit, spec_name, large_val=False):
    st.write(spec_name)
    left, right = st.columns(2)

    # boost clock frequency

    val_1 = s1[query_index] # ex. "cuda_cores" index of the dict
    val_2 = s2[query_index]

    # protection from divide by zero and other delta errors
    if (val_1 == -1 or val_1 == 0) or (val_2 == -1 or val_2 == 0):


        if val_1 == -1: 
            left.metric("", label_visibility="collapsed", value="N/A")
        else:
            if large_val:
                left.metric("", label_visibility="collapsed", value=str(millify(val_1, precision=2)) + " " + unit, )
            else:
                left.metric("", label_visibility="collapsed", value=str(val_1) + " " + unit, )

        if val_2 == -1: 
            right.metric("", label_visibility="collapsed", value="N/A")
        else:
            if large_val:
                right.metric("", label_visibility="collapsed", value=str(millify(val_2, precision=2)) + " " + unit, )
            else:
                right.metric("", label_visibility="collapsed", value=str(val_2) + " " + unit, )

        return
    

    # assuming two valid specs to compare

    delta = ( ( max(val_1, val_2) / min(val_1, val_2) ) - 1 ) * 100.0
    delta = round(delta, 2)

    if large_val == True: #display numbers as 1.23k instead of 1,230
        if val_1 > val_2:
            left.metric("", label_visibility="collapsed", value=str( millify(val_1, precision=2) ) + " " + unit,  delta=str(delta) + "%")
            right.metric("", label_visibility="collapsed", value=str( millify(val_2, precision=2) ) + " " + unit,  delta="")
        elif val_1 < val_2:
            left.metric("", label_visibility="collapsed", value=str(millify(val_1, precision=2)) + " " + unit,  delta="")
            right.metric("", label_visibility="collapsed", value=str(millify(val_2, precision=2)) + " " + unit, delta=str(delta) + "%")
        else:
            left.metric("", label_visibility="collapsed", value=str(millify(val_1, precision=2)) + " " + unit, )
            right.metric("", label_visibility="collapsed", value=str(millify(val_2, precision=2)) + " " + unit,)
    else:
        if val_1 > val_2:
            left.metric("", label_visibility="collapsed", value=str(val_1) + " " + unit,  delta=str(delta) + "%")
            right.metric("", label_visibility="collapsed", value=str(val_2) + " " + unit,  delta="")
        elif val_1 < val_2:
            left.metric("", label_visibility="collapsed", value=str(val_1) + " " + unit,  delta="")
            right.metric("", label_visibility="collapsed", value=str(val_2) + " " + unit, delta=str(delta) + "%")
        else:
            left.metric("", label_visibility="collapsed", value=str(val_1) + " " + unit, )
            right.metric("", label_visibility="collapsed", value=str(val_2) + " " + unit,)

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
 
    spec_1 = df.loc[gpu_1].to_dict() # convert each series to a python dict
    spec_2 = df.loc[gpu_2].to_dict()

    # === Comparing dashboard happens here ===

    compare_spec(spec_1, spec_2, "boost_clock (ghz)", "GHz", "Boost Clock Frequency")
    compare_spec(spec_1, spec_2, "cuda_cores", "", "CUDA Cores", large_val=True)

    

    