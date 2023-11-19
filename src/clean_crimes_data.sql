create table if not exists crimes_unprocessed (
    id numeric,
    case_number varchar(20),
    incident_date date,
    masked_address varchar(75),
    iucr_code varchar(5),
    incident_category varchar(100),
    incident_description varchar(100),
    location_description varchar(100),
    arrest boolean,
    domestic boolean,
    beat varchar(10),
    district varchar(10),
    ward varchar(10),
    community_area varchar(2),
    fbi_code varchar(3),
    x_coordinate char(7),
    y_coordinate varchar(7),
    year char(4),
    updated_on date,
    latitude numeric(5, 3),
    longitude numeric(5, 3),
    location varchar(50)
);

\copy crimes_unprocessed from 'big_data/Crimes_-_2001_to_Present.csv' DELIMITER ',' CSV HEADER;

create table if not exists crimes_trimmed as 
select c1.case_number, c1.incident_date, c2.neighborhood, c1.fbi_code, f.crime
from crimes_unprocessed c1
left join fbi_code_dict f on c1.fbi_code = f.code
left join community_area_dict c2 on (case when length(c1.community_area) <> 2 then concat('0', c1.community_area) else c1.community_area end) = c2.number
where c1.incident_date between '2018-01-01' and '2022-12-31' and fbi_code <> '27';

create table if not exists crimes_deduplicated as
select case_number,
       incident_date,
       extract(year from incident_date) as year,
       neighborhood,
       crime
from (select case_number, 
             incident_date, 
             crime,
             neighborhood,
<<<<<<< HEAD
             row_number() over (partition by case_number order by cast(regexp_replace(fbi_code, '[^0-9]', '', 'g') as int)) as rank 
      from crimes_trimmed) 
where rank = 1 order by incident_date;
=======
             row_number() over (partition by case_number order by CAST(regexp_replace(fbi_code, '[^0-9]', '', 'g') as int)) as rank 
      from crimes_trimmed) 
where rank = 1 order by incident_date;

create table if not exists crime_rates as 
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

\copy crime_rates to 'processed_data/neighborhood_crime_rates.csv' WITH DELIMITER ',' CSV HEADER;
>>>>>>> 08b5ec923e9a2e02de851acc9a0a2d75227c9f9a
