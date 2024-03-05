#%%
import psycopg2

def execute_stored_procedure_etl_loans():
    try:
        # Connection parameters
        conn_params = {
            "user": "cloudwalk",
            "password": "cloudwalk",
            "host": "localhost",
            "port": "5432",
            "database": "postgres"
        }

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**conn_params)

        # Create a cursor object
        cursor = conn.cursor()

        # Call the stored procedure
        cursor.execute("CALL sc_dm_cloudwalk.usp_etl_loans()")

        # Commit the transaction
        conn.commit()

        print("Stored procedure executed successfully!")

    except Exception as e:
        print("Error executing stored procedure:", e)

    finally:
        # Closing the cursor and connection
        cursor.close()
        conn.close()

# %%
# Example usage: Execute SQL script from file
execute_stored_procedure_etl_loans()

# %%
