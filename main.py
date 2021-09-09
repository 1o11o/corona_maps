
import streamlit as st
#import requests
import pandas as pd
import numpy as np
#import matplotlib
# matplotlib.use("Qt5Agg")
#import matplotlib.pyplot as plt
from plotnine import ggplot, aes, geom_line, geom_point, scale_x_datetime, theme_light, ylab, scale_color_manual
from mizani.breaks import date_breaks
#from mizani.formatters import date_format
#from plotnine.data import economics
# import os.path
from os import path

# This is a sample Python script.

# Header
st.header("Corona - Checker")

# Subheader
st.subheader("")


# ----------------------------------------------------------------------------------------------------------------------
# PATH_VACC = "./data/vaccs.pkl"
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DOWNLOAD = True
PATH = './data/'

# ------------------------- functions -----------------------------------
@st.cache(suppress_st_warning=True)  #
def load_data(url):
    if DOWNLOAD:
        df = pd.read_csv(url, parse_dates=[5], infer_datetime_format=True)
        st.write('cache miss, loaded data')
        pd.DataFrame.to_csv(df, PATH + 'owid_all.csv')
    else:
        df = pd.read_csv("./data/owid_all.csv")
    df = df.reset_index(drop=True)
    return df

df = load_data(url)




#df['location'] = df['location'].astype('category')
#print(df[['date']].isna().sum())
# 0 nas
#print(df.dtypes)
#print(pd.to_datetime(dt1))
#print(pd.to_datetime(df[["date"]][1:10]))
#df = pd.to_datetime(df[["date"]],errors='coerce', format="%Y-%m-%d")
#df = df["date"].dt.strftime("%d/%m/%y")
#df.dtypes
#print(df.dtypes)
#exit()
# dfx.plot(x='date', y='total_vaccinations')
#dfx.head()
#dfx["total_vaccinations"] = dfx["total_vaccinations"].fillna(0)
#col_plot = "total_vaccinations_per_hundred"
display = df.columns
#options = list(range(len(display)))
#col_plot = st.selectbox('Choose variable:', options, format_func=lambda x: display[x])
col_plot: str = st.selectbox('Choose variable:', display, index = 5)

#print('col_plot', col_plot)

ctr_options = df.location.unique()
ctr_options = np.insert(ctr_options, 0, '<select>')
countries_temp = st.selectbox('Choose country:', ctr_options, index=14, key = 0)
if countries_temp != '<select>':
    countries = [countries_temp]

# loop doesn't work, creates non-unique keys, plus I don't no if it is unnecessarily ressourceintensive to have a constant loop.
#i = 1
#while i == len(countries):
#    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
#    countries_temp = st.selectbox(f"Choose country {i}:", ctr_options, index=0, key = (i+=1))
#    if countries_temp != '<select>':
#        countries = np.concatenate((countries, countries_temp), axis=None)
#        #i += 1
#    #print('countries 2', countries)

if len(countries) > 0:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 2:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 2', countries)

if len(countries) > 1:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 3:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 2', countries)

if len(countries) > 2:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 4:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 2', countries

if len(countries) > 3:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 5:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 2', countries)

print(countries)

#if(exists(col_plot)):
dfx = df.loc[df['location'].isin(countries), ]
dfx = dfx.dropna(subset=[col_plot])

divide_y_bool = False
if divide_y_bool:
    if max(dfx[col_plot]) > 10000:
        dfx[col_plot] = dfx[col_plot] / 100000
        divide_y_bool = True


print(dfx.head())

# print(dfx[[col_plot]])

#print(dfx.dtypes)
#print(dfx.dtypes)


# print(dfx[["location"]].dtype)


color_palette = ['#AE8CA3', '#143642', '#0F8B8D', '#EC9A29', '#A23E48']
st.write('plotdf', dfx)
st.write('dtypes', dfx.dtypes)

fig = (

        ggplot(dfx)  # What data to use

        + aes(x="date", y=col_plot, color="location")  # What variable to use

       # + geom_point()
        + geom_line(size = 2, na_rm=True)  # Geometric object to use for drawing
        + scale_x_datetime(breaks=date_breaks("100 days"))
        #+ scale_color_manual(values = color_palette)
        + theme_light()
)



if divide_y_bool:
    fig = fig + ylab(col_plot + ' in 100,000s')

st.pyplot(ggplot.draw(fig))