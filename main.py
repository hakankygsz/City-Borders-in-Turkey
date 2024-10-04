import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def create_polygon(row):
    if row['southwest_lat'] < row['northeast_lat'] and row['southwest_lon'] < row['northeast_lon']:
        return Polygon([
            (row['southwest_lon'], row['southwest_lat']),
            (row['northeast_lon'], row['southwest_lat']),
            (row['northeast_lon'], row['northeast_lat']),
            (row['southwest_lon'], row['northeast_lat']),
            (row['southwest_lon'], row['southwest_lat'])
        ])
    else:
        print(f"Invalid coordinates for {row['pn']}")
        return None

cities_df = pd.read_csv('data/cities.csv')

cities_df['geometry'] = cities_df.apply(create_polygon, axis=1)

cities_gdf = gpd.GeoDataFrame(cities_df[~cities_df['geometry'].isnull()], geometry='geometry')

turkey_map = gpd.read_file('data/110m_cultural/ne_110m_admin_0_countries.shp')
turkey_map = turkey_map[turkey_map['ADMIN'] == 'Turkey']

fig, ax = plt.subplots(figsize=(16, 8))
turkey_map.boundary.plot(ax=ax, color='black', linewidth=1)
cities_gdf.boundary.plot(ax=ax, color='red', linewidth=1.5)

cities_gdf['centroid'] = cities_gdf.centroid
for x, y, label in zip(cities_gdf['centroid'].x, cities_gdf['centroid'].y, cities_df['pn']):
    ax.text(x, y, label, fontsize=8, ha='center', va='center', color='blue',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3'))

plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.title('City Borders in Turkey', fontsize=16)

plt.get_current_fig_manager().set_window_title("City Borders in Turkey")

plt.tight_layout()
plt.show()
