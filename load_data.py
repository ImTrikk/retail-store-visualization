import pandas as pd
import psycopg2

# Import cleaned data from ETL
cleaned_data = pd.read_csv('cleaned_data.csv')

# Connect DB
conn = psycopg2.connect(
    host="localhost",
    database="OnlineRetaildb",
    user="postgres",
    password="admin",
    port="5432"
)
cursor = conn.cursor()

# Insert customers
customers = cleaned_data[['CustomerID', 'Country']].drop_duplicates()

customer_insert_query = """
    INSERT INTO Customer (customerID, country) 
    VALUES (%s, %s)
    ON CONFLICT (customerID) DO NOTHING;
"""
customer_values = [
    (row['CustomerID'], row['Country'] if pd.notna(row['Country']) else 'Unknown')
    for index, row in customers.iterrows()
]
cursor.executemany(customer_insert_query, customer_values)
conn.commit()

# Insert products
products = cleaned_data[['StockCode', 'Description']].drop_duplicates()

product_insert_query = """
    INSERT INTO Product (stockCode, description)
    VALUES (%s, %s)
    ON CONFLICT (stockCode) DO NOTHING;
"""
product_values = [
    (row['StockCode'], row['Description'])
    for index, row in products.iterrows()
]
cursor.executemany(product_insert_query, product_values)
conn.commit()

# Insert time
time_data = cleaned_data[['Day', 'Month', 'Year', 'Hour', 'Minute']].drop_duplicates()

time_insert_query = """
    INSERT INTO time (day, month, year, hour, minute)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    RETURNING timeID;
"""
time_values = [
    (int(row['Day']), int(row['Month']), int(row['Year']), int(row['Hour']), int(row['Minute']))
    for index, row in time_data.iterrows()
]

# Insert each time value and store the corresponding timeID in a dictionary for later lookup
time_map = {}
for index, time_row in enumerate(time_values):
    cursor.execute(time_insert_query, time_row)
    timeID = cursor.fetchone()[0]
    time_map[time_row] = timeID

conn.commit()

# Insert sales
sales_insert_query = """
    INSERT INTO Sales (invoiceNo, customerID, stockCode, timeID, quantity, unitPrice, totalPrice)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""

sales_values = []
for index, row in cleaned_data.iterrows():
    time_tuple = (row['Day'], row['Month'], row['Year'], row['Hour'], row['Minute'])
    timeID = time_map.get(time_tuple)
    
    if timeID:
        sales_values.append((
            row['InvoiceNo'], 
            row['CustomerID'], 
            row['StockCode'], 
            timeID, 
            row['Quantity'], 
            row['UnitPrice'], 
            row['TotalPrice']
        ))

cursor.executemany(sales_insert_query, sales_values)
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Data has been successfully inserted into the database.")

