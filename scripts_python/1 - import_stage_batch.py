# %%
import pandas as pd
from sqlalchemy import create_engine


def input_stage_data (file, schema, table):
        """This function gets the file from a directory, connects to a postgresql database.
            After that the stage client tables is truncated and then loaded again.
            Once you have the stage table filled you should perform the "X" script to reflect this information in DM Layer
        """
        # Path CSV file
        path = r"C:\Users\Oslain Junior\OneDrive\profissional\Technical Case Cloudwalk\input_data"

        # Loading data into DataFrame
        clients = pd.read_csv(path+'\\'+file)

        # URI of connection in PostgreSQL
        postgres_uri = 'postgresql://cloudwalk:cloudwalk@localhost:5432/postgres'

        # Creating engine SQLAlchemy
        engine = create_engine(postgres_uri)

        #Define the schema
        engine.execute(f"SET search_path TO {schema}")

        #Truncate stage table in sc_stage_cloudwalk schema
        engine.execute(f"TRUNCATE TABLE "+schema+'.'+table) # "stg_clients"

        # Inserting data inside Postgresql SQL
        try:
            
            clients.to_sql(table, schema=schema, con=engine, index=False, if_exists='append')

            print("Data inserted successfully!")

        except Exception as e:
            print("Error inserting data:", e)

        finally:
            # Closing database connection
            engine.dispose()




#%%
            
file = 'clients.csv'
schema = 'sc_stage_cloudwalk'
table = 'stg_clients'

input_stage_data(file, schema, table)
 # %%
file = 'loans.csv'
schema = 'sc_stage_cloudwalk'
table = 'stg_loans'

input_stage_data(file, schema, table)
# %%
