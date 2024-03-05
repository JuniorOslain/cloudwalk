"""

# 1 Using the function input_stage_data from 1-import_clients_batch.py file

file = 'clients.csv'
schema = 'sc_stage_cloudwalk'
table = 'stg_clients'

input_stage_data(file, schema, table)


# 2 Example usage to insert or update a client
insert_or_update_client(user_id=1,
                        created_at='2023-09-18 16:05:00',
                        status="approved",
                        batch=1,
                        credit_limit=47050,
                        interest_rate=30)


# 3 Example usage: Execute SQL script from file
execute_stored_procedure()


# 4 Using the function input_stage_data from 1-import_loans_batch.py file
file = 'loans.csv'
schema = 'sc_stage_cloudwalk'
table = 'stg_loans'

input_stage_data(file, schema, table)

"""