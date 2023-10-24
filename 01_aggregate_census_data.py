import pandas as pd
import numpy as np
import os

import geopandas as gp
import argparse

def add_leading_zeros(string):
    result = '0' * (6 - len(string)) + string
    return result

def main(args):
    # Step 0: Pull data.
    acs_data = pd.read_csv(args.acs_data)
    decennial_data = pd.read_csv(args.decennial_data)
    block_group_shapefile = gp.read_file(args.block_group_shapefile)
    
    # Step 1: Using GEOID, join household income estimates from the 2021 ACS with population and housing unit totals from the 2020 Decennial Census.
    # Note: At the block group level, the GEOID is 12 digits: STATE + COUNTY + TRACT + BLOCK GROUP (2 + 3 + 6 + 1).
    for df in [acs_data, decennial_data]:
        df["county"] = df["county"].astype(str).apply(lambda x: "0" + x)
        df["tract"] = df["tract"].astype(str).apply(lambda x: add_leading_zeros(x))
        df["GEOID"] = df[["state", "county", "tract", "block group"]].apply(lambda x: "".join(x.astype(str)), axis = "columns")
    
    acs_data_trimmed = acs_data.copy()[["GEOID", "B19013_001E"]]
    decennial_data_trimmed = decennial_data.copy()[["GEOID", "H1_001N", "H8_001N"]]
    block_level_stats = pd.merge(acs_data_trimmed, decennial_data_trimmed, on = "GEOID", how = "left")
    block_level_stats.rename(columns = {"B19013_001E": "median_household_income", 
                                        "H1_001N": "total_housing_units",
                                        "H8_001N": "population"}, inplace = True)

    ###### Step 2: Recover geometries of the block groups from the 2021 TIGER/line shapefile, then join them with the block level statistics.
    block_group_shapefile_trimmed = block_group_shapefile[["GEOID", "geometry"]]
    df_temp = pd.merge(block_level_stats, block_group_shapefile_trimmed, on = "GEOID", how = "left")

    final_table = df_temp.loc[df_temp["population"] > 0, :]

    ###### Step 3: Export block group level census data.
    os.makedirs(args.output_dir, exist_ok = True)
    final_table.to_csv(f"{args.output_dir}/block_group_estimates.csv", index = False)
    
    print(f"Done. The clean block level census data has been exported to {args.output_dir}.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--acs_data", default = "raw_data/block_level_household_income.csv")
    parser.add_argument("--decennial_data", default = "raw_data/block_level_population_and_housing_units.csv")
    parser.add_argument("--block_group_shapefile", default = "raw_data/block_group_shapefiles/tl_2021_17_bg.shp")
    parser.add_argument("--output_dir", default = "processed_data")
    
    args = parser.parse_args()
    
    main(args)
    