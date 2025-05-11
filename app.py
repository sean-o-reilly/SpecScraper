import streamlit as st
import pandas as pd
from utils import process, millify, time, compare_spec

# need a way to get average fps across games

df = pd.read_json("data/gpu_specs.json").set_index("name")

df["boost_clock_ghz"] = df["boost_clock_ghz"].round(2) # fix floating point errors
names = df.index.tolist()

# save this for later, could be cool for a chatbot
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# takes in a dict with each gpu's specs, and unit of measurement, spec name for writing


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
             label_visibility="collapsed",
             index=None
             )

gpu_2 = right.selectbox(
            "empty2",
            names, 
             placeholder="Enter a GPU...", 
             label_visibility="collapsed",
             index=None
             )



if gpu_1 is not None and gpu_2 is not None:     #.strip() will ignore whitespace, this control flow will only trigger once both parameters are entered
    
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