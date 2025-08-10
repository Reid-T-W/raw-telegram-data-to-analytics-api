select
m.id,
m.channel_name,
m.message_id,
m.date_posted,
m.message_text,
case
    when mi.has_image is true then true
    else false
end as has_image
from {{ ref('raw_messages') }} as m
left join {{ ref('raw_messages_images')}} as mi
on m.message_id = mi.message_id

