import pandas as pd
import yaml
import os
import requests

from dotenv import load_dotenv

def main(config_file, type):
   # Step 0: Assign api_key from environment to an api_key object.
   load_dotenv()
   api_key = os.getenv("api_key")
   
   # Step 1: Create raw_data directory.
   try:
      os.makedirs("raw_data")
   except FileExistsError:
      pass
   
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
   
if __name__ == "__main__":
   with open("configuration/config.yaml", "r") as file:
      config = yaml.safe_load(file)
   
   main(config, type = "acs_request")
   main(config, type = "decennial_census_request")