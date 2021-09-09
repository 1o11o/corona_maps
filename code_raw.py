# import streamlit as st
import requests
import pandas as pd
import matplotlib
# matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from plotnine import ggplot, aes, geom_line, geom_point, scale_x_datetime
from mizani.breaks import date_breaks
from mizani.formatters import date_format
from plotnine.data import economics

# ----------------------------------------------------------------------------------------------------------------------
PATH_VACC = "./data/vaccs.pkl"
import os.path
from os import path

if path.exists(PATH_VACC):
    df = pd.read_pickle(PATH_VACC)
else:
    print('none')
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
    df = pd.read_csv(url, parse_dates=[2], infer_datetime_format=True)
    df.to_pickle(PATH_VACC)    #to save the dataframe, df to 123.pkl

    df.to_csv('./data/vaccs.csv')


#df['location'] = df['location'].astype('category')
#print(df[['date']].isna().sum())
# 0 nas
print(df.dtypes)


#print(pd.to_datetime(dt1))

#print(pd.to_datetime(df[["date"]][1:10]))


#df = pd.to_datetime(df[["date"]],errors='coerce', format="%Y-%m-%d")
#df = df["date"].dt.strftime("%d/%m/%y")

#df.dtypes
#print(df.dtypes)

#exit()





ctr = 'Austria', 'Greece'

dfx = df.loc[df['location'].isin(ctr),]
# dfx.plot(x='date', y='total_vaccinations')
dfx.head()

#dfx["total_vaccinations"] = dfx["total_vaccinations"].fillna(0)

col_plot = "total_vaccinations_per_hundred"

dfx = dfx.dropna(subset=[col_plot])


# print(dfx[[col_plot]])

#print(dfx.dtypes)
print(dfx.dtypes)


# print(dfx[["location"]].dtype)



fig = (

        ggplot(dfx)  # What data to use

        + aes(x="date", y=col_plot, color="location")  # What variable to use

       # + geom_point()
        + geom_line(size = 2, na_rm=True)  # Geometric object to use for drawing
        + scale_x_datetime(breaks=date_breaks("100 days"))
)

print(fig)