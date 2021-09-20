import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify
import PIL
import io

plt.rcParams.update({'figure.max_open_warning': 0})
data = pd.read_csv('C:\\Users\\Bill Tsiakiris\\Python\\gis\\COVID-19-master\\who_covid_19_situation_reports\\who_covid_19_sit_rep_time_series\\\who_covid_19_sit_rep_time_series.csv')
#Now group the data by country
data = data.groupby('Country/Region').sum()
print(data.head(20))

#3create the geodataframe object with the global shapefile
world = gpd.read_file('C:\\Users\\Bill Tsiakiris\\Python\\gis\\COVID-19-master\\World_Map.shp')

def replacements():
    ###These are the replacements, based on the check we made earlier
    ##The first argument is the name in the shapefile and the second the name in the csv(the database)
    world.replace('Viet Nam', 'Vietnam', inplace = True)
    world.replace('Brunei Darussalam', 'Brunei', inplace = True)
    world.replace('Cape Verde', 'Cabo Verde', inplace = True)
    world.replace('Democratic Republic of Congo', 'Congo (Kinshasa)', inplace = True)
    world.replace('Czech Republic', 'Czechia', inplace = True)
    world.replace('Swaziland', 'Eswatini', inplace = True)
    world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
    world.replace("Korea, Deocratic People's Republic of", 'Republic of Korea', inplace = True)
    world.replace("Lao People's Democratic Republic", 'Laos', inplace = True)
    world.replace('Libyan Arab Jamahiriya', 'Libya', inplace = True)
    world.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace = True)
    world.replace('Syrian Arab Republic', 'Syria', inplace = True)
    world.replace('Taiwan', 'Taiwan*', inplace = True)
    world.replace('United States', 'United States of America', inplace = True)
    world.replace('Palestine', 'occupied Palestinian territory', inplace = True)
    world.replace('Russia', 'Russian Federation', inplace = True)
    world.replace("Cote d'Ivoire", 'Cote dIvoire', inplace = True)
    world.replace('United Kingdom', 'The United Kingdom', inplace = True)
replacements()

#Now with the replaced Country names we can merge the  data with the NAME column of the shapefile
new_data = world.join(data, on='NAME', how='right')

map_frames = []
dates = new_data.columns.to_list()

for date in dates[2:155]:
    #Make the plot
    ax = new_data.plot(column = date,
                    cmap='OrRd',
                    figsize = (14, 14),
                    legend = True,
                    scheme = 'user_defined',
                    classification_kwds= {'bins': [10, 20, 50, 100, 500, 1000, 5000, 10000]},
                    edgecolor = 'black',
                    linewidth = 0.4)
    #Set a title to the plot
    ax.set_title('Total confirmed Coronavirus Cases: ' + date, fontdict = {'fontsize' : 20}, pad = 12.5)

    #Als the legend should mov down and left
    ax.get_legend().set_bbox_to_anchor((0.18, 0.6))
    
    #and remove the axis
    ax.set_axis_off()
    
    img = ax.get_figure()
    
    f = io.BytesIO()
    img.tight_layout()
    img.savefig(f, format='png')
    f.seek(0)
    map_frames.append(PIL.Image.open(f))

##Make the gif
map_frames[0].save('Covid-19 Confirmed Cases.gif', format='GIF', append_images = map_frames[1:], save_all= True, duration=300, loop=0) 

f.close()

