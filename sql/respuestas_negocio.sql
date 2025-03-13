CREATE TABLE PRIMEIRA_PERGUNTA
WITH 
        cte1 AS( 
            SELECT
                seller_id,
            	created_at,
            	COUNT(item_id) AS total_sells
            FROM	
                TRANSACTIONS  
            WHERE
                created_at BETWEEN '2020-01-01' AND '2020-01-31'
            GROUP BY
                seller_id
            HAVING	
                total_sells>1500
            ),
            
        cte2 AS(
            SELECT
                client_id,
            	birth_date
            
            FROM
                CLIENT 
            WHERE	
              strftime('%m', birth_date) = strftime('%m', 'now') 
              AND strftime('%d', birth_date) = strftime('%d', 'now')
            )
        
        SELECT
			cte2.client_id,
            cte2.birth_date,
            cte1.total_sells

        FROM	
                cte2
        LEFT JOIN 
                cte1
        ON
                cte2.client_id = cte1.seller_id;

CREATE TABLE SEGUNDA_PERGUNTA

WITH 
	cte1 AS(
      SELECT	
      	category_id,
      	category_name
      FROM
      	CATEGORY
      WHERE
      	category_name = 'telemoveis'
      ),
      
    cte2 AS(
      SELECT 
      	seller_id,
      	category_id,
      	strftime('%Y-%m', created_at) AS year_month,
      	SUM(quantity) AS total_items_sold,
      	SUM(price * quantity) as sell_amount,
      	COUNT(order_id) AS total_sells
      FROM
      	TRANSACTIONS
      GROUP BY
      	seller_id,
      	year_month,
      	category_id
      ),
      
     cte3 AS(
       SELECT
       	cte1.category_id,
       	cte2.seller_id,
       	cte2.year_month,
       	cte2.total_items_sold,
       	cte2.sell_amount,
       	cte2.total_sells
       FROM
       	cte2
       INNER JOIN
       	cte1
       ON
       	cte1.category_id = cte2.category_id
     ),
     
     cte4 AS(
       SELECT
       	client_id,
       	name
       from 
       	CLIENT 
       )
 
 SELECT
 	cte3.category_id,
    cte4.name,
    cte3.seller_id,
    cte3.year_month,
    cte3.total_items_sold,
    cte3.sell_amount,
    cte3.total_sells
    
 FROM
 	cte3    
 LEFT JOIN
 	cte4
 ON
 	cte3.seller_id = cte4.client_id;

CREATE TABLE TERCEIRA_PERGUNTA

WITH cte1 AS (
    SELECT
        datetime_ref,
        item_id,
        seller_id,
        published_at,
        price,
        category_id,
        condition,
        shipping,
        ROW_NUMBER() OVER (PARTITION BY DATE(datetime_ref), item_id, seller_id ORDER BY datetime_ref DESC) AS rn
    FROM
        TRANSACTIONS )
SELECT
    datetime_ref,
    item_id,
    seller_id,
    published_at,
    price,
    category_id,
    condition,
    shipping
FROM
    cte1
WHERE
    rn = 1;