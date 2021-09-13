import streamlit as st
import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point, scale_x_datetime, theme_light, ylab, scale_color_manual
from mizani.breaks import date_breaks

# Header
st.header("Corona - Checker")

# ----------------------------------------------------------------------------------------------------------------------
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DOWNLOAD = False
PATH = './data/'

default_relative = False
default_smoothed = False
default_relative_totals = True

if "totals" not in st.session_state:
    col_plot_decision = 'Cases'

# ---------------------------------------------- functions -------------------------------------------------------------
@st.cache(suppress_st_warning=True)  #
def load_data(url):
    if DOWNLOAD:
        df = pd.read_csv(url, parse_dates=[3], infer_datetime_format=True)
        st.write('cache miss, loaded data')
        pd.DataFrame.to_csv(df, PATH + 'owid_all.csv')
    else:
        df = pd.read_csv("./data/owid_all.csv")
    #df = df.reset_index(drop=True)
    return df

def get_col_plot(str):
    str = str.lower()
    if st.session_state.totals:
        str = "total_" + str
    else:
        str = "new_" + str
    if st.session_state.smoothed:
        str = str + "_smoothed"
    if st.session_state.relative:
        str = str + "_per_million"
    return(str)

# ------------------------------------------------ load data -----------------------------------------------------------

#session_state = SessionState.get(index_column=None)
df = load_data(url)
df = df.drop(df.columns[0], axis=1)

# ------------------------------------------------ sliders --------------------------------------------------------------

# Choose variable
display = ["Cases", "Tests", "Vaccinations", "Deaths", "Hospitalizations", "Intensive Care"]
col_plot_decision = st.sidebar.selectbox('Choose variable:', display, index = 0)

st.session_state.relative = st.sidebar.checkbox("Relative to Population", default_relative)
st.session_state.smoothed = st.sidebar.checkbox("Smoothed Lines (7-Day Average)", default_smoothed)
st.session_state.totals = st.sidebar.checkbox("Total " + col_plot_decision, default_relative_totals)

col_plot = get_col_plot(col_plot_decision)
st.write(col_plot)

# Choose Countries
try:
    country_selection
except NameError:
    country_selection = ["Austria"]
st.session_state.ctr_options = df.dropna(subset=[col_plot, 'date']).location.unique()
if 'country_selection' not in st.session_state:
    st.session_state.country_selection = ['Austria']
    country_selection = ['Austria']

st.session_state.country_selection = st.sidebar.multiselect('Select countries', st.session_state.ctr_options, default = st.session_state.country_selection)
st.write('country_selection update selection', st.session_state.country_selection)

countries = st.session_state.country_selection

dfx = df[['date', 'location', col_plot]]
dfx = dfx.dropna(subset=[col_plot, 'date'])
dfx = dfx.loc[dfx['location'].isin(countries), ]

divide_y_bool = False
if divide_y_bool:
    if max(dfx[col_plot]) > 10000:
        dfx[col_plot] = dfx[col_plot] / 100000
        divide_y_bool = True




color_palette = ['#7E2E84', '#16CA58', '#FFBA08', '#5BC0EB', '#F25A02']
#st.write('plotdf', dfx)
#st.write('dtypes', dfx.dtypes)


fig = (

        ggplot(dfx)  # What data to use

       # + aes(x="date", y=col_plot, color="location")  # What variable to use
        + aes(x='date', y=col_plot, group = 'location', color = 'location')  # What variable to use
        #+ geom_point()
        + geom_line(size=0.7)  # Geometric object to use for drawing
        + scale_x_datetime(breaks=date_breaks("100 days"))
        + scale_color_manual(values = color_palette, breaks = countries)
        + theme_light()
)



if divide_y_bool:
    fig = fig + ylab(col_plot + ' in 100,000s')

st.pyplot(ggplot.draw(fig))