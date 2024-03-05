CREATE TABLE sc_stage_cloudwalk.stg_clients
(
	user_id BIGINT,
	created_at TIMESTAMP,
	status CHAR(8) NOT NULL,
	batch INT NOT NULL,
	credit_limit NUMERIC(10,2),
	interest_rate INT,
	denied_reason VARCHAR(50),
	denied_at TIMESTAMP,
	dt_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sc_stage_cloudwalk.stg_loans
(
	user_id BIGINT NOT NULL,
	loan_id BIGINT,
	due_at TIMESTAMP,
	created_at TIMESTAMP,
	paid_at TIMESTAMP,
	status CHAR(8),
	loan_amount NUMERIC(10,2),
	tax NUMERIC(10,2),
	due_amount NUMERIC(10,2),
	amount_paid NUMERIC(10,2),
	dt_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP	
);