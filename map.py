
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
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
from os import path

# This is a sample Python script.


# ----------------------------------------------------------------------------------------------------------------------
# PATH_VACC = "./data/vaccs.pkl"
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
DOWNLOAD = False
PATH = './data/'



# https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units
# ------------------------- functions -----------------------------------
#@st.cache(suppress_st_warning=True)  #
def load_data(url):
    if DOWNLOAD:
        df = pd.read_csv(url, parse_dates=[3], infer_datetime_format=True)
        #st.write('cache miss, loaded data')
        pd.DataFrame.to_csv(df, PATH + 'CNTR_BN_60M_2020_3035_INLAND/CNTR_BN_60M_2020_3035_INLAND.shp')
    else:
        df = pd.read_csv("./data/owid_all.csv")
    #df = df.reset_index(drop=True)
    return df

df = load_data(url)
df = df.drop(df.columns[0], axis=1)

shp_path = PATH + 'CNTR_BN_60M_2020_3857/CNTR_BN_60M_2020_3857.shp'

sf = shp.Reader(shp_path)

sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))

def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]#fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]#converting shapefile data into pandas dataframe
    df = pd.DataFrame(columns=fields, data=records)#assigning the coordinates
    df = df.assign(coords=shps)
    return df

df = read_shapefile(sf)
df.shape

# plot
def plot_shape(id, s=None):
    plt.figure()
    #plotting the graphical axes where map ploting will be done
    ax = plt.axes()
    ax.set_aspect('equal')#storing the id number to be worked upon
    shape_ex = sf.shape(id)#NP.ZERO initializes an array of rows and column with 0 in place of each elements
    #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    x_lon = np.zeros((len(shape_ex.points),1))#an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]#plotting using the derived coordinated stored in array created by numpy
    plt.plot(x_lon,y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)# use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0


def plot_map(sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    plt.figure(figsize=figsize)
    id = 0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')

        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id + 1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)  # calling the function and passing required parameters to plot the full mapplot_map(sf)
    plt.show()

if False:
    DIST_NAME = 'JAIPUR'
    #to get the id of the city map to be plotted
    com_id = df[df.DIST_NAME == DIST_NAME].index.get_values()[0]
    plot_shape(com_id, DIST_NAME)
    sf.shape(com_id)

plot_map(sf)

df = read_shapefile(sf)
print(df.shape)