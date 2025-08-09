-- models/staging/stg_messages.sql

{{ config(materialized='table') }}

SELECT 
*
FROM {{ source('public', 'messages') }}

-- with source_data as (

--     select * from {{ source('public', 'messages') }}

-- )

-- select * from source_data








-- renamed as (

--     select
--         id as id_renamed,
--         message_id,
--         date_posted,
--         message_text
--     from source

-- )

-- select * from renamed


-- /*
--     Welcome to your first dbt model!
--     Did you know that you can also configure models directly within SQL files?
--     This will override configurations stated in dbt_project.yml

--     Try changing "table" to "view" below
-- */

-- {{ config(materialized='table') }}

-- with source_data as (

--     select 1 as id
--     union all
--     select null as id

-- )

-- select *
-- from source_data

-- /*
--     Uncomment the line below to remove records with null `id` values
-- */

-- -- where id is not null
