import streamlit as st
from rapidfuzz import process # for querying df
from millify import millify # pretty number formatting
import time # sleeping

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