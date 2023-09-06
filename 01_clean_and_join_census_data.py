import pandas as pd
import numpy as np
import os
import re

import geopandas as gp

acs_data = pd.read_csv("raw_data\\block_level_household_income.csv")
decennial_data = pd.read_csv("raw_data\\block_level_population_and_housing_units.csv")

#Step 1: Join household income estimates from the 2021 ACS with population and housing unit totals from the 2020 Decennial Census.
def add_leading_zeros(string):
    result = '0' * (6 - len(string)) + string
    return result

for df in [acs_data, decennial_data]:
    df["county"] = df["county"].astype(str).apply(lambda x: "0" + x)
    df["tract"] = df["tract"].astype(str).apply(lambda x: add_leading_zeros(x))
    df["GEOID"] = df[["state", "county", "tract", "block group"]].apply(lambda x: "".join(x.astype(str)), axis = "columns")

acs_data_trimmed = acs_data.copy()[["GEOID", "B19013_001E"]]
decennial_data_trimmed = decennial_data.copy()[["H1_001N", "H8_001N", "GEOID"]]

joined_df_temp = pd.merge(acs_data_trimmed, decennial_data_trimmed, on = "GEOID", how = "left")

block_level_stats = joined_df_temp[joined_df_temp["B19013_001E"] > 0].reset_index(drop = True)
block_level_stats.rename(columns = {"B19013_001E": "median_household_income",
                                    "H1_001N": "total_housing_units",
                                    "H8_001N": "population"}, inplace = True)



#Step 2: Recover geometries of the block groups from the 2021 TIGER/line shapefile.
block_group_shapefile = gp.read_file("raw_data\\block_group_shapefiles\\tl_2021_17_bg.shp")
block_group_shapefile_trimmed = block_group_shapefile[["GEOID", "ALAND", "AWATER", "geometry"]]

final_df = pd.merge(block_level_stats, block_group_shapefile_trimmed, on = "GEOID", how = "left")



# Step 3: Export.
try:
    os.makedirs("processed_data")
except FileExistsError:
    pass

final_df.to_csv("processed_data/clean_block_level_census_data.csv")