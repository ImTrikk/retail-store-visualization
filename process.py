import pandas as pd
data = pd.read_excel('Online Retail.xlsx')

data_clean = data.dropna(subset=['CustomerID', 'Description'])
data_clean = data_clean[data_clean['Quantity'] > 0]
data_clean = data_clean[data_clean['UnitPrice'] > 0]

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

data_clean = remove_outliers(data_clean, 'Quantity')
data_clean = remove_outliers(data_clean, 'UnitPrice')

data_clean['TotalPrice'] = data_clean['Quantity'] * data_clean['UnitPrice']

data_clean['InvoiceDate'] = pd.to_datetime(data_clean['InvoiceDate'])


data_clean['Day'] = data_clean['InvoiceDate'].dt.day
data_clean['Month'] = data_clean['InvoiceDate'].dt.month
data_clean['Year'] = data_clean['InvoiceDate'].dt.year
data_clean['Hour'] = data_clean['InvoiceDate'].dt.hour
data_clean['Minute'] = data_clean['InvoiceDate'].dt.minute


output_file = 'cleaned_data.csv'
data_clean.to_csv(output_file, index=False)

print(data_clean)

print(f"Data has been saved to {output_file}")

