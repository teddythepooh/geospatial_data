# Geospatial Analysis

As a Data Analytics Associate at the Urban Crime Lab in Chicago, I have to deal with geospatial data in my work. This repo documents **my geospatial work using *public* data from the US Census Bureau API and open data portals.**

**I aim to project different statistics onto a map of Chicago at the neighborhood level: population, median household income, total housing units, Part I violent crime rates, and burglary rates. In the long-run, I hope to analytically determine food deserts** by geocoding grocery store addresses&mdash;Aldi, Walmart, and Jewel Osco&mdash;and visualizing areas that are farther than *i* kilometers for *i = {1, 2,. . .}.* The following datasets are available for download, along with the scripts that generate them (if applicable):

1. Chicago community area geometries (Source: Chicago Data Portal)
2. Block group level household median income estimates from the 2021 American Community Survey (Source: US Census Bureau API), plus block group geometries from the 2021 TIGER/line shapefiles
3. Block group level population and housing unit estimates from the 2020 Decennial Census (Source: US Census Bureau API)
4. A crosswalk of block groups to community area, whereby I calculated how much of each block group is contained within a neigborhood

If anyone would like to apply this repo in their work, note the following:
<div style="text-align: justify;">
  
- US Census aggregations are uniquely identified by GEOID. It is a 12-character alphanumeric sequence for block groups (STATE+COUNTY+TRACT+BLOCK GROUP|2+3+6+1=12). Leading zeroes need to be added where applicable.

- The US Census does not formally obtain statistics at the "neighorhood" level for cities. Since a block group's geometry can reside within more than one neighborhood, dataset #4 above allows me to proportionally assign statistics by area. Suppose a block group has a population of 1000 people and 50% of its total area is within Albany Park; then, I would assign 500 of 1000 to Albany Park.

- I leverage the Albers Equal Area projection (ESPG:9822) for area calculations, but I reproject the geometries to World Geodetic System 1984 for visualization (ESPG: 4326).
</div>
