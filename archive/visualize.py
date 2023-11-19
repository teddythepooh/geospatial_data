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