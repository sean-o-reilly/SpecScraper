import streamlit as st
from rapidfuzz import process 
from millify import millify 
import time

def compare_spec(val_1, val_2, 
                 spec_name, unit, 
                 large_val=False, 
                 small_val=False, 
                 delta_color="normal", 
                 prefix="", 
                 compare_processors=0):

    with st.container(height=150):
        st.badge(spec_name)
        left, right = st.columns(2)

        # assuming two valid specs to compare

        # "+4 Gb" instead of "50% more GB"
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

            if compare_processors == -1: #Cuda cores left, stream processors right
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_1, precision=2) ) + " CUDA Cores")
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_2, precision=2) ) + " SPs")
            elif compare_processors == 1: #Cuda cores right, stream processors left
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_1, precision=2) ) + " SPs")
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_2, precision=2) ) + " CUDA Cores")
            elif delta_pos == -1:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_1, precision=2) ) + " " + unit,  delta=delta, delta_color=delta_color)
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str( millify(val_2, precision=2) ) + " " + unit)
            elif delta_pos == 1:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str(millify(val_1, precision=2)) + " " + unit)
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str(millify(val_2, precision=2)) + " " + unit, delta=delta, delta_color=delta_color)
            else:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str(millify(val_1, precision=2)) + " " + unit, )
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str(millify(val_2, precision=2)) + " " + unit,)
        else:
            if delta_pos == -1:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_1) + " " + unit,  delta=delta, delta_color=delta_color)
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_2) + " " + unit)
            elif delta_pos == 1:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_1) + " " + unit)
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_2) + " " + unit, delta=delta, delta_color=delta_color)
            else:
                left.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_1) + " " + unit)
                right.metric(spec_name, label_visibility="collapsed", value=prefix + str(val_2) + " " + unit)

# s1 and s2 are pandas series of gpu specs
def compare_all_specs(s1, s2):

    with st.spinner(): # adds spinning loading screen
        compare_spec(val_1=s1["boost_clock_ghz"], val_2=s2["boost_clock_ghz"], spec_name="Boost Clock Frequency", unit="GHz")
        compare_spec(val_1=s1["base_clock_ghz"], val_2=s2["base_clock_ghz"], spec_name="Base Clock Frequency", unit="GHz")
        compare_spec(val_1=s1["vram_gb"], val_2=s2["vram_gb"], spec_name="VRAM", unit="GB", small_val=True)
        compare_spec(val_1=s1["power_watts"], val_2=s2["power_watts"], spec_name="Power Usage", unit="Watts", small_val=True, delta_color="inverse")
        compare_spec(val_1=s1["msrp_usd"], val_2=s2["msrp_usd"], spec_name="MSRP Price", unit="USD", small_val=True, delta_color="inverse", prefix="$")
        
        # potentially a better way to compare processors, or simply dont compare cuda cores/stream processors at all
        if s1.name[0] == 'N' and s2.name[0] == 'N':
            compare_spec(val_1=s1["processors"], val_2=s2["processors"], spec_name="Processors", unit="CUDA Cores", large_val=True)
        elif "AMD" in s1.name  and "AMD" in s2.name:
            compare_spec(val_1=s1["processors"], val_2=s2["processors"], spec_name="Processors", unit="SPs", large_val=True)
        elif "NVIDIA" in s1.name  and "AMD" in s2.name: 
            compare_spec(val_1=s1["processors"], val_2=s2["processors"], spec_name="Processors", unit="", large_val=True, compare_processors=-1)
        elif "AMD" in s1.name  and "NVIDIA" in s2.name:
            compare_spec(val_1=s1["processors"], val_2=s2["processors"], spec_name="Processors", unit="", large_val=True, compare_processors=1)