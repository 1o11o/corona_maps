from plotnine.data import economics
from plotnine import ggplot, aes, geom_line

print(economics.head())
fig = (

        ggplot(economics)  # What data to use

        + aes(x="date", y="pop")  # What variable to use

        + geom_line()  # Geometric object to use for drawing

)

#fig.draw()
print(fig)

import matplotlib.pyplot as plt


plt.plot([1,2,3])
#plt.show()



if len([countries]) > 0:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 2:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 2', countries)

print('countries 2', countries)
print('length countries at 2:', len([countries]))
if len(countries) > 1:
    ctr_options = ctr_options[~np.isin(ctr_options, [countries])]
    countries_temp = st.selectbox('Choose country 3:', ctr_options, index=0)
    if countries_temp != '<select>':
        countries = np.concatenate((countries, countries_temp), axis=None)
    #print('countries 3', countries)