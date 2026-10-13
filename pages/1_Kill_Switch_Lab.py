"""Streamlit multipage entry for the Kill Switch Lab (see sovereign_game/lab.py)."""

import streamlit as st

from sovereign_game.components import base_styles
from sovereign_game.lab import render_lab

st.set_page_config(page_title="Kill Switch Lab", page_icon="🧪", layout="wide")
st.markdown(base_styles(), unsafe_allow_html=True)
render_lab()
