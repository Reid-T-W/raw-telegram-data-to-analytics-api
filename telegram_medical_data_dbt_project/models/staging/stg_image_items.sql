select *
from {{ ref('raw_image_items') }}
where item is not null
  and trim(item) <> ''
  and lower(trim(item)) <> 'null'