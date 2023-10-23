
import pandas as pd

import numpy as np
import geopandas as gp
import yaml

import matplotlib.pyplot as plt
pd.options.display.float_format = '{:.2f}'.format

# The CRS of the US Census and Chicago's community area shapefiles are 4269 and 4326, respectively. To proportionally assign census stats to
# the community area boundaries, I will use the equal area projection (9822) to calculate areas.

with open("configuration/config.yaml", "r") as file:
    config = yaml.safe_load(file)

##### Step 0: Load data.
block_level_stats = pd.read_csv("processed_data/clean_block_level_census_data.csv")
block_level_stats_trimmed = block_level_stats.copy()[["GEOID", "geometry", "population", "total_housing_units"]]

community_areas = gp.read_file("raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
community_areas_trimmed = community_areas.copy()[["community", "geometry"]]



##### Step 1: Calculate how much each block group (by area) is within a specific neighorhood.
# https://stackoverflow.com/questions/56433138/converting-a-column-of-polygons-from-string-to-geopandas-geometry
block_level_stats_trimmed["geometry"] = gp.GeoSeries.from_wkt(block_level_stats_trimmed["geometry"])
block_level_stats_trimmed = gp.GeoDataFrame(block_level_stats_trimmed, geometry = block_level_stats_trimmed["geometry"], crs = "EPSG:4269")

block_level_stats_trimmed.to_crs(config["crs_codes"]["for_area_calculations"], inplace = True)
block_level_stats_trimmed["block_area"] = block_level_stats_trimmed.area.round(2)

community_areas_trimmed.to_crs(config["crs_codes"]["for_area_calculations"], inplace = True)    

result = gp.overlay(block_level_stats_trimmed, community_areas_trimmed, how = "union", keep_geom_type = False)
result.dropna(subset = ["GEOID", "community"], inplace = True)
result["area_of_intersection"] = result.area.round(2)
result["pct"] = (result["area_of_intersection"] / result["block_area"]).round(3)

# result["proportional_pop"] = (result["population"] * result["pct"]).round(0).astype(int)
# result["proportional_total_housing_units"] = (result["total_housing_units"] * result["pct"]).round(0).astype(int)



##### Step 2: Assign block-group level statistics proportionally by area to neighborhoods.
result["GEOID"] = result["GEOID"].astype(float).astype("Int64").astype(str)
relevant_cols = ["GEOID", "block_area", "community", "area_of_intersection", "pct"]

result[relevant_cols].sort_values("community", ascending = True).to_csv("processed_data/block_group_to_neighborhood_crosswalk.csv", index = False)
