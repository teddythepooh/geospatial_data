import pandas as pd
import numpy as np
import os

import geopandas as gp

import argparse
import plotly.express as px

def main(args):
    # Step 0: Pull data.
    block_group_to_neighborhood_crosswalk = pd.read_csv(args.crosswalk)
    
    block_group_estimates = pd.read_csv(args.block_group_estimates).drop("geometry", axis = "columns")
    
    community_areas = gp.read_file(args.community_areas)
    community_areas_trimmed = community_areas.copy()[["community", "geometry"]]
    
    # Step 1: For cases of block groups where the median income is unknown (i.e., negative numbers), impute with the median city-wide household income.
    impute = block_group_estimates.loc[block_group_estimates["median_household_income"] > 0, "median_household_income"].median()
    block_group_estimates["median_household_income"] = block_group_estimates["median_household_income"].apply(lambda x: impute if x < 0 else x)
    
    # Step 2: Assign population and total housing units of each block group proportionally to the community areas.
    result_temp = pd.merge(block_group_to_neighborhood_crosswalk, block_group_estimates, on = "GEOID", how = "left")
    result_temp["prop_total_housing_units"] = result_temp["total_housing_units"] * result_temp["pct"]
    result_temp["prop_pop"] = result_temp["population"] * result_temp["pct"]
    
    # Step 3: Calculate median household income in each community area as the weighted average of the block groups (scaled by total housing units).
    result_temp["weight"] = result_temp["pct"] * result_temp["prop_total_housing_units"]
    result_temp["weighted_income"] = result_temp["weight"] * result_temp["median_household_income"]
    
    result = result_temp.groupby("community").agg(population = ("prop_pop", "sum"), 
                                                  total_housing_units = ("prop_total_housing_units", "sum"), 
                                                  weights = ("weight", "sum"), 
                                                  weighted_income = ("weighted_income", "sum")).reset_index()
    
    result["median_household_income"] = result["weighted_income"] / result["weights"]
    
    relevant_cols = ["community", "population", "total_housing_units", "median_household_income"]
    result = result[relevant_cols]
    result[relevant_cols[1:]] = result[relevant_cols[1:]].round(0).astype(int)
    
    # Step 4: Recover community area geometries, then export.
    neighborhood_level_estimates = pd.merge(result, community_areas_trimmed, on = "community", how = "left")
    
    os.makedirs(args.output_dir, exist_ok = True)
    neighborhood_level_estimates.to_csv(f"{args.output_dir}/neighborhood_estimates.csv", index = False)
    
    print(f"Done. The neighborhood estimates have been exported to {args.output_dir}.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--crosswalk", default = "processed_data/block_group_to_neighborhood_crosswalk.csv")
    parser.add_argument("--block_group_estimates", default = "processed_data/block_group_estimates.csv")
    parser.add_argument("--community_areas", default = "raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
    parser.add_argument("--output_dir", default = "processed_data")
    
    args = parser.parse_args()
    
    main(args)