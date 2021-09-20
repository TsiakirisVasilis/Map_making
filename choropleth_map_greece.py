import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt  
from mpl_toolkits.axes_grid1 import make_axes_locatable


#We read the data with pandas and save them in an excel file
def get_data(url):
    ##read online 
    data = pd.read_html(url)
    for population in data:
        print(population)

    #save it to excel
    print('Copying to excel from html..')
    population.to_excel('C:\\Users\\Bill Tsiakiris\\Python\\gis\\html_data.xlsx')


pop_data = pd.read_excel('C:\\Users\\Bill Tsiakiris\\Python\\gis\\html_data.xlsx')
pop_data = pop_data[['Native', 'Status', 'PopulationCensus1991-03-17', 'PopulationCensus2001-03-18', 'PopulationCensus2011-03-16']]
pop_data.rename(columns={'PopulationCensus1991-03-17':'17-03-1991', 'PopulationCensus2001-03-18':'18-03-2001', 'PopulationCensus2011-03-16':'16-03-2011'}, inplace=True)
###Also we want only the rows for status municipality.So:
pop_data = pop_data.loc[pop_data['Status'] == 'Municipality']
###NOw read the shapefile by using the geopandas
greece = gpd.read_file('C:\\Users\\Bill Tsiakiris\\Python\\gis\\Νέος φάκελος\\GRC_adm3.shp')
greece = greece[['NL_NAME_3', 'geometry']]
greece = greece.rename(columns={'NL_NAME_3':'Municipality'})

#We have to delete the word Δήμος from the Native column
pop_data['Native'] = pop_data['Native'].str.replace(r'Δήμος', "")

##We have to make the reprojection
current_crs = greece.crs
greece.to_crs(epsg=2100, inplace=True)
###And now we need to calculate the area 
greece['Area'] = greece.area / 1000000

##But in order to make the check we needed to strip the spaces in order to match the same names and not read them as different strings
greece['Municipality'] = greece['Municipality'].str.strip()
pop_data['Native'] = pop_data['Native'].str.strip()

def check():
    #This is the check in order to make the join
    for index, row in greece['Municipality'].iteritems():
        if row in pop_data['Native'].tolist():
            pass
        else:
            print(row, 'is not in the list')

##Both datasets have to contain the same column name in order for the merge to be completed
pop_data = pop_data.rename(columns={'Native':'Municipality'})
#And now we make our merge
greece = greece.merge(pop_data, on = 'Municipality')

#we make a list of the three collumns that we want to iterrate on

greece['1991'] = greece['17-03-1991'] / greece['Area']
greece['2001'] = greece['18-03-2001'] / greece['Area']
greece['2011'] = greece['16-03-2011'] / greece['Area']
print(greece)

dates = greece[['1991', '2001', '2011']]

for date in dates:
    ax = greece.plot(column=date, cmap='OrRd', legend=True, scheme = 'user_defined', classification_kwds= {'bins': [5, 10, 20, 30, 50, 100]}, figsize=(10, 10))
    plt.title(f"Population Density in Greece for {date} (people per Sq. km)")
    ax.set_axis_off()
    ##MOve the legend out of the map
    ax.get_legend().set_bbox_to_anchor((0.1, 0.6))

    
    plt.show()







