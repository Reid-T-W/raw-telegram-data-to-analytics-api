select
	dd.day as day,
	dd.month as month,
	dd.year as year,
	count(*)
from {{ ref('fact_messages') }} fm
join {{ ref('dim_dates') }} dd on dd.id = fm.date_dim_id
group by (day, month, year)