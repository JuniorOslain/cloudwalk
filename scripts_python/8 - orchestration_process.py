import schedule
import time
import subprocess
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import psycopg2

# Function to execute the data import script to the stage
def import_stage_data():
    subprocess.run(["python", "import_stage_batch.py"])

# Function to execute ETL for clients (Stage to Data Mart)
def execute_clients_etl():
    subprocess.run(["python", "2 - execute_clients_etl_stg_to_dm.py"])

# Function to execute ETL for loans (Stage to Data Mart)
def execute_loans_etl():
    subprocess.run(["python", "4 - execute_loans_etl_stg_to_dm.py"])

# Function to send the weekly activity summary via email
def send_weekly_summary():
    # Connect to the database
    conn = psycopg2.connect(
        dbname="postgres",
        user="cloudwalk",
        password="cloudwalk",
        host="localhost",
        port="5432"
    )

    # Query to retrieve weekly activity summary
    query = """
        SELECT COUNT(DISTINCT l.loan_id) AS total_loans_issued,
               SUM(l.amount_paid) AS total_amount_paid,
               AVG(CASE WHEN l.paid_at <= l.due_at THEN 1 ELSE 0 END) * 100 AS percentage_paid_on_time,
               COUNT(CASE WHEN l.status = 'default' THEN 1 END) AS total_defaulted_loans
        FROM sc_dm_cloudwalk.dm_loans l
        WHERE l.created_at >= TIMESTAMP '2024-02-25 00:00:00' - INTERVAL '7 days'
    """

    # Execute the query
    summary_df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Check if DataFrame is not empty
    if not summary_df.empty:
        # Get the summary data
        total_loans_issued = summary_df['total_loans_issued'].iloc[0]
        total_amount_paid = summary_df['total_amount_paid'].iloc[0]
        percentage_paid_on_time = summary_df['percentage_paid_on_time'].iloc[0]
        total_defaulted_loans = summary_df['total_defaulted_loans'].iloc[0]

        # Construct the email content
        subject = "Weekly Activity Summary"
        body = f"""
            Dear Team/Recipient,
            Here's a summary of our operation activities for the week:
            - Total Loans Issued: {total_loans_issued}
            - Total Amount Paid: $ {total_amount_paid}
            - Percentage of Loans Paid on Time: {percentage_paid_on_time}%
            - Number of Defaulted Loans: {total_defaulted_loans}
            Please review the attached report for more details.
            Regards,
            Your Company
        """

        # Sending the email
        send_email(subject, body, "recipient@example.com")

# Function to send emails
def send_email(subject, body, recipient):
    # Email server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'noreply.cloudwalk@gmail.com'
    sender_password = 'cloudwalk'

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(body, 'plain'))

    # Initialize SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to SMTP server
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient, msg.as_string())

    # Close SMTP server connection
    server.quit()

# Schedule daily tasks
schedule.every().day.at("00:00").do(import_stage_data)
schedule.every().day.at("01:00").do(execute_clients_etl)
schedule.every().day.at("02:00").do(execute_loans_etl)

# Schedule weekly task
schedule.every().sunday.at("03:00").do(send_weekly_summary)

# Loop to execute the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait for 60 seconds before checking scheduled tasks again
