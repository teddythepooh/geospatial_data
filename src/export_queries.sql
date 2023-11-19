\copy neighborhood_estimates to 'processed_data/neighborhood_census_estimates.csv' WITH DELIMITER ',' CSV HEADER
\copy five_year_average_crime_rates to 'processed_data/neighborhood_crime_rates.csv' WITH DELIMITER ',' CSV HEADER
\copy robbery_rates_per_year to 'processed_data/neighborhood_crime_rates_by_year.csv' WITH DELIMITER ',' CSV HEADER