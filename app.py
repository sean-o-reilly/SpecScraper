import streamlit as st
import pandas as pd
from utils import process, millify, time, compare_all_specs
import plotly.express as px

def load_csv_with_error(path, **kwargs):
    try:
        return pd.read_csv(path, **kwargs)
    except Exception as e:
        st.error(f"Failed to load {path}: {e}")
        st.stop()

try:
    specs = load_csv_with_error("data/local/gpu_specs.csv").set_index("name")
    benchmarks = load_csv_with_error("data/local/gpu_fps.csv")
    games = load_csv_with_error("data/local/games.csv")
except Exception as e:
    st.error(f"Critical error loading data: {e}")
    st.stop()

# adding a relevance score to games df, weighted by how new the game is, and how popular it is
games['relevance_score'] = (
    (0.4 * games['popularity_score']) + 0.6 * (games['release_year'] - games['release_year'].min())
)

fps_df = pd.merge(benchmarks, games, on="game")
fps_df = fps_df.sort_values(by=['relevance_score'], ascending=[False])

names = specs.index.tolist()

# === Begin st UI === 

st.title("Hello, welcome to :blue[SpecScraper]! :wave:", anchor=None)

st.write("Enter two GPUs to compare below..")

left, right = st.columns(2)

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
    
    # === Comparing dashboard ===

    specs_tab, fps_tab = st.tabs(["Specs", "FPS"])

    with specs_tab:
        spec_1 = specs.loc[gpu_1]
        spec_2 = specs.loc[gpu_2]

        compare_all_specs(spec_1, spec_2)  
    with fps_tab:

        left, middle, right = st.columns(3)

        resolution = "1440p" # default for comparison

        if left.button("1080p", use_container_width=True):
            resolution = "1080p"
        if middle.button("1440p", use_container_width=True):
            resolution = "1440p"
        if right.button("4k", use_container_width=True):
            resolution = "4k"

        compare_fps_df = fps_df[
            ((fps_df['gpu_name'] == gpu_1) | (fps_df['gpu_name'] == gpu_2)) &
            (fps_df['resolution'] == resolution)
        ]

        # compare_fps_df
        fps_bar = px.bar(compare_fps_df, 
                x='game', 
                y='fps_avg', 
                color='gpu_name', 
                barmode='group', 
                text='fps_avg',
                width=10,
                title=f"{resolution}")
        fps_bar.update_traces(textposition='outside')
        fps_bar.update_layout(yaxis_title='Average FPS', xaxis_title='', legend_title=None, title_x=0.5)

        st.plotly_chart(fps_bar, use_container_width=True, on_select="rerun")
    
        st.caption("Benchmarked on max settings")