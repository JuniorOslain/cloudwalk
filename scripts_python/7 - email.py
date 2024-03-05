import psycopg2
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Function to connect to the database
def connect_to_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="cloudwalk",
        password="cloudwalk",
        host="localhost"
    )
    return conn

# Function to execute SQL queries and return a Pandas DataFrame
def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=columns)
    cur.close()
    return df

# Function to send emails
def send_email(subject, body, recipient):
    # Email server settings
    smtp_server = 'smtp.cloudwalk.com'  # Change to your SMTP server
    smtp_port = 587  # Change as needed
    sender_email = 'noreply.cloudwalk@gmail.com'  # Change to your email address
    sender_password = 'cloudwalk'  # Change to your email password

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

# Function to send daily payment reminders
def send_payment_reminder(conn):
    query = """
        SELECT c.user_id, c.created_at, c.status, c.batch, c.credit_limit, c.interest_rate, c.denied_reason, 
               c.denied_at, c.dt_updated, l.loan_id, l.due_at, l.created_at, l.paid_at, l.status, l.loan_amount,
               l.tax, l.due_amount, l.amount_paid, l.dt_updated
        FROM sc_dm_cloudwalk.dm_clients c
        INNER JOIN sc_dm_cloudwalk.dm_loans l ON c.user_id = l.user_id
        WHERE l.status = 'ongoing'
          AND l.due_at >= TIMESTAMP '2024-02-25 00:00:00'
          AND l.due_at <= TIMESTAMP '2024-02-25 00:00:00' + INTERVAL '3 days'
    """
    reminders_df = execute_query(conn, query)
    for index, row in reminders_df.iterrows():
        # Construct email body with DataFrame data
        recipient = "email@example.com"  # Replace with recipient's email
        subject = "Loan Payment Reminder"
        body = f"""
            Hello {row['user_id']},
            This is a friendly reminder that your loan payment of $ {row['loan_amount']} is due on {row['due_at']}. 
            Please ensure timely payment to avoid any additional charges.
            Thank you for choosing our services.
            Best regards,
            Your Company
        """
        # Send the email
        send_email(subject, body, recipient)

# Function to send weekly summary of activities
def send_weekly_summary(conn):
    query = """
        SELECT COUNT(DISTINCT l.loan_id) AS total_loans_issued,
               SUM(l.amount_paid) AS total_amount_paid,
               AVG(CASE WHEN l.paid_at <= l.due_at THEN 1 ELSE 0 END) * 100 AS percentage_paid_on_time,
               COUNT(CASE WHEN l.status = 'default' THEN 1 END) AS total_defaulted_loans
        FROM sc_dm_cloudwalk.dm_loans l
        WHERE l.created_at >= TIMESTAMP '2024-02-25 00:00:00' - INTERVAL '7 days'
    """
    summary_df = execute_query(conn, query)
    for index, row in summary_df.iterrows():
        # Construct email body with DataFrame data
        recipient = "user@example.com"  # Replace with recipient's email
        subject = "Weekly Activity Summary"
        body = f"""
            Dear Team/Recipient,
            Here's a summary of our operation activities for the week:
            - Total Loans Issued: {row['total_loans_issued']}
            - Total Amount Paid: $ {row['total_amount_paid']}
            - Percentage of Loans Paid on Time: {row['percentage_paid_on_time']}%
            - Number of Defaulted Loans: {row['total_defaulted_loans']}
            Please review the attached report for more details.
            Regards,
            Your Company
        """
        # Send the email
        send_email(subject, body, recipient)

# Connect to the database
conn = connect_to_database()

# Execute email sending functions
send_payment_reminder(conn)
send_weekly_summary(conn)

# Close the database connection
conn.close()
