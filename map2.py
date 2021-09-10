
import geopandas as gpd
import zipfile39 as zipf
import matplotlib.pyplot as plt
import re
import os
arr = os.listdir('data')
print(arr)

zipfile = "./data/10m_cultural.zip/10m_cultural/ne_10m_admin_0_boundary_lines_map_units.shp"
filename = "data/10m_cultural.zip"


# zip file handler
zip = zipf.ZipFile(filename)

# list available files in the container
zip_names = zip.namelist()
matching = [s for s in zip_names if "ne_10m_admin_0_boundary_lines_map_units" in s]

zip.extractall(members = matching, path = "data/")



shp_files = gpd.read_file("data/10m_cultural")
# extract a specific file from the zip container
#f = zip.open("file_inside_zip.txt")

# save the extraced file
#content = f.read()
#f = open('file_inside_zip.extracted.txt', 'wb')
#f.write(content)
#f.close()


#states = gpd.read_file("f'zip+s3://" + zipfile)

#import geoplot

#geoplot.polyplot(shp_files, figsize=(8, 4))


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

plot_map(shp_files)