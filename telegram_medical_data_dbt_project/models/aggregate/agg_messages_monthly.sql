select
	dd.month as month,
	dd.year as year,
	count(*)
from {{ ref('fact_messages') }} fm
join {{ ref('dim_dates') }} dd on dd.id = fm.date_dim_id
group by (month, year)