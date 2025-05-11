import streamlit as st
from rapidfuzz import process # for querying df
from millify import millify # pretty number formatting
import time # sleeping



"""
compare_spec API to draw a comparison between two specs of a GPU

val_1 : corresponding value from gpu 1
val_2 : corresponding value from gpu 2
spec_name : index of spec to compare. "cuda_cores", "base_clock_ghz", etc.
unit : "GHz", "GB", "Watts", etc.
large_val : will use millify to round numbers. ex. 1,230 -> "1.23k"
small_val : will format small values like VRAM accordingly
delta_color : set to inverse when flipping weights^
prefix : string to add on, "$" for money, maybe curly "=" or "approx."

"""

def compare_spec(val_1, val_2, spec_name, unit, large_val=False, small_val=False, delta_color="normal", prefix=""):
    st.badge(spec_name)
    left, right = st.columns(2)

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


def compare_all_specs(s1, s2):


    with st.container(height=700):
        with st.spinner(): # adds spinning loading screen
            compare_spec(val_1=s1["boost_clock_ghz"], val_2=s2["boost_clock_ghz"], spec_name="Boost Clock Frequency", unit="GHz")
            compare_spec(val_1=s1["base_clock_ghz"], val_2=s2["base_clock_ghz"], spec_name="Base Clock Frequency", unit="GHz")
            compare_spec(val_1=s1["vram_gb"], val_2=s2["vram_gb"], spec_name="VRAM", unit="GB", small_val=True)
            compare_spec(val_1=s1["power_watts"], val_2=s2["power_watts"], spec_name="Power Usage", unit="Watts", small_val=True, delta_color="inverse")
            compare_spec(val_1=s1["msrp_usd"], val_2=s2["msrp_usd"], spec_name="MSRP Price", unit="USD", small_val=True, delta_color="inverse", prefix="$")
            compare_spec(val_1=s1["cuda_cores"], val_2=s2["cuda_cores"], spec_name="CUDA Cores", unit="", large_val=True)