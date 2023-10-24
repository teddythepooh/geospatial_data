import pandas as pd
import numpy as np
import os

import geopandas as gp
import argparse

import yaml

pd.options.display.float_format = '{:.2f}'.format

# The CRS of the US Census and Chicago's community area shapefiles are 4269 and 4326, respectively. To proportionally assign census stats to
# the community area boundaries, I will use the equal area projection (9822) to calculate areas.

def main(args, config_file):
    # Step 0: Pull data.    
    block_group_estimates = pd.read_csv(args.block_group_estimates)
    community_areas = gp.read_file(args.community_areas)
    
    block_group_estimates_trimmed = block_group_estimates.copy()[["GEOID", "geometry", "population", "total_housing_units"]]
    community_areas_trimmed = community_areas.copy()[["community", "geometry"]]
    
    crs_for_area_calculations = config_file["crs_codes"]["for_area_calculations"]

    # Step 1: Calculate how much each block group (by area) is within a specific neighorhood.
    # https://stackoverflow.com/questions/56433138/converting-a-column-of-polygons-from-string-to-geopandas-geometry
    block_group_estimates_trimmed["geometry"] = gp.GeoSeries.from_wkt(block_group_estimates_trimmed["geometry"])
    block_group_estimates_trimmed = gp.GeoDataFrame(block_group_estimates_trimmed, geometry = block_group_estimates_trimmed["geometry"], crs = "EPSG:4269")

    block_group_estimates_trimmed.to_crs(crs_for_area_calculations, inplace = True)
    community_areas_trimmed.to_crs(crs_for_area_calculations, inplace = True)    
    
    block_group_estimates_trimmed["block_area"] = block_group_estimates_trimmed.area.round(2)

    result = gp.overlay(block_group_estimates_trimmed, community_areas_trimmed, how = "union", keep_geom_type = False)
    result.dropna(subset = ["GEOID", "community"], inplace = True)
    result["area_of_intersection"] = result.area.round(2)
    result["pct"] = (result["area_of_intersection"] / result["block_area"]).round(3)

    ##### Step 2: Export.
    result["GEOID"] = result["GEOID"].astype(float).astype("Int64").astype(str)
    relevant_cols = ["GEOID", "block_area", "community", "area_of_intersection", "pct"]
    
    os.makedirs(args.output_dir, exist_ok = True)
    result[relevant_cols].to_csv(f"{args.output_dir}/block_group_to_neighborhood_crosswalk.csv", index = False)
    
    print(f"Done. The proportional crosswalk of block groups to community area has been exported {args.output_dir}.")
    
if __name__ == "__main__":
    with open("configuration/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_group_estimates", default =  "processed_data/block_group_estimates.csv")
    parser.add_argument("--community_areas", default = "raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
    parser.add_argument("--output_dir", default = "processed_data")
    
    args = parser.parse_args()
    
    main(args, config_file = config)
    
    
    
    

