-- Create the trigger function to handle operations

CREATE OR REPLACE FUNCTION sc_dm_cloudwalk.trg_audit_dm_clients()
RETURNS TRIGGER AS $$
BEGIN
    
    -- If it's an insertion operation
    IF TG_OP = 'INSERT' THEN
        
    -- Insert information into the log table
        INSERT INTO sc_dm_cloudwalk.log_dm_clients (user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason, denied_at, operation)
        VALUES (NEW.user_id, NEW.created_at, NEW.status, NEW.batch, NEW.credit_limit, NEW.interest_rate, NEW.denied_reason, NEW.denied_at, 'INSERT');

    -- If it's an update operation
    ELSIF TG_OP = 'UPDATE' THEN
    -- Insert information into the log table
        INSERT INTO sc_dm_cloudwalk.log_dm_clients (user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason, denied_at, operation)
        VALUES (NEW.user_id, NEW.created_at, NEW.status, NEW.batch, NEW.credit_limit, NEW.interest_rate, NEW.denied_reason, NEW.denied_at, 'UPDATE');

    -- If it's a deletion operation
    ELSIF TG_OP = 'DELETE' THEN
    -- Insert information into the log table
        INSERT INTO sc_dm_cloudwalk.log_dm_clients (user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason, denied_at, operation)
        VALUES (OLD.user_id, OLD.created_at, OLD.status, OLD.batch, OLD.credit_limit, OLD.interest_rate, OLD.denied_reason, OLD.denied_at, 'DELETE');
    END IF;

    -- Return the row
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating the trigger to invoke the function in dm_clients
CREATE TRIGGER trg_audit_dm_clients
AFTER INSERT OR UPDATE OR DELETE ON sc_dm_cloudwalk.dm_clients
FOR EACH ROW
EXECUTE FUNCTION sc_dm_cloudwalk.trg_audit_dm_clients();



