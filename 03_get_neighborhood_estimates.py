import pandas as pd
import numpy as np

import geopandas as gp

import matplotlib.pyplot as plt
import plotly.express as px

block_group_to_neighborhood_crosswalk = pd.read_csv("processed_data/block_group_to_neighborhood_crosswalk.csv")
block_group_estimates = pd.read_csv("processed_data/clean_block_level_census_data.csv").drop("geometry", axis = "columns")
community_areas = gp.read_file("raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
community_areas_trimmed = community_areas.copy()[["community", "geometry"]]

impute = block_group_estimates.loc[block_group_estimates["median_household_income"] > 0, "median_household_income"].median()
block_group_estimates["median_household_income"] = block_group_estimates["median_household_income"].apply(lambda x: impute if x < 0 else x)

a = pd.merge(block_group_to_neighborhood_crosswalk, block_group_estimates, on = "GEOID", how = "left")
a["prop_total_housing_units"] = a["total_housing_units"] * a["pct"]
a["prop_pop"] = a["population"] * a["pct"]

a["weight"] = a["pct"] * a["prop_total_housing_units"]
a["weighted_median"] = a["weight"] * a["median_household_income"]

result = a.groupby("community").agg(population = ("prop_pop", "sum"), total_housing_units = ("prop_total_housing_units", "sum"), weights = ("weight", "sum"), weighted_median = ("weighted_median", "sum")).reset_index()
result["weighted_median_income"] = (result["weighted_median"] / result["weights"])

result_final = result[["community", "population", "total_housing_units", "weighted_median_income"]]
cols = ["population", "total_housing_units", "weighted_median_income"]
result_final.loc[:, cols] = result_final[cols].astype(int)

result2 = pd.merge(community_areas_trimmed, result_final, on = "community", how = "left")




community_areas_trimmed.crs




















fig = px.choropleth(result2, geojson = result2.geometry, locations = result2.index,  # Use the DataFrame index as locations
                    z=result2['weighted_median_income'],  # Replace with the actual column name for neighborhood names
                    hover_name = 'community', 
                    hoverinfo='location+z+name',# Replace with the actual column name for neighborhood names
                    title = 'Neighborhoods with Hover Names')
color_options = ["population", "total_housing_units", "weighted_median_income"]
buttons = [dict(label=col, method="restyle", args=[{"z": [result2[col]]}]) for col in color_options]
fig.update_layout(updatemenu=[dict(type="buttons", showactive=True, buttons=buttons, x=1.1, xanchor="left", y=1.05, yanchor="top")])
fig.update_geos(fitbounds = "locations", visible = False)
fig.show()           