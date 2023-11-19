create table if not exists a as 
with robberies_per_year as(
    select neighborhood, year, count(*) as total_robberies from crimes_deduplicated
    where crime = 'Robbery'
    group by neighborhood, year
)
select r.neighborhood, 
       r.year,
       round((r.total_robberies / n.total_population) * 100000) as robbery_rate_per_100k  
from robberies_per_year r
left join neighborhood_estimates n on r.neighborhood = n.neighborhood
order by robbery_rate_per_100k desc;

\copy a to 'processed_data/neighborhood_crime_rates_by_year.csv' WITH DELIMITER ',' CSV HEADER;
