-- models/staging/stg_messages.sql

{{ config(materialized='table') }}

SELECT 
*
FROM {{ source('public', 'messages_images') }}
