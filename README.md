# Project to show structure carried out on the proposed assessment by Cloudwalk.

This repository contains a simple Loan Management System (LMS) implemented using Python and PostgreSQL. The system includes functionalities to send daily payment reminders to clients with ongoing loans and to generate weekly activity summaries.

## Folder Structure

Technical Case Cloudwalk
  input_data
  scripts_sql
  scripts_python
  output_dataviz

## Prerequisites

Before running the application, ensure you have the following installed:

- Python (version 3.6 or higher)
- PostgreSQL (version 9.6 or higher)
- psycopg2 (Python PostgreSQL adapter)
- pandas (Python Data Analysis Library)
- smtplib (Python SMTP client)
- email.mime (Python email library)

## Setup

### Set up the PostgreSQL database:

1. Create a database named postgres.
2. Create two schemas named with this file: "Technical Case Cloudwalk\scripts_sql\1-create_schemas.sql"
3. Create clients and loans stage tables: "Technical Case Cloudwalk\scripts_sql\2-create_tables_stage.sql"
4. Create clients and loans dm tables: "Technical Case Cloudwalk\scripts_sql\3-create_tables_dm.sql"
5. Create a trigger in order to control all changes in clients dm table: "Technical Case Cloudwalk\scripts_sql\4-create_trigger_clients.sql"
6. Create a user stored procedure to load the dm tables from stage tables: "Technical Case Cloudwalk\scripts_sql\5-create_usp_etl_clients.sql"

### Performing Python Scripts

1. `import_stage_batch.py` - uploading the files from the directory
2. `execute_clients_etl_stg_to_dm.py` - moving the stage data to the dm data. This case will run the trigger to INSERT, UPDATE and DELETE
3. `insert_or_update_clients.py` - function to include or update clients.
4. `execute_loans_etl_stg_to_dm.py` - moving the stage data to the dm data. There are no duplicities.
5. `data_viz.py` - Notebook answering the questions. Some of them are with lists or dictionaries to perform the script without database connection.
6. Folder `output_dataviz` with graphs.
7. `email.py` - to send daily or weekly emails with information about the loans.
8. `orchestration_process.py` - Done to manage the processes and perform it daily it doesn't matter the data source.

## Acknowledgments

Inspiration: Cloudwalk

## Author

Oslain Junior
