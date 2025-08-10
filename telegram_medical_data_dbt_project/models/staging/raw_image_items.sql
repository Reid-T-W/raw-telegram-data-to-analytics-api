{{ config(materialized='table') }}

SELECT 
*
FROM {{ source('public', 'image_items') }}
