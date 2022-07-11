with actors as (
    select * from {{ ref('stg_swapi_data') }}
),
heaviest_actor_by_gender as (
select     
     name
    ,height
    ,mass
    ,hair_color
    ,skin_color
    ,eye_color
    ,birth_year
    ,age
    ,gender
    ,homeworld
    ,films
    ,species
    ,vehicles
    ,starships
    ,created
    ,edited
    ,url
    ,insert_date
    ,rank() over(partition by gender order by  mass desc) as rnk
FROM  actors
WHERE  mass is not null
and gender is not null
),
final as (
    select 
        name
        ,height
        ,age
        ,species
        ,homeworld
        ,gender
        ,mass
    from heaviest_actor_by_gender
    where rnk = 1
)
select * from final
