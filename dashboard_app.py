import streamlit as st
import pandas as pd
import plotly.express as px # Plotly Express for interactive charts
import os

# --- Page Settings ---
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading Function (Cached for performance) ---
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Error: Data file not found at {file_path}. Please make sure 'cleaned_sales_data.csv' is in the same directory.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(file_path)
        # Convert 'Date' to datetime and handle invalid dates
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        # Convert 'Quantity' to numeric and handle missing values
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df.dropna(subset=['Quantity'], inplace=True)

        # Handle 'Price' column, ensure numeric and fill missing with median
        if 'Price' in df.columns:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            # Corrected inplace warning by direct assignment
            df.loc[:, 'Price'] = df['Price'].fillna(df['Price'].median()) 
        else:
            df['Price'] = 1 # Default price 1 agar column nahi hai (avoid multiplication error)
            st.warning("Price column not found. Revenue will be based on Quantity only.")

        df['Revenue'] = df['Quantity'] * df['Price'] # Calculate Revenue
        return df
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        return pd.DataFrame()

# --- Main Dashboard Logic ---
st.title('📈 Sales Performance Dashboard')

# Data load karein
data_file_path = 'cleaned_sales_data.csv'
df = load_data(data_file_path)

# --- Sidebar for Filters ---
st.sidebar.header("Filters")

if not df.empty:
    # Date Range Filter
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    # Using st.date_input for selecting date range
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on selected date range
    df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]

    # Product Name Filter
    all_products = sorted(df_filtered['Product Name'].unique().tolist())
    selected_products = st.sidebar.multiselect(
        "Select Products",
        options=all_products,
        default=all_products # By default, sab products selected honge
    )
    
    # Apply product filter
    df_filtered = df_filtered[df_filtered['Product Name'].isin(selected_products)]

    # Check if filtered data is empty
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
        # Agar data empty ho toh sirf header aur warning dikhayen
        st.header("Overall Sales Metrics")
        st.metric(label="Total Sales Quantity", value="0")
        st.metric(label="Total Revenue", value="$0.00")
        st.metric(label="Unique Products Sold", value="0")
        st.subheader("Charts")
        st.info("Please adjust filters to see data.")
    else:
        # --- Overview Section ---
        st.header("Overall Sales Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            total_quantity = int(df_filtered['Quantity'].sum())
            st.metric(label="Total Sales Quantity", value=f"{total_quantity:,}")
        
        with col2:
            total_revenue = df_filtered['Revenue'].sum()
            st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
        
        with col3:
            unique_products = df_filtered['Product Name'].nunique()
            st.metric(label="Unique Products Sold", value=f"{unique_products:,}")

        # --- Charts Section ---
        st.header("Sales Analysis Charts")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("Top 10 Products by Sales Quantity")
            top_products = df_filtered.groupby('Product Name')['Quantity'].sum().nlargest(10).reset_index()
            fig_top_products = px.bar(
                top_products, 
                x='Quantity', 
                y='Product Name', 
                orientation='h', # Horizontal bar chart
                title='Quantity Sold',
                labels={'Quantity':'Total Quantity Sold', 'Product Name':'Product'},
                height=400,
                color='Quantity', # Bars ko quantity ke hisaab se color karein
                color_continuous_scale=px.colors.sequential.Plotly3 # Color scheme
            )
            fig_top_products.update_layout(yaxis_title='', xaxis_title='Total Quantity Sold') # Titles adjust karein
            fig_top_products.update_yaxes(categoryorder='total ascending') # Products ko quantity ke hisaab se sort karein
            st.plotly_chart(fig_top_products, use_container_width=True) # Plotly chart display karein

        with chart_col2:
            st.subheader("Sales Trend Over Time (Revenue)")
            # Daily revenue calculate karein
            daily_revenue = df_filtered.groupby(df_filtered['Date'].dt.date)['Revenue'].sum().reset_index()
            daily_revenue.columns = ['Date', 'Revenue'] # Column names theek karein
            
            fig_sales_trend = px.line(
                daily_revenue,
                x='Date',
                y='Revenue',
                title='Daily Revenue Trend',
                labels={'Date':'Date', 'Revenue':'Total Revenue'},
                height=400,
                markers=True # Data points par markers dikhayen
            )
            fig_sales_trend.update_layout(xaxis_title='Date', yaxis_title='Total Revenue ($)')
            st.plotly_chart(fig_sales_trend, use_container_width=True)

        # --- Cleaned Data Preview (Optional, can be removed in final product) ---
        st.subheader("Filtered Data Preview")
        st.dataframe(df_filtered.head(10)) # Filtered data ki pehli 10 rows display karein

else:
    st.warning("Dashboard run nahi ho sakta kyunki data load nahi hua ya empty hai. Please 'cleaned_sales_data.csv' file check karein aur ensure karein ke usmein data hai.")

