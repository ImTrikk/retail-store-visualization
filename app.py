import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data (can be from a CSV file, database, or API)
data = pd.DataFrame({
    'Category': ['Key Metrics', 'B', 'C', 'D'],
    'Values': [100, 200, 300, 400]
})

# Dashboard title
st.title("Business Intelligence ")

# Sidebar for user input
st.sidebar.header("Sidebar")

# Select a category to filter data
category = st.sidebar.selectbox("Select Category", data['Category'].unique())

# Filter data based on user selection
filtered_data = data[data['Category'] == category]

# Display filtered data 
st.write(f"Data for Category {category}:")
st.write(filtered_data)

# Visualizations

# Line Chart (using Matplotlib)
st.subheader("Line Chart")
fig, ax = plt.subplots()
ax.plot(data['Category'], data['Values'], marker='o')
ax.set_title("Category Values")
ax.set_xlabel("Category")
ax.set_ylabel("Values")
st.pyplot(fig)

# Bar Chart (using Plotly)
st.subheader("Bar Chart")
bar_chart = px.bar(data, x='Category', y='Values', title="Bar Chart of Category Values")
st.plotly_chart(bar_chart)

# Display summary statistics
st.subheader("Summary Statistics")
st.write(data.describe())

