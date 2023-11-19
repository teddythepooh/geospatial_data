create table five_year_average_crime_rates as 
    with total_robberies_by_year as (
        select neighborhood, year, count(*) as total_robbery_counts
        from crimes_deduplicated
        where crime = 'Robbery'
        group by neighborhood, year
    ),
    average_robberies as (
        select neighborhood, avg(total_robbery_counts) as average_robbery_count
        from total_robberies_by_year
        group by neighborhood
    )
    select ar.neighborhood,
           round((ar.average_robbery_count / ne.total_population) * 100000) as robbery_rate_per_100k
    from average_robberies ar
    left join neighborhood_estimates ne on ar.neighborhood = ne.neighborhood
    order by robbery_rate_per_100k desc;

create table robbery_rates_per_year as 
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