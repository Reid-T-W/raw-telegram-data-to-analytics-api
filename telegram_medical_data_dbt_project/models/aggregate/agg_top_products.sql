select 
    product_name, 
    count(*) 
from {{ ref('fact_messages') }}
where product_name != '-'
group by product_name

