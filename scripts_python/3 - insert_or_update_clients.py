#%%
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, func

def insert_client(user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason=None, denied_at=None):
    """
    Insert a new client an existing client in the dm_clients table.

    Parameters:
    user_id (int): The user ID of the client.
    created_at (datetime): The creation date of the client.
    status (str): The status of the client (e.g., "approved", "denied").
    batch (int): The batch to which the client belongs.
    credit_limit (int): The credit limit assigned to the client.
    interest_rate (int): The annual interest rate assigned to the client.
    denied_reason (str, optional): The reason for denial of the client.
    denied_at (datetime, optional): The date and time when the client was denied.

    """
    try:
        # Connection URI for PostgreSQL
        postgres_uri = 'postgresql://cloudwalk:cloudwalk@localhost:5432/postgres'
        
        # Creating engine with SQLAlchemy
        engine = create_engine(postgres_uri)

        # Getting metadata
        meta = MetaData()

        # Reflect the existing table structure
        dm_clients_table = Table('dm_clients', meta, autoload_with=engine, schema='sc_dm_cloudwalk')

        # Inserting data into the dm_clients table
        ins = dm_clients_table.insert().values(
            user_id=user_id,
            created_at=created_at,
            status=status,
            batch=batch,
            credit_limit=credit_limit,
            interest_rate=interest_rate,
            denied_reason=denied_reason,
            denied_at=denied_at
        )

        engine.execute(ins)

        print("Client inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        # Closing the database connection
        engine.dispose()

def insert_or_update_client(user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason=None, denied_at=None):
    """
    Insert a new client or update an existing client in the dm_clients table.

    Parameters:
    user_id (int): The user ID of the client.
    created_at (datetime): The creation date of the client.
    status (str): The status of the client (e.g., "approved", "denied").
    batch (int): The batch to which the client belongs.
    credit_limit (int): The credit limit assigned to the client.
    interest_rate (int): The annual interest rate assigned to the client.
    denied_reason (str, optional): The reason for denial of the client.
    denied_at (datetime, optional): The date and time when the client was denied.

    """
    try:
        # Connection URI for PostgreSQL
        postgres_uri = 'postgresql://cloudwalk:cloudwalk@localhost:5432/postgres'
        
        # Creating engine with SQLAlchemy
        engine = create_engine(postgres_uri)

        # Getting metadata
        meta = MetaData()

        # Reflect the existing table structure
        dm_clients_table = Table('dm_clients', meta, autoload_with=engine, schema='sc_dm_cloudwalk')

        # Check if user_id already exists in the table
        existing_user = engine.execute(dm_clients_table.select().where(dm_clients_table.c.user_id == user_id)).fetchone()

        if existing_user:
            # If user exists, update the record
            upd = dm_clients_table.update().where(dm_clients_table.c.user_id == user_id).values(
                created_at=created_at,
                status=status,
                batch=batch,
                credit_limit=credit_limit,
                interest_rate=interest_rate,
                denied_reason=denied_reason,
                denied_at=denied_at,
                dt_updated = func.current_timestamp()
            )
            engine.execute(upd)
            print("Client updated successfully!")

        else:
            # If user does not exist, insert a new record
            insert_client(user_id, created_at, status, batch, credit_limit, interest_rate, denied_reason, denied_at)

    except Exception as e:
        print("Error:", e)

    finally:
        # Closing the database connection
        engine.dispose()
#%%
# Example usage to insert or update a client
insert_or_update_client(user_id=1,
                        created_at='2023-09-18 16:05:00',
                        status="approved",
                        batch=1,
                        credit_limit=47050,
                        interest_rate=30)


# %%
