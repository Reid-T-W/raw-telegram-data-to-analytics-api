with distinct_channels as (
    select distinct
    channel_name
    from {{ ref('stg_messages') }}
)

select
    row_number() over (order by channel_name) as id,
    channel_name
from distinct_channels