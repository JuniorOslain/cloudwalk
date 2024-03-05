--1.Identify the best month in terms of loan issuance. What was the quantity and amount lent in each month?
--Result = December is the best month

SELECT 
    TO_CHAR(created_at, 'YYYYMM') AS yearmonth,
    COUNT(*) AS loan_quantity,
    SUM(loan_amount) AS total_amount
FROM sc_dm_cloudwalk.dm_loans
GROUP BY yearmonth
ORDER BY total_amount DESC
LIMIT 1;


---------------------------------------------------------------------------------------------------------------------

--2.Which batch had the best overall adherence?
--Result = Batch 1
SELECT c.batch,
       COUNT(*) AS total_loans
FROM sc_dm_cloudwalk.dm_loans l
INNER JOIN sc_dm_cloudwalk.dm_clients c 
ON l.user_id = c.user_id
GROUP BY c.batch

---------------------------------------------------------------------------------------------------------------------
-- 3. Do different interest rates lead to different loan outcomes in terms of default rate?
-- Result = NO
SELECT 
    interest_rate,
	COUNT(DISTINCT c.user_id) 																			AS qtd_clients,
    COUNT(l.loan_id) 																					AS qtd_loans,
	COUNT(CASE WHEN l.status = 'default' THEN 1 ELSE NULL END)											AS default_loans,
    COUNT(CASE WHEN l.status = 'default' THEN 1 ELSE NULL END)/ CAST(COUNT(loan_id) AS NUMERIC(10,2)) 	AS "default_rate"
FROM sc_dm_cloudwalk.dm_loans l
INNER JOIN sc_dm_cloudwalk.dm_clients c 
ON l.user_id = c.user_id  
GROUP BY interest_rate;
/*

---------------------------------------------------------------------------------------------------------------------
4. Rank the best 10 and 10 worst clients. Explain your methodology for constructing this ranking.

Reasoning
Best Clients - 
1 - all customers who paid their loans 100%
2 - customers who have loyalty taking more than 1 loan
3 - customers who took out large loans and brought a difference in total owed vs. total paid, which gives the company more profit.
Worst Clients - 
1- all customers who broke their loans
2 - with the biggest difference due in our customer base considering total due vs total paid
*/
WITH best_clients AS (
    SELECT   	 c.user_id									AS user_id
                ,COUNT(l.loan_id)							AS qtd_loans
                ,SUM(l.loan_amount)							AS total_loan_amount
                ,ROUND(AVG(l.loan_amount),2)				AS avg_loan_amount
                ,MAX(l.loan_amount)							AS max_loan_amount
                ,MAX(c.credit_limit)						AS credit_limit
                ,SUM(amount_paid)							AS amount_paid
                ,SUM(due_amount)							AS due_amount
                ,SUM(amount_paid) - SUM(l.loan_amount)		AS total_difference_paid
                ,SUM(due_amount) - SUM(amount_paid)			AS total_remaining
                ,'BEST CLIENTS'								AS group_clients
    FROM sc_dm_cloudwalk.dm_loans l
    INNER JOIN sc_dm_cloudwalk.dm_clients c ON l.user_id = c.user_id 
    WHERE l.status = 'paid' 
    AND c.status = 'approved'
    GROUP BY c.user_id
    ORDER BY 9 DESC,3 DESC,2 DESC
    LIMIT 10
),
worst_clients AS (
    SELECT   c.user_id									AS user_id
            ,COUNT(l.loan_id)							AS qtd_loans
            ,SUM(l.loan_amount)							AS total_loan_amount
            ,ROUND(AVG(l.loan_amount),2)				AS avg_loan_amount
            ,MAX(l.loan_amount)							AS max_loan_amount
            ,MAX(c.credit_limit)						AS credit_limit
            ,SUM(amount_paid)							AS amount_paid
            ,SUM(due_amount)							AS due_amount
            ,SUM(amount_paid) - SUM(l.loan_amount)		AS total_difference_paid
            ,SUM(due_amount) - SUM(amount_paid)			AS total_remaining
            ,'WORST CLIENTS'							AS group_clients
    FROM sc_dm_cloudwalk.dm_loans l
    INNER JOIN sc_dm_cloudwalk.dm_clients c ON l.user_id = c.user_id 
    WHERE l.status = 'default'
    GROUP BY c.user_id
    ORDER BY 10 DESC,3 DESC,2 DESC
    LIMIT 10
)
SELECT * FROM best_clients
UNION ALL
SELECT * FROM worst_clients;
---------------------------------------------------------------------------------------------------------------------
--5. What is the default rate by month and batch?

SELECT TO_CHAR(l.created_at, 'YYYY-MM')																	   AS yearmonth
		,batch
		,COUNT(CASE WHEN l.status = 'default' THEN 1 ELSE NULL END)/ CAST(COUNT(loan_id) AS NUMERIC(10,2)) AS "%_default_loans"
FROM sc_dm_cloudwalk.dm_loans l
INNER JOIN sc_dm_cloudwalk.dm_clients c 
ON l.user_id = c.user_id 
GROUP BY TO_CHAR(l.created_at, 'YYYY-MM'),batch
ORDER BY 1
---------------------------------------------------------------------------------------------------------------------
/*6. Assess the profitability of this operation. Provide an analysis of the operation's timeline.
adherence: clients that got loans
season: loan issuing month
default rate: defaulted/issued loans
*/
-- Calculate the total revenue generated from loans
SELECT SUM(due_amount) AS total_revenue
FROM sc_dm_cloudwalk.dm_loans
WHERE status = 'paid';

-- Calculate the total loan amount issued
SELECT SUM(loan_amount) AS total_loan_amount
FROM sc_dm_cloudwalk.dm_loans;

-- Calculate the default rate
SELECT
    COUNT(CASE WHEN status = 'default' THEN 1 END) AS defaulted_loans,
    COUNT(*) AS total_issued_loans,
    (COUNT(CASE WHEN status = 'default' THEN 1 END)::float / COUNT(*)) AS default_rate
FROM sc_dm_cloudwalk.dm_loans;

-- Determine the distribution of loan issuance over time
SELECT
    TO_CHAR(created_at, 'YYYY-MM') AS issuance_month,
    COUNT(*) AS issued_loans
FROM sc_dm_cloudwalk.dm_loans
GROUP BY issuance_month
ORDER BY issuance_month;

-- Determine the adherence of clients who got loans
SELECT
    COUNT(DISTINCT user_id) AS adherent_clients
FROM sc_dm_cloudwalk.dm_loans;


