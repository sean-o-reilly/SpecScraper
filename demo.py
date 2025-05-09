import streamlit as st
import matplotlib.pyplot as plt

gpu_data = {
    "GTX 1060": {"VRAM": 6, "Cores": 1280},
    "RTX 5070": {"VRAM": 12, "Cores": 7168}
}

gpu1, gpu2 = st.selectbox("Select GPU 1", gpu_data.keys()), st.selectbox("Select GPU 2", gpu_data.keys())

labels = list(gpu_data[gpu1].keys())
x = range(len(labels))

fig, ax = plt.subplots()
ax.bar(x, [gpu_data[gpu1][k] for k in labels], width=0.4, label=gpu1)
ax.bar([i+0.4 for i in x], [gpu_data[gpu2][k] for k in labels], width=0.4, label=gpu2)
ax.set_xticks([i+0.2 for i in x])
ax.set_xticklabels(labels)
ax.legend()
st.pyplot(fig)
