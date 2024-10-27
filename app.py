from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data (can be from a CSV file, database, or API)
data = pd.DataFrame({
    'Category': ['Home', 'Insights', 'Sales', 'Inventory'],  # 5 categories
    'Values': [100, 200, 300, 400]  # 5 corresponding values
})

# Set Page Configuration
st.set_page_config(page_title="Retail Store Visualization",page_icon="🏪" ,layout="wide")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu("Menu", 
                           ["Home", "Dashboard", "Sales", "Insights", 
                            "Product Analytics", "Customer Analysis"
                            ], 
                           icons=['house', 'speedometer', 'bar-chart', 
                                  'lightbulb', 'box', 'people', 
                                  ],
                           menu_icon="cast", 
                           default_index=0)

# Use the selected option to display the corresponding content
if selected == "Home":
    st.title("🏪 Retail Store Visualization")
    st.markdown("---")
    st.write("Welcome to the Retail Store Visualization! ✨")
    st.write("")  # Empty line for spacing
    st.write("This interactive data visualization provides insights into sales performance, customer behavior, and product trends in our online retail store. Explore various metrics such as total sales, popular products, and customer demographics to make informed business decisions.")

elif selected == "Dashboard":
    st.title("Dashboard")
    st.markdown("---")

    # Sample data for demonstration
    # You can replace this with your actual sales data
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'Sales': [15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000],
        'Product': ['Product A', 'Product B', 'Product C', 'Product A', 'Product B', 'Product C', 
                    'Product A', 'Product B', 'Product C', 'Product A', 'Product B', 'Product C'],
        'Quantity Sold': [150, 133, 125, 300, 233, 200, 450, 333, 250, 600, 433, 350]  # Quantity sold
    }
    df = pd.DataFrame(data)

    # Calculate total sales and sales by product
    total_sales = df['Sales'].sum()
    num_transactions = len(df)
    average_order_value = total_sales / num_transactions if num_transactions > 0 else 0
    customer_retention_rate = 75  # Example value

    # Group by product to get sales distribution
    sales_by_product = df.groupby('Product')['Sales'].sum().reset_index()

    # Display key metrics
    st.metric(label="Total Sales Revenue", value=f"${total_sales:,.2f}")
    st.metric(label="Number of Transactions", value=num_transactions)
    st.metric(label="Average Order Value", value=f"${average_order_value:,.2f}")
    st.metric(label="Customer Retention Rate", value=f"{customer_retention_rate}%")

    # Pie chart for sales distribution by product
    pie_chart_fig = px.pie(sales_by_product, values='Sales', names='Product', title='Sales Distribution by Product')
    st.plotly_chart(pie_chart_fig)

    # Bar chart for sales trends over time
    sales_trend_fig = px.bar(df, x='Date', y='Sales', title='Sales Trends Over Time', color='Product', barmode='group')
    st.plotly_chart(sales_trend_fig)

elif selected == "Sales":
    st.title("Sales Performance")
    st.markdown("---")
    st.write("Detailed reports and visualizations on sales trends and revenue.")

    # Sample data for demonstration
    # You can replace this with your actual sales data
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'Sales': [15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000],
        'Product': ['Product A', 'Product B', 'Product C', 'Product A', 'Product B', 'Product C', 
                    'Product A', 'Product B', 'Product C', 'Product A', 'Product B', 'Product C'],
        'Price': [100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200],  # Price per unit
        'Quantity Sold': [150, 133, 125, 300, 233, 200, 450, 333, 250, 600, 433, 350]  # Quantity soldz
    }
    df = pd.DataFrame(data)

    # Calculate total revenue
    df['Revenue'] = df['Price'] * df['Quantity Sold']

    # Line chart for revenue trends over time
    revenue_trend_fig = px.line(df, x='Date', y='Revenue', title='Revenue Trends Over Time', markers=True)
    st.plotly_chart(revenue_trend_fig)

    # Bar chart for revenue by product
    revenue_by_product_fig = px.bar(df, x='Product', y='Revenue', title='Revenue by Product', color='Product')
    st.plotly_chart(revenue_by_product_fig)

elif selected == "Insights":
    st.title("Insights")
    st.markdown("---")
    st.write("Explore insights into customer behavior and product performance.")

elif selected == "Product Analytics":
    st.title("Product Analytics")
    st.markdown("---")
    st.write("Analyze product performance, including bestsellers and inventory turnover.")

elif selected == "Customer Analysis":
    st.title("Customer Analysis")
    st.markdown("---")
    st.write("Insights into customer behavior, segmentation, and demographics.")


# # Filter data based on user selection
# filtered_data = data[data['Category'] == selected]

# # Display filtered data 
# st.write(f"Data for Category {selected}:")
# st.write(filtered_data)

# # Visualizations
# # Line Chart (using Matplotlib)
# st.subheader("Line Chart")
# fig, ax = plt.subplots()
# ax.plot(data['Category'], data['Values'], marker='o')
# ax.set_title("Category Values")
# ax.set_xlabel("Category")
# ax.set_ylabel("Values")
# st.pyplot(fig)

# # Bar Chart (using Plotly)
# st.subheader("Bar Chart")
# bar_chart = px.bar(data, x='Category', y='Values', title="Bar Chart of Category Values")
# st.plotly_chart(bar_chart)

# # Display summary statistics
# st.subheader("Summary Statistics")
# st.write(data.describe())
