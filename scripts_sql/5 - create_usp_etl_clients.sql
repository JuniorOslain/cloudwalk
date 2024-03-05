CREATE OR REPLACE PROCEDURE sc_dm_cloudwalk.usp_etl_clients()

LANGUAGE plpgsql

AS $$

BEGIN
/*Inserting data from staging table to dm clients table

*There is a rule that only new clients it will be included
**If there is the same client coming from the staging, this rule will be updated inside dm clients and the trigger 
will be enabled saving the former result inside sc_dm_cloudwalk.log_dm_clients.

*/
INSERT INTO sc_dm_cloudwalk.dm_clients 
	 (   user_id
	   , created_at
	   , status
	   , batch
	   , credit_limit
	   , interest_rate
	   , denied_reason
	   , denied_at
	 )
SELECT    user_id
		, created_at
		, status
		, batch
		, credit_limit
		, interest_rate
		, denied_reason
		, denied_at
FROM sc_stage_cloudwalk.stg_clients
WHERE user_id NOT IN (SELECT user_id FROM sc_dm_cloudwalk.dm_clients);


--If there is the same client coming, the fields bellow will be updated.
UPDATE sc_dm_cloudwalk.dm_clients AS a
SET 
    status = b.status,
    credit_limit = b.credit_limit,
    interest_rate = b.interest_rate,
    denied_reason = b.denied_reason,
    denied_at = b.denied_at
FROM sc_stage_cloudwalk.stg_clients AS b
WHERE 
    a.user_id = b.user_id;

END;

$$;