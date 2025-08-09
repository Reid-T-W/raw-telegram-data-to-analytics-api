with distinct_dates as (
    select distinct
    date(date_posted) as date_column
    from {{ ref('stg_messages') }}
)

select
    row_number() over (order by date_column) as id,
    extract (day from date_column) as day,
    extract (month from date_column) as month,
    extract (year from date_column) as year
from distinct_dates