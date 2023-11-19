import pandas as pd
import numpy as np
import geopandas as gp

import plotly.express as px

crime_rates = pd.read_csv("processed_data/neighborhood_crime_rates_by_year.csv")
census_estimates = pd.read_csv("processed_data/neighborhood_census_estimates.csv")
data_temp = pd.merge(census_estimates, crime_rates, on = "neighborhood", how = "left")

neighborhood_shapefile = gp.read_file("raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
geometries = neighborhood_shapefile.copy()[["community", "geometry"]]

data = pd.merge(data_temp, geometries[["community", "geometry"]], left_on = "neighborhood", right_on = "community", how = "left")
data_as_gp = gp.GeoDataFrame(data, geometry = data["geometry"])

fig = px.choropleth_mapbox(
    data_as_gp,
    geojson = data_as_gp.geometry,
    locations = data_as_gp.index,
    color = 'robbery_rate_per_100k',
    animation_frame = "year",
    center = {"lat": data_as_gp.geometry.centroid.y.mean(), "lon": data_as_gp.geometry.centroid.x.mean()},
    mapbox_style=  "carto-positron",
    color_continuous_scale = "Viridis",
    range_color = (data_as_gp['robbery_rate_per_100k'].min(), data_as_gp['robbery_rate_per_100k'].max()))

fig.update_layout(title_text = "Crime Rate Over Time by Neighborhood", mapbox = dict(zoom=9))

fig.write_html("robbery_rates_over_time.html")  
