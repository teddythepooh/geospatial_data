# Geospatial Analysis
## Sources: US Census Bureau API, Chicago Data Portal

As a Data Analytics Associate at the Urban Crime Lab in Chicago, I have to deal with geospatial data in my work. This repo documents *solely* my own geospatial work from *public* data sources. **I aim to project different statistics onto a map of Chicago at the neighborhood level: population, median household income, total housing units, Part I violent crime rates, and burglary rates. In the long-run, I hope to identify food deserts** by visualizing areas that are farther than *i* kilometers for *i = {1, 2,. . .}* to a grocery store. The following datasets are available for download, along with the scripts that generate them (when applicable):

1. Chicago community area geometries
2. Point coordinates of 200+ grocery stores in Chicago
3. Block group estimates from the US Census Bureau API, plus their geometries (TIGER/Line)
4. A crosswalk of block group to community area, whereby I calculated how much of each block group is contained within a neigborhood

#### If anyone would like to apply this repo in their work, note the following:
<div style="text-align: justify;">
  
- You must register for an API key from the US Census. I deliberately stored mine in a `private_config.yaml`, hence the key value in `config.yaml` is an empty string. In lines 8 and 15 of `src/get_census_data.py,` I assign the api key from `private_config.yaml` back to the dictionary before initiating my API request.
- US Census aggregations are uniquely identified by GEOID. It is a 12-character alphanumeric sequence for block groups (STATE+COUNTY+TRACT+BLOCK GROUP|2+3+6+1=12). Leading zeroes need to be added where applicable.

- The US Census does not formally obtain statistics at the "neighborhood" level for cities. Since a block group's geometry can reside within more than one neighborhood, dataset #4 above allows me to proportionally assign statistics by area. Suppose a block group has a population of 1000 people and 50% of its total area is within Albany Park; then, I would assign 500 of 1000 to Albany Park.

- I leverage the Albers Equal Area projection (ESPG: 9822) for area calculations, but I reproject the geometries to World Geodetic System 1984 (ESPG: 4326) for visualization. By default, the CRS of the US Census and Chicago community area geometries are 4269 and 4326, respectively.

- All scripts are intended to be run from the project root (`geospatial_analysis/`), including the `.sql` script and `.py` scripts in `geospatial_analysis/src/`.
</div>
