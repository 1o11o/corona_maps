import streamlit as st
import pandas as pd
from plotnine import ggplot, aes, geom_line, geom_point, scale_x_datetime, theme_light, ylab, scale_color_manual
from mizani.breaks import date_breaks
from datetime import datetime

# -------------------------------------------- Parameter ---------------------------------------------------------------
URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DOWNLOAD = True
PATH = './data/'

# ---------------------------------------------- functions -------------------------------------------------------------
@st.cache(suppress_st_warning=True)  #
def load_data(url):
    if DOWNLOAD:
        df = pd.read_csv(url, parse_dates=[3], infer_datetime_format=True)
        st.write('cache miss, loaded data')
        pd.DataFrame.to_csv(df, PATH + 'owid_all.csv')
    else:
        df = pd.read_csv("./data/owid_all.csv", parse_dates=[3], infer_datetime_format=False)
    #df = df.reset_index(drop=True)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
    return df

def get_col_plot(str):
    col_plot = str.lower()
    if totals:
        col_plot = "total_" + col_plot
    else:
        col_plot = "new_" + col_plot
        if smoothed:
            col_plot = col_plot + "_smoothed"
    if relative:
        if str == "Tests":
            col_plot = col_plot + "_per_thousand"
        else: col_plot = col_plot + "_per_million"
    return(col_plot)

# ------------------------------------------------ load data -----------------------------------------------------------
# Header
st.header("Corona - Checker")

#session_state = SessionState.get(index_column=None)
df = load_data(URL)
df = df.drop(df.columns[0], axis=1)


#get_state()
# ------------------------------------------------ User input --------------------------------------------------------------

# Choose variable
#display = ["Cases", "Tests", "Vaccinations", "Deaths", "Hospitalizations", "Intensive Care"]
var_options = ["Cases", "Tests", "Deaths"]
col_plot_decision = st.sidebar.selectbox('Choose variable:', var_options, index = 0) # todo: always defaults???

# Choose variable options
st.sidebar.write("Display Options")
totals = st.sidebar.checkbox("Total " + col_plot_decision, False, key="totals_cb")
relative = st.sidebar.checkbox("Relative to Population", False)
smoothed = st.sidebar.checkbox("Smoothed Lines (7-Day Average)", False)
if totals & smoothed:
    st.sidebar.write("Smoothed variables only available for new " + col_plot_decision)
else:
    st.sidebar.write(" ")

# get column
col_plot = get_col_plot(col_plot_decision)
st.write(col_plot)


# choose time
#time_span = st.sidebar.slider("Select Time span", min(df.date), max(df.date), (min(df.date), max(df.date)), 1)


#print(type(min(df.date)))
mint = min(df.date).to_pydatetime().date()
maxt = max(df.date).to_pydatetime().date()
time_span = st.sidebar.slider("Select Time span", mint, maxt, (mint, maxt), format="D.M.Y")

print(time_span)
print(type(time_span[0]))
print(pd.to_datetime(time_span[1]))
#time_span = st.sidebar.slider("Select Time span", min(df.date), max(df.date), (min(df.date), max(df.date)), format=format)
# Choose Countries
ctr_options = df.location.unique()

if "countries" not in st.session_state:
    st.session_state.countries = ["Austria"]

countries = st.sidebar.multiselect('Select countries', ctr_options, default = st.session_state.countries, key="countries")


dfx = df[['date', 'location', col_plot]]
dfx = dfx.dropna(subset=[col_plot, 'date'])
dfx = dfx.loc[dfx['location'].isin(countries) & (dfx['date'] >= pd.to_datetime(time_span[0])) & (dfx['date'] <= pd.to_datetime(time_span[1])),]

countries_missing = [value for value in countries if value not in dfx.location.unique()]
if len(countries_missing) > 0:
    st.write("No data available for the following countries. Please choose different countries or variables.\n" + ', '.join(countries_missing))


color_palette = ['#7E2E84', '#16CA58', '#FFBA08', '#5BC0EB', '#F25A02']

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

st.pyplot(ggplot.draw(fig))
