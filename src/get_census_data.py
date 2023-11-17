import pandas as pd
import yaml
import os
import requests

def main(private_config_file, config_file, type):
   # Step 0: Pull api_key from private_config.
   api_key = private_config_file["api_key"]
   
   # Step 1: Create raw_data directory.
   os.makedirs("raw_data", exist_ok = True)

   #Step 2: Load parameters from config based on "type" of API request; assign api key to config["type"]["params"]["key"]; and initiate request.
   parameters = config_file[type]
   parameters["params"]["key"] = api_key
   
   response = requests.get(url = parameters["endpoint"], params = parameters["params"])
   data = response.json()
   
   # Step 3: Export output as .csv to raw_data/.
   response_as_df = pd.DataFrame(data)
   response_as_df.rename(columns = response_as_df.iloc[0, :], inplace = True)
   response_as_df.drop([0], axis = "rows", inplace = True)
   
   output_name = parameters["output_name"]
   response_as_df.to_csv(f"raw_data/{output_name}", index = False)
   
   print(f"Done. The {type} has been pulled.")
   
if __name__ == "__main__":
   with open("configuration/private_config.yaml", "r") as file:
      private_config = yaml.safe_load(file)   
   with open("configuration/config.yaml", "r") as file:
      config = yaml.safe_load(file)
      
   main(private_config, config, type = "acs_request")
   main(private_config, config, type = "decennial_census_request")