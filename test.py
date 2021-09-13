
import streamlit as st

import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point, scale_x_datetime, theme_light, ylab, scale_color_manual
from mizani.breaks import date_breaks

# Header
st.header("Corona - test")

a_selection = st.selectbox('choose a', ['a1', 'a2'], index = 0)

if a_selection == 'a1':




b_selection = st.selectbox('choose a', ['a1', 'a2'], index = 0)


