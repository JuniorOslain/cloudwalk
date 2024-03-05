
CREATE TABLE sc_dm_cloudwalk.dm_clients
(
	user_id BIGSERIAL PRIMARY KEY,
	dt_create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	ds_status CHAR(8) NOT NULL,
	batch INT NOT NULL,
	credit_limit BIGINT,
	vlr_interest_rate INT,
	ds_denied_reason VARCHAR(50),
	dt_denied_at TIMESTAMP
	dt_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE sc_dm_cloudwalk.dm_loans
(
	user_id BIGINT NOT NULL,
	loan_id BIGINT PRIMARY KEY,
	due_at TIMESTAMP,
	created_at TIMESTAMP,
	paid_at TIMESTAMP,
	status CHAR(8),
	loan_amount NUMERIC(10,2),
	tax NUMERIC(10,2),
	due_amount NUMERIC(10,2),
	amount_paid NUMERIC(10,2),
	dt_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,	
	CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES sc_dm_cloudwalk.dm_clients(user_id)
)