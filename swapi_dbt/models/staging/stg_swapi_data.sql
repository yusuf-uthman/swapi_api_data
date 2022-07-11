with 
source as (
SELECT 
    id
    ,name
    ,case when height = 'unknown' then NULL else CAST(height AS INT) end as height
    ,case when mass = 'unknown' then NULL else CAST(mass as DECIMAL) end as mass
    ,hair_color
    ,skin_color
    ,eye_color
    ,birth_year
    ,case when age = 'unknown' then NULL else CAST(age as INT) end as age    
    ,case when gender in ('n/a','none') then NULL else gender end as gender
    ,homeworld
    ,films
    ,species
    ,vehicles
    ,starships
    ,created
    ,edited
    ,url
    ,insert_date
FROM {{source('staging','swapi_data')}}
)
select * from source
