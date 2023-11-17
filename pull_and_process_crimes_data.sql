create table if not exists crimes (
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

\copy crimes from 'big_data/Crimes_-_2001_to_Present.csv' DELIMITER ',' CSV HEADER;

create table if not exists crimes_trimmed as 
select case_number, 
       incident_date,
       fbi_code,
       case when length(community_area) <> 2 then concat('0', community_area) else community_area end as community_area_number
from crimes where incident_date between '2018-01-01' and '2022-12-31' and fbi_code <> '27';

alter table crimes_trimmed
add column code varchar(50),
add column community_area varchar(50); 

update crimes_trimmed
set 
    code = 
        case 
            when fbi_code like '01_' then 'homicides'
            when fbi_code = '02' then 'sexual assault'
            when fbi_code = '03' then 'robbery'
            when fbi_code like '04_' then 'aggravated assault and battery'
            when fbi_code = '05' then 'burglary'
            when fbi_code = '06' then 'larceny'
            when fbi_code = '07' then 'auto theft'
            when fbi_code like '08_' then 'simple assault and battery'
            when fbi_code = '09' then 'arson'
            when fbi_code = '10' then 'forgery and counterfitting'
            when fbi_code = '11' then 'fraud'
            when fbi_code = '12' then 'embezzlement'
            when fbi_code = '13' then 'stolen property'
            when fbi_code = '14' then 'stolen property'
            when fbi_code = '15' then 'weapons violation'
            when fbi_code = '16' then 'prostitution'
            when fbi_code = '17' then 'criminal sexual abuse'
            when fbi_code = '18' then 'drug abuse'
            when fbi_code = '19' then 'gambling'
            when fbi_code = '20' then 'offenses against family'
            when fbi_code = '22' then 'liquor law violation'
            when fbi_code = '24' then 'disorderly conduct'
            else 'non-index'
    end,
    community_area = 
        upper(case
            when community_area_number = '01' then 'Rogers Park'
            when community_area_number = '02' then 'West Ridge'
            when community_area_number = '03' then 'Uptown'
            when community_area_number = '04' then 'Lincoln Square'
            when community_area_number = '05' then 'North Center'
            when community_area_number = '06' then 'Lake View'
            when community_area_number = '07' then 'Lincoln Park'
            when community_area_number = '08' then 'Near North Side'
            when community_area_number = '09' then 'Edison Park'
            when community_area_number = '10' then 'Norwood Park'
            when community_area_number = '11' then 'Jefferson Park'
            when community_area_number = '12' then 'Forest Glen'
            when community_area_number = '13' then 'North Park'
            when community_area_number = '14' then 'Albany Park'
            when community_area_number = '15' then 'Portage Park'
            when community_area_number = '16' then 'Irving Park'
            when community_area_number = '17' then 'Dunning'
            when community_area_number = '18' then 'Montclare'
            when community_area_number = '19' then 'Belmont Cragin'
            when community_area_number = '20' then 'Hermosa'
            when community_area_number = '21' then 'Avondale'
            when community_area_number = '22' then 'Logan Square'
            when community_area_number = '23' then 'Humboldt Park'
            when community_area_number = '24' then 'West Town'
            when community_area_number = '25' then 'Austin'
            when community_area_number = '26' then 'West Garfield Park'
            when community_area_number = '27' then 'East Garfield Park'
            when community_area_number = '28' then 'Near West Side'
            when community_area_number = '29' then 'North Lawndale'
            when community_area_number = '30' then 'South Lawndale'
            when community_area_number = '31' then 'Lower West Side'
            when community_area_number = '32' then 'Loop'
            when community_area_number = '33' then 'Near South Side'
            when community_area_number = '34' then 'Armour Square'
            when community_area_number = '35' then 'Douglas'
            when community_area_number = '36' then 'Oakland'
            when community_area_number = '37' then 'Fuller Park'
            when community_area_number = '38' then 'Grand Boulevard'
            when community_area_number = '39' then 'Kenwood'
            when community_area_number = '40' then 'Washington Park'
            when community_area_number = '41' then 'Hyde Park'
            when community_area_number = '42' then 'Woodlawn'
            when community_area_number = '43' then 'South Shore'
            when community_area_number = '44' then 'Chatham'
            when community_area_number = '45' then 'Avalon Park'
            when community_area_number = '46' then 'South Chicago'
            when community_area_number = '47' then 'Burnside'
            when community_area_number = '48' then 'Calumet Heights'
            when community_area_number = '49' then 'Roseland'
            when community_area_number = '50' then 'Pullman'
            when community_area_number = '51' then 'South Deering'
            when community_area_number = '52' then 'East Side'
            when community_area_number = '53' then 'West Pullman'
            when community_area_number = '54' then 'Riverdale'
            when community_area_number = '55' then 'Hegewisch'
            when community_area_number = '56' then 'Garfield Ridge'
            when community_area_number = '57' then 'Archer Heights'
            when community_area_number = '58' then 'Brighton Park'
            when community_area_number = '59' then 'McKinley Park'
            when community_area_number = '60' then 'Bridgeport'
            when community_area_number = '61' then 'New City'
            when community_area_number = '62' then 'West Elsdon'
            when community_area_number = '63' then 'Gage Park'
            when community_area_number = '64' then 'Clearing'
            when community_area_number = '65' then 'West Lawn'
            when community_area_number = '66' then 'Chicago Lawn'
            when community_area_number = '67' then 'West Englewood'
            when community_area_number = '68' then 'Englewood'
            when community_area_number = '69' then 'Greater Grand Crossing'
            when community_area_number = '70' then 'Ashburn'
            when community_area_number = '71' then 'Auburn Gresham'
            when community_area_number = '72' then 'Beverly'
            when community_area_number = '73' then 'Washington Heights'
            when community_area_number = '74' then 'Mount Greenwood'
            when community_area_number = '75' then 'Morgan Park'
            when community_area_number = '76' then 'OHare'
            when community_area_number = '77' then 'Edgewater'
            else 'unknown'
    end);

create table if not exists crimes_deduplicated as
select case_number,
       incident_date,
       extract(year from incident_date) as year,
       code,
       community_area
from (select case_number, 
             incident_date, 
             code,
             community_area,
             row_number() over (partition by case_number order by CAST(regexp_replace(fbi_code, '[^0-9]', '', 'g') as int)) as rank 
      from crimes_trimmed) 
where rank = 1 order by incident_date;

create table if not exists robbery_rates as 
    with total_robberies_by_year as (
        select community_area, year, count(*) as total_robbery_counts
        from crimes_deduplicated
        where code = 'robbery'
        group by community_area, year
    ),
    average_robberies as (
        select community_area, avg(total_robbery_counts) as average_robbery_count
        from total_robberies_by_year
        group by community_area
    )
    select ar.community_area, /*round(ar.average_robbery_count) as average_robbery_count,*/
           /*ne.total_population, ne.total_housing_units, ne.median_household_income,*/
           round((ar.average_robbery_count / ne.total_population) * 100000) as robbery_rate_per_100k
    from average_robberies ar
    left join neighborhood_estimates ne on ar.community_area = ne.community_area
    order by robbery_rate_per_100k desc;

\copy robbery_rates to 'processed_data/robbery_rates_by_neighborhood.csv' WITH DELIMITER ',' CSV HEADER;
