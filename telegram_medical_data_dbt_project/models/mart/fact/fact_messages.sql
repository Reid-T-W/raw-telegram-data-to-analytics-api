select
    m.id,
    c.id as channel_dim_id,
    m.message_id,
    m.message_text,
    d.id as date_dim_id,
    llm.message_id as llm_message_id,
    llm.intent,
    llm.product_name
from {{ ref('stg_messages') }} as m
left join {{ ref('dim_channels')}} as c
on m.channel_name = c.channel_name
left join {{ ref('dim_dates')}} as d
  on extract(day from m.date_posted::date) = d.day
  and extract(month from m.date_posted::date) = d.month
  and extract(year from m.date_posted::date) = d.year
-- Do not include messages that do not have their intents identified
-- in this case their are 7 (the inner join removes this records)
inner join {{ ref('stg_llm_extracts_for_messages')}} as llm
  on m.message_id = llm.message_id
