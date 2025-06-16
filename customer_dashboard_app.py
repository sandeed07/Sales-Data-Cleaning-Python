import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Configuration ---
CUSTOMER_DATA_FILE = 'customer_rfm_data.csv'

# --- Page Settings ---
st.set_page_config(
    page_title="Customer Segmentation & CLV Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Decoration ---
# Yeh CSS aapke dashboard ki look and feel ko change karega.
# Aap ismein colors, fonts, spacing, buttons, etc. customize kar sakte hain.
st.markdown(
    """
    <style>
    /* General Body Styling */
    body {
        font-family: 'Inter', sans-serif; /* Google Fonts ka Inter font */
        color: #333333; /* Default text color */
        background-color: #f0f2f6; /* Light gray background */
    }

    /* Main Title Styling */
    .css-fg4ri6 h1 { /* Streamlit ka auto-generated class for title */
        color: #4A00B7; /* Dark purple color */
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #e0e0e0;
        font-weight: 700;
        font-size: 2.5em;
    }

    /* Headers (h2, h3) Styling */
    .st-emotion-cache-1jm692z h2, .st-emotion-cache-1jm692z h3 { /* Another auto-generated class for headers */
        color: #007bff; /* Blue color for section headers */
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Sidebar Styling */
    .st-emotion-cache-1l0bgz .st-emotion-cache-1l0bgz { /* Sidebar background */
        background-color: #ffffff; /* White sidebar background */
        padding: 20px;
        border-right: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Metric Cards Styling (Total Customers, Avg Recency etc.) */
    [data-testid="stMetric"] {
        background-color: #ffffff; /* White background for metric cards */
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }

    [data-testid="stMetric"] label {
        color: #555555; /* Label color */
        font-size: 0.9em;
        margin-bottom: 5px;
    }

    [data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #2c3e50; /* Value color */
        font-size: 1.8em;
        font-weight: 700;
    }

    /* General containers for charts/dataframes */
    .st-emotion-cache-nahz7x { /* Main container for sections */
        background-color: #ffffff;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Button Styling (Example) */
    .st-emotion-cache-lq6ncu button {
        background-color: #007bff; /* Blue button */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    .st-emotion-cache-lq6ncu button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }

    /* Warning/Error Messages */
    .st-emotion-cache-1cxhxxt p { /* Streamlit warning/error messages */
        background-color: #fff3cd; /* Light yellow background */
        color: #856404;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Data Loading Function (Cached for performance) ---
@st.cache_data
def load_customer_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Error: Customer data file not found at {file_path}. Please make sure 'customer_rfm_data.csv' is in the same directory.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(file_path)
        # Ensure numeric columns are correct type
        numeric_cols = ['Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'Overall_Score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=numeric_cols, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading or processing customer data: {e}")
        return pd.DataFrame()

# --- Main Dashboard Logic ---
st.title('👥 Customer Segmentation & Lifetime Value (CLV) Dashboard')

# Load customer data
customer_df = load_customer_data(CUSTOMER_DATA_FILE)

if customer_df.empty:
    st.warning("Dashboard run nahi ho sakta kyunki customer data load nahi hua ya empty hai. Please 'customer_rfm_data.csv' file check karein.")
else:
    # --- Sidebar for Filters ---
    st.sidebar.header("Filters")
    
    # Segment Filter
    all_segments = ['All Segments'] + sorted(customer_df['Segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox(
        "Select Customer Segment",
        options=all_segments,
        index=0
    )
    
    # Filter data based on selected segment
    if selected_segment != 'All Segments':
        df_filtered = customer_df[customer_df['Segment'] == selected_segment]
    else:
        df_filtered = customer_df.copy() # Use a copy to avoid SettingWithCopyWarning

    # Check if filtered data is empty
    if df_filtered.empty:
        st.warning(f"No customers found for the '{selected_segment}' segment.")
        st.header("Overall Customer Metrics")
        st.metric(label="Total Customers", value="0")
        st.metric(label="Average Recency (Days)", value="N/A")
        st.metric(label="Average Frequency", value="N/A")
        st.metric(label="Average Monetary ($)", value="$0.00")
        st.subheader("Charts")
        st.info("Please adjust filters to see data.")
    else:
        # --- Overall Customer Metrics ---
        st.header("Overall Customer Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_customers = df_filtered['Customer ID'].nunique()
            st.metric(label="Total Customers", value=f"{total_customers:,}")
        
        with col2:
            avg_recency = int(df_filtered['Recency'].mean())
            st.metric(label="Average Recency (Days)", value=f"{avg_recency} days")
        
        with col3:
            avg_frequency = round(df_filtered['Frequency'].mean(), 2)
            st.metric(label="Average Frequency", value=f"{avg_frequency}")
        
        with col4:
            avg_monetary = df_filtered['Monetary'].mean()
            st.metric(label="Average Monetary ($)", value=f"${avg_monetary:,.2f}")

        # --- Customer Segmentation Breakdown ---
        st.header("Customer Segmentation Breakdown")
        
        segment_counts = df_filtered['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Number of Customers']
        
        fig_segments = px.bar(
            segment_counts,
            x='Number of Customers',
            y='Segment',
            orientation='h',
            title='Number of Customers by Segment',
            labels={'Number of Customers':'Customers', 'Segment':'Customer Segment'},
            height=400,
            color='Number of Customers',
            color_continuous_scale=px.colors.sequential.Cividis
        )
        fig_segments.update_layout(yaxis_title='', xaxis_title='Number of Customers')
        fig_segments.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig_segments, use_container_width=True)

        # --- RFM Distribution Charts ---
        st.header("RFM Score Distribution")
        
        chart_col1, chart_col2, chart_col3 = st.columns(3)

        with chart_col1:
            st.subheader("Recency Score Distribution")
            fig_r = px.histogram(df_filtered, x='R_Score', title='Recency Scores', nbins=5, color_discrete_sequence=px.colors.qualitative.Plotly)
            fig_r.update_layout(xaxis_title="Recency Score (5=Most Recent)", yaxis_title="Number of Customers")
            fig_r.update_xaxes(tickvals=[1, 2, 3, 4, 5], ticktext=['1 (Least Recent)', '2', '3', '4', '5 (Most Recent)'])
            st.plotly_chart(fig_r, use_container_width=True)

        with chart_col2:
            st.subheader("Frequency Score Distribution")
            fig_f = px.histogram(df_filtered, x='F_Score', title='Frequency Scores', nbins=5, color_discrete_sequence=px.colors.qualitative.Plotly)
            fig_f.update_layout(xaxis_title="Frequency Score (5=Most Frequent)", yaxis_title="Number of Customers")
            fig_f.update_xaxes(tickvals=[1, 2, 3, 4, 5], ticktext=['1 (Least Frequent)', '2', '3', '4', '5 (Most Frequent)'])
            st.plotly_chart(fig_f, use_container_width=True)

        with chart_col3:
            st.subheader("Monetary Score Distribution")
            fig_m = px.histogram(df_filtered, x='M_Score', title='Monetary Scores', nbins=5, color_discrete_sequence=px.colors.qualitative.Plotly)
            fig_m.update_layout(xaxis_title="Monetary Score (5=Highest Spending)", yaxis_title="Number of Customers")
            fig_m.update_xaxes(tickvals=[1, 2, 3, 4, 5], ticktext=['1 (Lowest Spending)', '2', '3', '4', '5 (Highest Spending)'])
            st.plotly_chart(fig_m, use_container_width=True)

        # Optional: RFM scatter plot
        st.subheader("RFM Segments (Recency vs. Monetary)")
        fig_rfm_scatter = px.scatter(
            df_filtered, 
            x='Recency', 
            y='Monetary', 
            color='Segment', 
            size='Frequency', # Frequency ko dot size se dikhayen
            hover_name='Customer ID', 
            title='Customer Segmentation by RFM',
            log_y=True, # Monetary scale ko logarithmic kar sakte hain agar values bohot vary karti hain
            height=500
        )
        st.plotly_chart(fig_rfm_scatter, use_container_width=True)

        # Optional: Raw customer RFM data preview
        st.subheader("Filtered Customer Data Preview")
        st.dataframe(df_filtered.head(10))
