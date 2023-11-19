import pandas as pd
import numpy as np
import geopandas as gp

import plotly.express as px

crime_rates = pd.read_csv("processed_data/neighborhood_crime_rates.csv")
census_estimates = pd.read_csv("processed_data/neighborhood_census_estimates.csv")
data_temp = pd.merge(census_estimates, crime_rates, on = "neighborhood", how = "left")

neighborhood_shapefile = gp.read_file("raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
geometries = neighborhood_shapefile.copy()[["community", "geometry"]]

data = pd.merge(data_temp, geometries[["community", "geometry"]], left_on = "neighborhood", right_on = "community", how = "left")
data_as_gp = gp.GeoDataFrame(data, geometry = data["geometry"])
data_as_gp.drop("community", axis = "columns", inplace = True)

bins = [data_as_gp["robbery_rate_per_100k"] < 100,
        (data_as_gp["robbery_rate_per_100k"] >= 100) & (data_as_gp["robbery_rate_per_100k"] < 300),
        (data_as_gp["robbery_rate_per_100k"] >= 300) & (data_as_gp["robbery_rate_per_100k"] < 500),
        (data_as_gp["robbery_rate_per_100k"] >= 500) & (data_as_gp["robbery_rate_per_100k"] < 700),
        (data_as_gp["robbery_rate_per_100k"] >= 700) & (data_as_gp["robbery_rate_per_100k"] < 1000),
        data_as_gp["robbery_rate_per_100k"] >= 1000]
labels = ["< 100", "100 - 300", "300 - 500", "500 - 700", "700 - 1000", ">= 1000"]

data_as_gp["bin"] = np.select(bins, labels)

color_dict = {
    "< 100": "lightblue",
    "100 - 300": "lightgreen",
    "300 - 500": "orange",
    "500 - 700": "lightcoral",
    "700 - 1000": "gold",
    ">= 1000": "red"
}

fig = px.choropleth(
    data_as_gp, 
    geojson = data_as_gp.geometry, 
    locations = data_as_gp.index, 
    color = data_as_gp["bin"],
    color_discrete_map = color_dict,
    hover_name = data_as_gp.neighborhood,
)

fig.update_geos(fitbounds = "locations", visible=False)
fig.show()

data_as_gp.robbery_rate_per_100k.describe()








crime_rates = pd.read_csv("processed_data/neighborhood_crime_rates_by_year.csv")
census_estimates = pd.read_csv("processed_data/neighborhood_census_estimates.csv")
data_temp = pd.merge(census_estimates, crime_rates, on = "neighborhood", how = "left")

neighborhood_shapefile = gp.read_file("raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
geometries = neighborhood_shapefile.copy()[["community", "geometry"]]

data = pd.merge(data_temp, geometries[["community", "geometry"]], left_on = "neighborhood", right_on = "community", how = "left")
data_as_gp = gp.GeoDataFrame(data, geometry = data["geometry"])
data_as_gp.drop(["community", "median_household_income", "total_population", "total_housing_units"], axis = "columns", inplace = True)

data_as_gp

fig1 = px.choropleth(data_as_gp,
                     geojson=data_as_gp.geometry,
                     locations=data_as_gp.index,
                     color=data_as_gp['robbery_rate_per_100k'],
                     animation_frame='year',
                     color_continuous_scale="Viridis",
                     title="Robbery Rates by Neighborhood (2018 - 2022)",
                     labels={'robbery_rate_per_100k': 'Robbery Rate per 100k'})

fig1.update_geos(fitbounds = "locations", visible=False)
fig1.write_html
