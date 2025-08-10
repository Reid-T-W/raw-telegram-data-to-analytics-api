select *
from {{ ref('raw_llm_extracts_for_messages') }}
where channel_name != 'channel_name'
  and message_id != 'message_id'
  and intent != 'intent'
  and product_name != 'product_name'

