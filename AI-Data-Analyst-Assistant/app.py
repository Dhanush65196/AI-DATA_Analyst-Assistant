"""
AI Data Analyst Assistant - Main Streamlit Application

A production-grade data analysis tool that:
- Accepts CSV file uploads
- Validates and displays data
- Provides statistical insights
- Follows clean coding best practices

Author: Data Analyst Team
Version: 1.0.0
"""

import logging
import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)

MAX_UPLOAD_SIZE_MB = 50
_ALLOWED_CSV_CONTENT_TYPES = {"text/csv", "application/vnd.ms-excel"}


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
# This section configures the Streamlit page settings for optimal UX
def configure_page() -> None:
    """
    Configure Streamlit page settings.
    
    Sets:
    - Page title and icon
    - Layout configuration
    - Initial sidebar state
    """
    st.set_page_config(
        page_title="AI Data Analyst Assistant",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ============================================================================
# CUSTOM STYLING
# ============================================================================
# Enhance the visual appearance with custom CSS
def apply_custom_styling() -> None:
    """Apply custom CSS styling for better UI/UX."""
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            color: #1f77b4;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .success-box {
            padding: 1rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 0.5rem;
            color: #155724;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================================
# DATA VALIDATION & PROCESSING
# ============================================================================
def validate_csv_file(uploaded_file: io.BytesIO) -> Tuple[bool, str]:
    """
    Validate the uploaded CSV file.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        Tuple of (is_valid: bool, message: str)
        
    Raises:
        None (returns error message instead)
    """
    # Check if file exists
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file extension
    if not uploaded_file.name.endswith('.csv'):
        return False, "⚠️ Please upload a CSV file"
    
    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_UPLOAD_SIZE_MB:
        return False, f"⚠️ File size ({file_size_mb:.2f}MB) exceeds {MAX_UPLOAD_SIZE_MB}MB limit"

    # Validate content type when available
    if hasattr(uploaded_file, 'type') and uploaded_file.type:
        if uploaded_file.type not in _ALLOWED_CSV_CONTENT_TYPES:
            return False, "⚠️ File content type is not CSV"

    return True, "✅ File validation passed"


def load_csv_file(uploaded_file: io.BytesIO) -> Optional[pd.DataFrame]:
    """
    Load and parse the CSV file into a pandas DataFrame.
    
    Args:
        uploaded_file: The uploaded file object
        
    Returns:
        DataFrame if successful, None otherwise
    """
    try:
        # Read CSV file with error handling
        df = pd.read_csv(uploaded_file)
        return df
    except pd.errors.ParserError:
        st.error("❌ Error parsing CSV file. Please check the file format.")
        return None
    except Exception:
        logger.exception("Unexpected error loading CSV")
        st.error("❌ An unexpected error occurred while loading the file.")
        return None


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate comprehensive data summary statistics.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary containing:
        - Shape (rows, columns)
        - Column info
        - Data types
        - Missing values count
        - Memory usage
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 ** 2)
    }


# ============================================================================
# UI COMPONENTS
# ============================================================================
def display_header() -> None:
    """Display the main header and description."""
    st.title("📊 AI Data Analyst Assistant")
    st.markdown(
        """
        Welcome! This tool helps you analyze CSV data files with ease.
        
        **Features:**
        - 📁 Upload CSV files
        - 📈 View data preview
        - 📊 Statistical analysis
        - 💡 Data insights
        """
    )
    st.divider()


def display_file_uploader() -> Optional[io.BytesIO]:
    """
    Display file upload widget.
    
    Returns:
        Uploaded file object or None
    """
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file (max 50MB)"
    )
    return uploaded_file


def display_success_message(filename: str) -> None:
    """
    Display success message with file details.
    
    Args:
        filename: Name of the uploaded file
    """
    st.success(f"✅ Successfully loaded: **{filename}**")
    st.markdown("---")


def display_data_preview(df: pd.DataFrame, num_rows: int = 5) -> None:
    """
    Display first N rows of the dataset.
    
    Args:
        df: Input DataFrame
        num_rows: Number of rows to display (default: 5)
    """
    st.subheader(f"📋 First {num_rows} Rows")
    
    # Display as an interactive table
    st.dataframe(
        df.head(num_rows),
        use_container_width=True,
        height=300
    )


def display_data_statistics(df: pd.DataFrame) -> None:
    """
    Display comprehensive data statistics.
    
    Args:
        df: Input DataFrame
    """
    summary = get_data_summary(df)
    
    # Create columns for better layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Rows",
            value=f"{summary['rows']:,}"
        )
    
    with col2:
        st.metric(
            label="📋 Total Columns",
            value=summary['columns']
        )
    
    with col3:
        st.metric(
            label="💾 Memory Usage",
            value=f"{summary['memory_usage_mb']:.2f} MB"
        )
    
    with col4:
        # Count missing values
        total_missing = sum(summary['missing_values'].values())
        st.metric(
            label="⚠️ Missing Values",
            value=total_missing
        )


def display_data_info(df: pd.DataFrame) -> None:
    """
    Display detailed data information.
    
    Args:
        df: Input DataFrame
    """
    st.subheader("📊 Data Information")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Column Types", "Missing Values", "Statistics"])
    
    with tab1:
        # Display column data types
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values
        })
        st.dataframe(dtype_df, use_container_width=True)
    
    with tab2:
        # Display missing value counts
        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing %": (df.isnull().sum().values / len(df) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True)
    
    with tab3:
        # Display statistical summary
        st.dataframe(
            df.describe().T,
            use_container_width=True
        )


# ============================================================================
# VISUALIZATION COMPONENTS
# ============================================================================
def detect_sales_columns(df: pd.DataFrame) -> List[str]:
    """
    Detect columns that appear to be sales-related.
    
    Args:
        df: Input DataFrame
        
    Returns:
        List of column names that look like sales columns
    """
    sales_keywords = [
        'sales', 'revenue', 'amount', 'total', 'price',
        'quantity', 'units', 'qty', 'cost', 'profit',
        'income', 'earnings', 'value'
    ]
    
    detected_columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in sales_keywords):
            # Check if column contains numeric data
            if pd.api.types.is_numeric_dtype(df[col]):
                detected_columns.append(col)
    
    return detected_columns


def detect_category_columns(df: pd.DataFrame) -> List[str]:
    """
    Detect columns that can be used as categories for pie charts.
    
    Args:
        df: Input DataFrame
        
    Returns:
        List of categorical column names
    """
    category_keywords = [
        'category', 'type', 'status', 'region', 'state',
        'country', 'city', 'product', 'department', 'name',
        'brand', 'segment'
    ]
    
    detected_columns = []
    for col in df.columns:
        col_lower = col.lower()
        # Check if it's categorical
        if df[col].dtype == 'object' or df[col].nunique() < 50:
            if any(keyword in col_lower for keyword in category_keywords):
                detected_columns.append(col)
    
    return detected_columns


def create_pie_chart_by_category(df: pd.DataFrame, values_col: str, category_col: str) -> None:
    """
    Create and display an interactive pie chart.
    
    Args:
        df: Input DataFrame
        values_col: Column with values for pie chart
        category_col: Column with categories
    """
    try:
        # Group by category and sum values
        grouped_data = df.groupby(category_col)[values_col].sum().reset_index()
        grouped_data = grouped_data.sort_values(values_col, ascending=False)
        
        # Create interactive pie chart using Plotly
        fig = px.pie(
            grouped_data,
            values=values_col,
            names=category_col,
            title=f"📊 {values_col} by {category_col}",
            hole=0,  # Set to 0 for full pie, 0.3 for donut
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value:.2f}<br>%{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            height=600,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        logger.exception("Error creating pie chart")
        st.error("❌ Error creating pie chart. Please check your data.")


def create_sales_summary_dashboard(df: pd.DataFrame, sales_cols: List[str]) -> None:
    """
    Create a summary dashboard for sales data.
    
    Args:
        df: Input DataFrame
        sales_cols: List of sales column names
    """
    st.subheader("💰 Sales Summary Dashboard")
    
    # Create columns for metrics
    cols = st.columns(len(sales_cols))
    
    for idx, col in enumerate(sales_cols):
        with cols[idx]:
            total = df[col].sum()
            avg = df[col].mean()
            max_val = df[col].max()
            
            st.metric(
                label=f"Total {col}",
                value=f"${total:,.2f}" if isinstance(total, (int, float)) else f"{total:,.0f}"
            )
            
            with st.expander(f"📈 {col} Details"):
                st.write(f"**Average:** ${avg:,.2f}" if isinstance(avg, (int, float)) else f"**Average:** {avg:,.0f}")
                st.write(f"**Maximum:** ${max_val:,.2f}" if isinstance(max_val, (int, float)) else f"**Maximum:** {max_val:,.0f}")
                st.write(f"**Minimum:** ${df[col].min():,.2f}" if isinstance(df[col].min(), (int, float)) else f"**Minimum:** {df[col].min():,.0f}")


def display_pie_charts_section(df: pd.DataFrame) -> None:
    """
    Display pie chart visualizations section.
    
    Args:
        df: Input DataFrame
    """
    st.divider()
    st.subheader("📈 Sales Pie Charts Analysis")
    
    # Detect sales and category columns
    sales_columns = detect_sales_columns(df)
    category_columns = detect_category_columns(df)
    
    if not sales_columns:
        st.info("ℹ️ No sales-related columns detected. Add columns with names like 'Sales', 'Revenue', 'Amount', etc.")
        return
    
    if not category_columns:
        st.info("ℹ️ No category columns detected for grouping. Add columns with names like 'Category', 'Product', 'Region', etc.")
        return
    
    # Show sales summary
    create_sales_summary_dashboard(df, sales_columns)
    
    st.divider()
    st.write("### 🔍 Detailed Pie Charts")
    
    # Create tabs for each sales column
    if len(sales_columns) > 1:
        tabs = st.tabs([f"📊 {col}" for col in sales_columns])
        
        for tab_idx, (tab, sales_col) in enumerate(zip(tabs, sales_columns)):
            with tab:
                # Let user select category column
                selected_category = st.selectbox(
                    f"Select category for {sales_col}",
                    category_columns,
                    key=f"category_{sales_col}"
                )
                
                # Create pie chart
                create_pie_chart_by_category(df, sales_col, selected_category)
                
                # Show data table
                with st.expander(f"📋 View {sales_col} data"):
                    grouped = df.groupby(selected_category)[sales_col].agg(['sum', 'count', 'mean']).reset_index()
                    grouped.columns = [selected_category, 'Total', 'Count', 'Average']
                    st.dataframe(grouped, use_container_width=True)
    else:
        # Single sales column
        sales_col = sales_columns[0]
        
        # Let user select category column
        selected_category = st.selectbox(
            f"Select category for {sales_col}",
            category_columns,
            key=f"category_{sales_col}"
        )
        
        # Create pie chart
        create_pie_chart_by_category(df, sales_col, selected_category)
        
        # Show data table
        with st.expander(f"📋 View {sales_col} data"):
            grouped = df.groupby(selected_category)[sales_col].agg(['sum', 'count', 'mean']).reset_index()
            grouped.columns = [selected_category, 'Total', 'Count', 'Average']
            st.dataframe(grouped, use_container_width=True)


def display_numerical_distributions(df: pd.DataFrame) -> None:
    """
    Display distribution charts for numerical columns.
    
    Args:
        df: Input DataFrame
    """
    st.divider()
    st.subheader("📊 Numerical Data Distributions")
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.info("ℹ️ No numerical columns found.")
        return
    
    # Let user select column for histogram
    selected_col = st.selectbox(
        "Select a column for distribution analysis",
        numeric_cols,
        key="distribution_col"
    )
    
    # Create histogram
    fig = px.histogram(
        df,
        x=selected_col,
        nbins=30,
        title=f"Distribution of {selected_col}",
        color_discrete_sequence=["#636EFA"]
    )
    
    fig.update_layout(
        xaxis_title=selected_col,
        yaxis_title="Frequency",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================
def main() -> None:
    """
    Main application entry point.
    
    Flow:
    1. Configure page settings
    2. Apply styling
    3. Display header
    4. Handle file upload
    5. Validate file
    6. Load and display data
    7. Show statistics
    8. Display visualizations (pie charts)
    """
    # Initialize page
    configure_page()
    apply_custom_styling()
    
    # Display header
    display_header()
    
    # File upload
    uploaded_file = display_file_uploader()
    
    # Process uploaded file
    if uploaded_file is not None:
        # Step 1: Validate file
        is_valid, validation_message = validate_csv_file(uploaded_file)
        
        if is_valid:
            # Step 2: Load CSV file
            df = load_csv_file(uploaded_file)
            
            if df is not None:
                # Step 3: Display success message
                display_success_message(uploaded_file.name)
                
                # Step 4: Display preview (first 5 rows)
                display_data_preview(df, num_rows=5)
                
                # Step 5: Display statistics
                display_data_statistics(df)
                
                # Step 6: Display detailed information
                st.divider()
                display_data_info(df)
                
                # Step 7: Display pie charts and visualizations
                display_pie_charts_section(df)
                
                # Step 8: Display distribution charts
                display_numerical_distributions(df)
                
                # Step 9: Download processed data option
                st.divider()
                st.subheader("💾 Export Options")
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name="analyzed_data.csv",
                    mime="text/csv"
                )
        else:
            # Display validation error
            st.error(validation_message)
    else:
        # Display initial instruction
        st.info("👆 Upload a CSV file to get started!")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()
