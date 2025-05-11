import streamlit as st
import pandas as pd
from utils import process, millify, time, compare_all_specs

df = pd.read_json("data/gpu_specs.json").set_index("name")

df["boost_clock_ghz"] = df["boost_clock_ghz"].round(2) # fix floating point errors
names = df.index.tolist()

# save this for later, could be cool for a chatbot
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

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

# using st's selectbox query, finds strings of each gpu with a dropdown menu and search

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

if gpu_1 is not None and gpu_2 is not None:  # only trigger once both parameters are entered
    
    # === Comparing dashboard happens here ===

    spec_1 = df.loc[gpu_1].to_dict() # convert each series to a python dict
    spec_2 = df.loc[gpu_2].to_dict()
    compare_all_specs(spec_1, spec_2)  

    # TODO: some sort of compare_fps function here