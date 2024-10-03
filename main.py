import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

cities_df = pd.read_csv('data/cities.csv')

cities_df['geometry'] = cities_df.apply(lambda row: Polygon([
    (row['southwest_lon'], row['southwest_lat']),
    (row['northeast_lon'], row['southwest_lat']),
    (row['northeast_lon'], row['northeast_lat']),
    (row['southwest_lon'], row['northeast_lat']),
    (row['southwest_lon'], row['southwest_lat'])
]), axis=1)

cities_gdf = gpd.GeoDataFrame(cities_df, geometry='geometry')

turkey_map = gpd.read_file('data/110m_cultural/ne_110m_admin_0_countries.shp')
turkey_map = turkey_map[turkey_map['ADMIN'] == 'Turkey']

fig, ax = plt.subplots(figsize=(16, 8))
turkey_map.boundary.plot(ax=ax, color='black')
cities_gdf.boundary.plot(ax=ax, color='red')

for x, y, label in zip(cities_df['southwest_lon'], cities_df['southwest_lat'], cities_df['pn']):
    ax.text(x, y, label, fontsize=7, ha='center', va='center', color='#000')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('City Borders in Turkey')

plt.get_current_fig_manager().set_window_title("City Borders in Turkey")
plt.show()
