import yaml
import argparse

from src import get_census_data, aggregate_census_data, crosswalk_block_group_to_neighborhood

if __name__ == "__main__":
    with open("configuration/private_config.yaml", "r") as file:
        private_config = yaml.safe_load(file)   
    with open("configuration/config.yaml", "r") as file:
        config = yaml.safe_load(file)    
        
    get_census_data.main(private_config, config, type = "acs_request")
    get_census_data.main(private_config, config, type = "decennial_census_request")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--acs_data", default = "raw_data/block_level_household_income.csv")
    parser.add_argument("--decennial_data", default = "raw_data/block_level_population_and_housing_units.csv")
    parser.add_argument("--block_group_shapefile", default = "raw_data/block_group_shapefiles/tl_2021_17_bg.shp")
    parser.add_argument("--block_group_estimates", default = "processed_data/block_group_estimates.csv")
    parser.add_argument("--community_areas", default = "raw_data/community_area_shapefiles/geo_export_f8931b70-ff47-499c-8e70-012e4eebd628.shp")
    parser.add_argument("--output_dir", default = "processed_data")
    
    args, extra = parser.parse_known_args()

    aggregate_census_data.main(args)
    crosswalk_block_group_to_neighborhood.main(args, config)
