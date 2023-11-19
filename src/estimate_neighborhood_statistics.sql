create table if not exists block_group_estimates (
    GEOID char(12) NOT NULL,
    median_household_income integer,
    total_housing_units integer,
    population integer,
    geometry varchar(50000) NOT NULL
);

create table if not exists block_group_to_neighborhood_crosswalk (
    GEOID char(12) NOT NULL,
    block_area numeric NOT NULL,
    community_area varchar(25) NOT NULL,
    area_of_intersection numeric NOT NULL,
    pct numeric(4, 3) NOT NULL
);

\copy block_group_to_neighborhood_crosswalk from 'processed_data/block_group_to_neighborhood_crosswalk.csv' DELIMITER ',' CSV HEADER;
\copy block_group_estimates from 'processed_data/block_group_estimates.csv' DELIMITER ',' CSV HEADER;

alter table block_group_estimates drop geometry;

create table summary as
select 
    c.geoid, c.community_area, b.median_household_income,
    b.population * c.pct as population_adjusted, 
    b.total_housing_units * c.pct as housing_units_adjusted
from block_group_estimates b
left join block_group_to_neighborhood_crosswalk c on c.geoid = b.geoid;

create temporary table temp as
select 
    community_area as neighborhood, 
    case when median_household_income < 0 
        then (select percentile_cont(0.5) within group (order by median_household_income) from summary where median_household_income > 0)
    else median_household_income end as adjusted_median_household_income,
    population_adjusted,
    housing_units_adjusted
from summary
where population_adjusted > 0 and housing_units_adjusted > 0;

create table neighborhood_estimates as
select 
    neighborhood, 
    round(avg(adjusted_median_household_income)) as median_household_income,
    round(sum(population_adjusted)) as total_population,
    round(sum(housing_units_adjusted)) as total_housing_units
from temp 
group by neighborhood
order by neighborhood asc;