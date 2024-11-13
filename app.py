from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2

# Set Page Configuration
st.set_page_config(page_title="Retail Store Visualization", page_icon="🏪", layout="wide")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# load cleaned data
# database connection 
# Function to create a database connection
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="OnlineRetaildb",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Load data from the database
def load_data(query):
    conn = create_connection()
    if conn:
        try:
            data = pd.read_sql(query, conn)
            print(data.columns)  # Print column names for debugging
            print(data.head())  # Print the first few rows of the DataFrame
            if data.empty:
                print("No data returned from the query.")  # Debugging output
            return data
        except Exception as e:
            st.error(f"Error reading from the database: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error
        finally:
            conn.close()
    return pd.DataFrame()  # Return empty DataFrame if connection

# query for data mining

#kpi
query = """
SELECT 
    pd.description AS product_name,
    pd.stockcode,
    sls.quantity,
    sls.unitprice,
    sls.totalprice,
    c.country,
    t.year,
    t.month,
    t.day,
    COUNT(DISTINCT sls.invoiceno) as total_orders,
    COUNT(DISTINCT sls.customerid) as unique_customers
FROM 
    sales sls 
JOIN 
    product pd ON sls.stockcode = pd.stockcode 
JOIN 
    customer c ON c.customerid = sls.customerid 
JOIN 
    time t ON t.timeid = sls.timeid 
GROUP BY 
    pd.description, pd.stockcode, sls.quantity, sls.unitprice, 
    sls.totalprice, c.country, t.year, t.month, t.day
ORDER BY 
    t.year, t.month, t.day;
"""

data = load_data(query)


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
    
    # Data Overview Section
    st.markdown("## Data Overview")
    
    # Create tabs for different views of the data
    tab1, tab2, tab3 = st.tabs(["📊 Data Sample", "📈 Summary Statistics", "ℹ️ Data Info"])
    
    with tab1:
        # Display sample of the data
        st.markdown("### Sample Data")
        st.dataframe(
            data.head(10),
            use_container_width=True
        )
        
        # Display total number of records
        st.info(f"Total number of records: {len(data):,}")
        
    with tab2:
        # Display summary statistics
        st.markdown("### Summary Statistics")
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Numeric Columns**")
            numeric_summary = data.describe()[['quantity', 'unitprice', 'totalprice']].round(2)
            st.dataframe(numeric_summary, use_container_width=True)
            
        with col2:
            st.markdown("**Categorical Columns**")
            categorical_summary = pd.DataFrame({
                'Country': data['country'].value_counts().head(),
                'Products': data['product_name'].value_counts().head()
            })
            st.dataframe(categorical_summary, use_container_width=True)
    
    with tab3:
        # Display data information
        st.markdown("### Dataset Information")
        
        # Create columns for different metrics
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.metric("Total Countries", data['country'].nunique())
            st.metric("Total Products", data['product_name'].nunique())
            
        with info_col2:
            st.metric("Date Range", f"{data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
            st.metric("Total Orders", data['total_orders'].sum())
            
        with info_col3:
            st.metric("Total Revenue", f"${data['totalprice'].sum():,.2f}")
            st.metric("Unique Customers", data['unique_customers'].sum())
    
    # Data Dictionary
    st.markdown("## Data Dictionary")
    
    dict_data = {
        'Column': ['product_name', 'stockcode', 'quantity', 'unitprice', 'totalprice', 'country', 'year', 'month', 'day', 'total_orders', 'unique_customers'],
        'Description': [
            'Description of the product',
            'Product stock code',
            'Quantity of items purchased',
            'Price per unit',
            'Total price of the transaction',
            'Country where the order was placed',
            'Year of the transaction',
            'Month of the transaction',
            'Day of the transaction',
            'Total number of orders',
            'Number of unique customers'
        ],
        'Type': [
            'String',
            'String',
            'Integer',
            'Float',
            'Float',
            'String',
            'Integer',
            'Integer',
            'Integer',
            'Integer',
            'Integer'
        ]
    }
    
    st.dataframe(
        pd.DataFrame(dict_data),
        use_container_width=True,
        hide_index=True
    )

elif selected == "Dashboard":
    st.title("📈Dashboard")
    st.markdown("---")

    # Create columns for KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    total_sales = data['totalprice'].sum()
    total_orders = data['total_orders'].sum()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    unique_customers = data['unique_customers'].sum()
    
    # Display KPIs
    with col1:
        st.metric("Total Revenue", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Orders", f"{total_orders:,}")
    with col3:
        st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    with col4:
        st.metric("Unique Customers", f"{unique_customers:,}")

    # Create two columns for charts
    col_left, col_right = st.columns(2)

    with col_left:
        # Sales by Country
        sales_by_country = data.groupby('country')['totalprice'].sum().reset_index()
        country_fig = px.choropleth(sales_by_country, 
                                  locations='country',
                                  locationmode='country names',
                                  color='totalprice',
                                  title='Sales Distribution by Country',
                                  color_continuous_scale='Viridis')
        st.plotly_chart(country_fig, use_container_width=True)

        # Top Products by Revenue
        top_products = data.groupby('product_name')['totalprice'].sum().nlargest(10).reset_index()
        product_fig = px.bar(top_products, 
                           x='product_name', 
                           y='totalprice',
                           title='Top 10 Products by Revenue',
                           labels={'product_name': 'Product', 'totalprice': 'Revenue'})
        st.plotly_chart(product_fig, use_container_width=True)

    with col_right:
        # Monthly Sales Trend
        monthly_sales = data.groupby(['year', 'month'])['totalprice'].sum().reset_index()
        monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(DAY=1))
        trend_fig = px.line(monthly_sales, 
                          x='date', 
                          y='totalprice',
                          title='Monthly Sales Trend',
                          labels={'date': 'Month', 'totalprice': 'Revenue'})
        st.plotly_chart(trend_fig, use_container_width=True)

        # Average Order Value by Country
        aov_by_country = (data.groupby('country')['totalprice'].sum() / 
                         data.groupby('country')['total_orders'].sum()).reset_index()
        aov_fig = px.bar(aov_by_country,
                        x='country',
                        y='totalprice',
                        title='Average Order Value by Country',
                        labels={'country': 'Country', 'totalprice': 'Average Order Value'})
        st.plotly_chart(aov_fig, use_container_width=True)

elif selected == "Sales":
    st.title("📊Sales Performance")
    st.markdown("---")
    
    # Time period selector
    time_period = st.selectbox(
        "Select Time Period",
        ["Daily", "Weekly", "Monthly", "Yearly"]
    )
    
    # Create date column for easier manipulation
    data['date'] = pd.to_datetime(data[['year', 'month', 'day']].assign(hour=0))
    
    # Aggregate data based on selected time period
    if time_period == "Daily":
        sales_over_time = data.groupby(['year', 'month', 'day'])['totalprice'].sum().reset_index()
        sales_over_time['date'] = pd.to_datetime(sales_over_time[['year', 'month', 'day']])
        x_axis = 'date'
    elif time_period == "Weekly":
        sales_over_time = data.groupby([pd.Grouper(key='date', freq='W')])['totalprice'].sum().reset_index()
        x_axis = 'date'
    elif time_period == "Monthly":
        sales_over_time = data.groupby(['year', 'month'])['totalprice'].sum().reset_index()
        sales_over_time['date'] = pd.to_datetime(sales_over_time[['year', 'month']].assign(day=1))
        x_axis = 'date'
    else:  # Yearly
        sales_over_time = data.groupby('year')['totalprice'].sum().reset_index()
        x_axis = 'year'

    # Create two columns for the first row of charts
    col1, col2 = st.columns(2)

    with col1:
        # Revenue Trend
        revenue_trend_fig = px.line(
            sales_over_time,
            x=x_axis,
            y='totalprice',
            title=f'Revenue Trends ({time_period})',
            labels={'totalprice': 'Revenue', 'date': 'Date'},
            markers=True
        )
        revenue_trend_fig.update_layout(xaxis_title=time_period)
        st.plotly_chart(revenue_trend_fig, use_container_width=True)

    with col2:
        # Sales by Country
        sales_by_country = data.groupby('country')['totalprice'].sum().reset_index()
        country_sales_fig = px.bar(
            sales_by_country.sort_values('totalprice', ascending=False),
            x='country',
            y='totalprice',
            title='Sales by Country',
            labels={'totalprice': 'Revenue', 'country': 'Country'}
        )
        st.plotly_chart(country_sales_fig, use_container_width=True)

    # Create two columns for the second row of charts
    col3, col4 = st.columns(2)

    with col3:
        # Top Products
        top_n = st.slider('Select number of top products to display', 5, 20, 10)
        top_products = data.groupby('product_name')['totalprice'].sum().nlargest(top_n).reset_index()
        product_sales_fig = px.bar(
            top_products,
            x='product_name',
            y='totalprice',
            title=f'Top {top_n} Products by Revenue',
            labels={'totalprice': 'Revenue', 'product_name': 'Product'}
        )
        product_sales_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(product_sales_fig, use_container_width=True)

    with col4:
        # Sales Distribution by Hour
        hourly_sales = data.groupby('hour')['totalprice'].sum().reset_index()
        hour_sales_fig = px.line(
            hourly_sales,
            x='hour',
            y='totalprice',
            title='Sales Distribution by Hour',
            labels={'totalprice': 'Revenue', 'hour': 'Hour of Day'}
        )
        hour_sales_fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        st.plotly_chart(hour_sales_fig, use_container_width=True)

    # Additional Metrics Section
    st.markdown("### Detailed Metrics")
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        avg_order_value = data['totalprice'].mean()
        st.metric("Average Order Value", f"${avg_order_value:,.2f}")

    with metric_col2:
        total_orders = data['total_orders'].sum()
        st.metric("Total Orders", f"{total_orders:,}")

    with metric_col3:
        total_revenue = data['totalprice'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")

    # Interactive Data Table
    st.markdown("### Detailed Sales Data")
    show_data = st.checkbox("Show Raw Data")
    if show_data:
        st.dataframe(
            data[['date', 'product_name', 'quantity', 'unitprice', 'totalprice', 'country']]
            .sort_values('date', ascending=False)
        )

# elif selected == "Insights":
#     st.title("📑Insights")
#     st.markdown("---")
#     st.write("Explore insights into customer behavior and product performance.")

# elif selected == "Product Analytics":
#     st.title("👘Product Analytics")
#     st.markdown("---")
#     st.write("Analyze product performance, including bestsellers and inventory turnover.")

# elif selected == "Customer Analysis":
#     st.title("🧑‍🦰Customer Analysis")
#     st.markdown("---")
#     st.write("Insights into customer behavior, segmentation, and demographics.")
