Let your working directory be at the project root `geospatial_analysis/`. Refer to the `configuration/` subdirectory for the `config.yaml` and `requirements.txt` files, the latter of which only applies to the .py scripts. Lastly, note that `main.py` and `create_database.sql` execute the scripts stored in `src/`.

Order of Operations (as of August 18, 2024):
1. `main.py`
2. `create_database.sql`

https://public.tableau.com/app/profile/ted.chua/viz/ChicagoRobberyRateswithDemographicEstimateOverlay/Dashboard1

![image](https://github.com/user-attachments/assets/0447cd8d-efae-40a6-9b5b-97696a524e5a)


#### Data Sources: US Census Bureau API, Chicago Data Portal
#### Software: Python, SQL (psql)

# <p align="center"> Geospatial Analysis <p align="center">
  
As a Research Analyst at the University of Chicago Crime Lab, I have to deal with geospatial data in my work. This repo documents *solely* my own geospatial work from *public* data sources. **I aim to project different statistics at the neighborhood level in Chicago: population, median household income, total housing units, Part I violent crime rates, burglary rates, and robbery rates. In the long-run, I am also interested in identifying food deserts** by visualizing areas that are farther than *i* kilometers for *i = {1, 2,. . .}* to a grocery store. The following datasets are available for download, along with the scripts that generate them (when applicable):

1. Chicago community area geometries
2. Point coordinates of 200+ grocery stores in Chicago
3. Block group estimates from the US Census Bureau API, plus their geometries (TIGER/Line)
4. A crosswalk of block group to community area, whereby I calculated how much of each block group is contained within a neigborhood

If anyone would like to apply this repo in their work,
<div style="text-align: justify;">

- You must register for an API key from the US Census. I stored mine in `private_config.yaml` in the same subdirectory as `config.yaml`. US Census aggregations are uniquely identified by GEOID. It is a 12-character alphanumeric sequence for block groups (STATE+COUNTY+TRACT+BLOCK GROUP|2+3+6+1=12).

- A block group's geometry can reside within more than one neighborhood. For my use-case, I proportionally assign block group estimates to neighborhoods on the basis of overlapping area. Suppose a block group has a population of 1000 and 50% of its total area is within Albany Park; then, I would assign 500 of 1000 to Albany Park. I project the geometries to Albers Equal Area (ESPG: 9822) for area calculations, but I reproject them to World Geodetic System 1984 (ESPG: 4326) for visualization.
</div>
