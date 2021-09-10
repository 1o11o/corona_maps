# https://datahub.io/core/geo-countries
import pandas as pd
import plotly.figure_factory as ff

# data
def load_data():
    df = pd.read_csv("./data/owid_all.csv")
    df = df.reset_index(drop=True)
    return df
df = load_data()

# --------------------------------------------

print(df[["date"]][1:10])

date_scope = "2021-03-05"

df = df[df["date"].isin([date_scope])]

values = df["total_cases"].tolist()

#print(df.head)






import plotly.graph_objects as go
import plotly.express as px


#country_data = px.data.gapminder()

print(df.head())

#df = px.data.gapminder().query("year == 2007")
#plot = px.scatter_geo(df, locations="iso_alpha")
#plot.show()


map_fix = px.scatter_geo(df,
                         locations = "iso_code",
                         projection = 'orthographic',
                         color = "location",
                         opacity= .8,
                         hover_name="location",
                         hover_data=["total_cases"])


#map_fix.show()
print(df.columns)


map_fix2 = px.choropleth(df,
                         locations = "iso_code",
                         projection = 'orthographic',
                         color = "total_vaccinations_per_hundred",
                         hover_name="location",
                         hover_data=["total_vaccinations_per_hundred"])


map_fix2.show()


fig = go.Figure(go.Scattergeo())
fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple"
)
fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()