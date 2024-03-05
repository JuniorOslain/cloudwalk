#%%

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="cloudwalk",
    password="cloudwalk",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query to get loan issuance data
cur.execute("""
    SELECT 
        EXTRACT(MONTH FROM created_at) AS month,
        COUNT(*) AS loan_quantity,
        SUM(loan_amount) AS total_amount
    FROM sc_dm_cloudwalk.dm_loans
    GROUP BY month
    ORDER BY month
""")

# Fetch all rows from the result set
rows = cur.fetchall()

columns = ['month', 'loan_quantity', 'total_amount']
df = pd.DataFrame(rows, columns=columns)

# Close cursor and connection
cur.close()
conn.close()

# Plotting the data
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot loan quantity on primary y-axis
ax1.bar(df['month'], df['loan_quantity'], color='blue', alpha=0.7, label='Loan Quantity')
ax1.set_xlabel('Month')
ax1.set_ylabel('Loan Quantity', color='blue')
ax1.tick_params('y', colors='blue')

# Create a secondary y-axis for total amount
ax2 = ax1.twinx()
ax2.plot(df['month'], df['total_amount'], color='red', marker='o', linestyle='-', linewidth=2, label='Total Amount')
ax2.set_ylabel('Total Amount ($)', color='red')
ax2.tick_params('y', colors='red')

# Adding legend
fig.tight_layout()
plt.title('Loan Issuance by Month')
plt.xticks(df['month'])
plt.grid(True)

# Adding legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.show()
# %%
#Another option to see the full timeline by year/mounth

import matplotlib.pyplot as plt

# Data from the query
year_month = ["202312", "202401", "202311", "202310", "202309", "202308", "202307", "202306", "202305", "202304",
              "202303", "202302", "202301", "202212", "202211", "202210", "202208", "202209", "202207", "202206",
              "202205", "202204", "202203", "202201", "202202", "202112", "202111", "202110", "202109", "202108",
              "202107", "202105", "202106", "202103", "202104", "202102", "202101", "202012", "202010", "202011",
              "202009", "202008", "202007", "202006", "202005", "202004", "202003", "202002", "202001"]
loan_quantity = [17351, 16123, 13269, 11593, 8976, 7792, 6713, 5894, 5325, 4624, 4334, 3610, 3566, 3309, 3055, 2858,
                 2507, 2513, 2347, 2124, 2011, 1842, 1790, 1515, 1430, 1399, 1246, 1187, 1096, 1032, 997, 849, 841,
                 763, 698, 551, 546, 495, 464, 430, 343, 314, 274, 224, 161, 145, 107, 59, 16]
total_amount = [442464966.00, 409112591.00, 330839275.00, 293005656.00, 229573371.00, 193164454.00, 168555063.00,
                147375148.00, 133772086.00, 116296080.00, 108927883.00, 90230173.00, 89852114.00, 82602369.00,
                75198263.00, 72964244.00, 62721494.00, 62239268.00, 58539111.00, 53142823.00, 50975116.00, 47196314.00,
                44671752.00, 38647669.00, 36459355.00, 35329381.00, 31657873.00, 31012651.00, 28357908.00, 25899061.00,
                25898185.00, 21540540.00, 20943661.00, 18965882.00, 17755313.00, 13727884.00, 12879301.00, 12378822.00,
                11477276.00, 10442335.00, 8852936.00, 7998350.00, 7086345.00, 5918356.00, 4323270.00, 3465180.00,
                2460062.00, 1723978.00, 348731.00]

# Plotting the bar chart
plt.figure(figsize=(12, 6))
plt.bar(year_month, loan_quantity, color='skyblue')
plt.xlabel('Year-Month')
plt.ylabel('Loan Quantity')
plt.title('Loan Quantity Over Time')
plt.xticks(rotation=90)
plt.tight_layout()

# Show plot
plt.show()

# %%

# 2 Which batch had the best overall adherence?

import matplotlib.pyplot as plt

# Data from the SQL query
batch = [1, 2, 3, 4]
total_loans = [98364, 37415, 8958, 5971]

# Plotting the bar chart
plt.figure(figsize=(8, 6))
plt.bar(batch, total_loans, color='skyblue')
plt.xlabel('Batch')
plt.ylabel('Total Loans')
plt.title('Total Loans by Batch')
plt.xticks(batch)
plt.tight_layout()
plt.show()


# %%
#3. Do different interest rates lead to different loan outcomes in terms of default rate?

#ANSWER - NO

import matplotlib.pyplot as plt

# Data
interest_rates = [20, 30, 70, 90]
default_loans = [3061, 3077, 3060, 3143]
default_rates = [0.0805, 0.0822, 0.0823, 0.0826]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.25
index = range(len(interest_rates))

# Plotting default loans
plt.bar([i + bar_width for i in index], default_loans, bar_width, label='Default Loans', color='orange')
plt.xlabel('Interest Rate')
plt.ylabel('Count')

# Creating a secondary y-axis for default rate
ax2 = ax.twinx()
ax2.plot([i + (bar_width * 2) for i in index], default_rates, marker='o', linestyle='-', color='green', label='Default Rate')
ax2.set_ylabel('Default Rate')

plt.title('Loan Outcomes by Interest Rate')
plt.xticks([i + bar_width for i in index], interest_rates)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()



# %%
#Rank the best 10 and 10 worst clients. Explain your methodology for constructing this ranking.
'''
There are a SQL Script to generate this result [scripts_sql\consultas_dataviz.sql]

/*Reasoning
Best Clients - 
1 - all customers who paid their loans 100%
2 - customers who have loyalty taking more than 1 loan
3 - customers who took out large loans and brought a difference in total owed vs. total paid, which gives the company more profit.
Worst Clients - 
1- all customers who broke their loans
2 - with the biggest difference due in our customer base considering total due vs total paid
'''
import pandas as pd

# Creating the table through a dictionary
data = {
    "user_id": [
        77087, 44244, 28742, 41151, 11529,
        16557, 70705, 58861, 12241, 23742,
        66899, 30138, 8934, 89832, 20291,
        49266, 34726, 80125, 81110, 73637
    ],
    "qtd_loans": [
        7, 5, 5, 5, 5,
        6, 5, 6, 4, 5,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1
    ],
    "total_loan_amount": [
        457594.00, 362316.00, 352145.00, 320096.00, 309072.00,
        306955.00, 300277.00, 298582.00, 294229.00, 289923.00,
        96486.00, 93237.00, 92081.00, 93087.00, 86799.00,
        85674.00, 97846.00, 86824.00, 79051.00, 84832.00
    ],
    "avg_loan_amount": [
        65370.57, 72463.20, 70429.00, 64019.20, 61814.40,
        51159.17, 60055.40, 49763.67, 73557.25, 57984.60,
        96486.00, 93237.00, 92081.00, 93087.00, 86799.00,
        85674.00, 97846.00, 86824.00, 79051.00, 84832.00
    ],
    "max_loan_amount": [
        89781.00, 84734.00, 89611.00, 89522.00, 73688.00,
        86404.00, 72757.00, 77301.00, 94692.00, 70606.00,
        96486.00, 93237.00, 92081.00, 93087.00, 86799.00,
        85674.00, 97846.00, 86824.00, 79051.00, 84832.00
    ],
    "credit_limit": [
        93750.00, 99500.00, 90000.00, 92500.00, 80500.00,
        89250.00, 75250.00, 88750.00, 98250.00, 94000.00,
        97250.00, 96250.00, 94500.00, 95000.00, 92750.00,
        90500.00, 98250.00, 90750.00, 86000.00, 96750.00
    ],
    "amount_paid": [
        565668.55, 447887.79, 435314.61, 395696.28, 382068.62,
        379451.63, 371196.43, 369101.09, 363720.01, 358397.02,
        3345.00, 458.44, 1526.38, 2951.66, 592.04,
        5697.61, 23028.74, 5241.46, 696.33, 8228.78
    ],
    "due_amount": [
        565668.55, 447887.79, 435314.61, 395696.28, 382068.62,
        379451.63, 371196.43, 369101.09, 363720.01, 358397.02,
        119274.06, 115257.71, 109224.64, 110417.94, 107299.19,
        105908.49, 120955.27, 102988.89, 97721.27, 104867.62
    ],
    "total_difference_paid": [
        108074.55, 85571.79, 83169.61, 75600.28, 72996.62,
        72496.63, 70919.43, 70519.09, 69491.01, 68474.02,
        -93141.00, -92778.56, -90554.62, -90135.34, -86206.96,
        -79976.39, -74817.26, -81582.54, -78354.67, -76603.22
    ],
    "total_remaining": [
        0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00,
        115929.06, 114799.27, 107698.26, 107466.28, 106707.15,
        100210.88, 97926.53, 97747.43, 97024.94, 96638.84
    ],
    "group_clients": [
        "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS",
        "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS", "BEST CLIENTS",
        "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS",
        "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS", "WORST CLIENTS"
    ]
}

# Creating o DataFrame
df = pd.DataFrame(data)

# Showing o DataFrame
df


# %%
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="cloudwalk",
    password="cloudwalk",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query to get loan issuance data
cur.execute("""
    SELECT TO_CHAR(l.created_at, 'YYYY-MM')																	   AS yearmonth
		,batch
		,COUNT(CASE WHEN l.status = 'default' THEN 1 ELSE NULL END)/ CAST(COUNT(loan_id) AS NUMERIC(10,2)) AS "%_default_loans"
FROM sc_dm_cloudwalk.dm_loans l
INNER JOIN sc_dm_cloudwalk.dm_clients c 
ON l.user_id = c.user_id 
GROUP BY TO_CHAR(l.created_at, 'YYYY-MM'),batch
ORDER BY 1
""")

# Fetch all rows from the result set
rows = cur.fetchall()

columns = ['yearmonth', 'batch', '%_default_loans']
df = pd.DataFrame(rows, columns=columns)

df
#
# %%

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="cloudwalk",
    password="cloudwalk",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query to get loan issuance data
cur.execute("""SELECT
               TO_CHAR(created_at, 'YYYY-MM') AS issuance_month,
               COUNT(*) AS issued_loans
               FROM sc_dm_cloudwalk.dm_loans
               GROUP BY issuance_month
               ORDER BY issuance_month
            """)

# Fetch all rows from the result set
rows = cur.fetchall()

columns = ['issuance_month', 'issued_loans']

df = pd.DataFrame(rows, columns=columns)

# Convert the 'issuance_month' column to datetime format
df['issuance_month'] = pd.to_datetime(df['issuance_month'])

# Sort the DataFrame by the 'issuance_month' column
df.sort_values(by='issuance_month', inplace=True)

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(df['issuance_month'], df['issued_loans'], marker='o', color='blue', linestyle='-')
plt.title('Evolution of Loans Over Time')
plt.xlabel('Issuance Month')
plt.ylabel('Number of Issued Loans')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
