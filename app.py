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
    #     "boost_clock_ghz": ,
    #     "base_clock": , 
    #     "vram_gb": ,
    #     "cuda_cores": ,
    #     "power_watts": 
    # },


# i want to add a picutre too^^^ AND MSRP
# average fps across games

df = pd.read_json("data/gpu_specs.json").set_index("name")

df["boost_clock_ghz"] = df["boost_clock_ghz"].round(2) # fix floating point errors
names = df.index.tolist()

# save this for later, could be cool for a chatbot
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# takes in a dict with each gpu's specs, and unit of measurement, spec name for writing
def compare_spec(s1, s2, query_index, unit, spec_name, large_val=False, small_val=False, flip_weights=False, delta_color="normal", prefix=""):
    st.badge(spec_name)
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
                left.metric("", label_visibility="collapsed", value=prefix + str(millify(val_1, precision=2)) + " " + unit, )
            else:
                left.metric("", label_visibility="collapsed", value=prefix + str(val_1) + " " + unit, )

        if val_2 == -1: 
            right.metric("", label_visibility="collapsed", value="N/A")
        else:
            if large_val:
                right.metric("", label_visibility="collapsed", value=prefix + str(millify(val_2, precision=2)) + " " + unit, )
            else:
                right.metric("", label_visibility="collapsed", value=prefix + str(val_2) + " " + unit, )
        
        return
    

    # assuming two valid specs to compare

    # wouldn't make sense to say 12GB of RAM is "50%" more ram.. but maybe i should revert this later
    if small_val == True:
        delta = (abs(val_1 - val_2))
        delta = prefix + str(int(delta)) + " " + unit
        val_1 = int(val_1)
        val_2 = int(val_2)

    else:
        delta = ( ( max(val_1, val_2) / min(val_1, val_2) ) - 1 ) * 100.0
        delta = round(delta, 2)
        delta = prefix + str(delta) + "%"



    delta_pos = 0 # middle
    if val_1 > val_2: delta_pos = -1 # left
    if val_2 > val_1: delta_pos = 1 # right

    if delta_color == "inverse": 
        delta_pos *= -1 # flip direction
        delta = "-" + delta # flip arrow
    else:
        delta = "+" + delta


    if large_val == True: #display numbers as 1.23k instead of 1,230
        if delta_pos == -1:
            left.metric("", label_visibility="collapsed", value=prefix + str( millify(val_1, precision=2) ) + " " + unit,  delta=delta, delta_color=delta_color)
            right.metric("", label_visibility="collapsed", value=prefix + str( millify(val_2, precision=2) ) + " " + unit)
        elif delta_pos == 1:
            left.metric("", label_visibility="collapsed", value=prefix + str(millify(val_1, precision=2)) + " " + unit)
            right.metric("", label_visibility="collapsed", value=prefix + str(millify(val_2, precision=2)) + " " + unit, delta=delta, delta_color=delta_color)
        else:
            left.metric("", label_visibility="collapsed", value=prefix + str(millify(val_1, precision=2)) + " " + unit, )
            right.metric("", label_visibility="collapsed", value=prefix + str(millify(val_2, precision=2)) + " " + unit,)
    else:
        if delta_pos == -1:
            left.metric("", label_visibility="collapsed", value=prefix + str(val_1) + " " + unit,  delta=delta, delta_color=delta_color)
            right.metric("", label_visibility="collapsed", value=prefix + str(val_2) + " " + unit)
        elif delta_pos == 1:
            left.metric("", label_visibility="collapsed", value=prefix + str(val_1) + " " + unit)
            right.metric("", label_visibility="collapsed", value=prefix + str(val_2) + " " + unit, delta=delta, delta_color=delta_color)
        else:
            left.metric("", label_visibility="collapsed", value=prefix + str(val_1) + " " + unit)
            right.metric("", label_visibility="collapsed", value=prefix + str(val_2) + " " + unit)

# === Application ===

# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.005)
#     my_bar.progress(percent_complete + 1)
# time.sleep(0.5)
# my_bar.empty()


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

    with st.container(height=700):
        with st.spinner(): # adds spinning loading screen
            compare_spec(spec_1, spec_2, "boost_clock_ghz", "GHz", "Boost Clock Frequency")
            compare_spec(spec_1, spec_2, "base_clock", "GHz", "Base Clock Frequency")
            compare_spec(spec_1, spec_2, "vram_gb", "GB", "VRAM",small_val=True)
            compare_spec(spec_1, spec_2, "power_watts", "Watts", "Power Usage", small_val=True, delta_color="inverse")
            compare_spec(spec_1, spec_2, "msrp_usd", "USD", "MSRP Price", small_val=True, delta_color="inverse", prefix="$")
            compare_spec(spec_1, spec_2, "cuda_cores", "", "CUDA Cores", large_val=True)
            

    

    