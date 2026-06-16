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

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Optional, Tuple, List
import io

from utils.data_profiler import (
    get_data_profile,
    get_missing_values_report,
    get_numeric_columns,
)
from utils.column_detector import detect_sales_columns, detect_category_columns


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
        page_icon="\U0001f4ca",
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
        return False, "\u26a0\ufe0f Please upload a CSV file"
    
    # Check file size (max 50MB)
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 50:
        return False, f"\u26a0\ufe0f File size ({file_size_mb:.2f}MB) exceeds 50MB limit"
    
    return True, "\u2705 File validation passed"


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
    except pd.errors.ParserError as e:
        st.error(f"\u274c Error parsing CSV file: {str(e)}")
        return None
    except Exception as e:
        st.error(f"\u274c Unexpected error: {str(e)}")
        return None


# ============================================================================
# UI COMPONENTS
# ============================================================================
def display_header() -> None:
    """Display the main header and description."""
    st.title("\U0001f4ca AI Data Analyst Assistant")
    st.markdown(
        """
        Welcome! This tool helps you analyze CSV data files with ease.
        
        **Features:**
        - \U0001f4c1 Upload CSV files
        - \U0001f4c8 View data preview
        - \U0001f4ca Statistical analysis
        - \U0001f4a1 Data insights
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
    st.success(f"\u2705 Successfully loaded: **{filename}**")
    st.markdown("---")


def display_data_preview(df: pd.DataFrame, num_rows: int = 5) -> None:
    """
    Display first N rows of the dataset.
    
    Args:
        df: Input DataFrame
        num_rows: Number of rows to display (default: 5)
    """
    st.subheader(f"\U0001f4cb First {num_rows} Rows")
    
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
    profile = get_data_profile(df)
    
    # Create columns for better layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="\U0001f4ca Total Rows",
            value=f"{profile['rows']:,}"
        )
    
    with col2:
        st.metric(
            label="\U0001f4cb Total Columns",
            value=profile['columns']
        )
    
    with col3:
        st.metric(
            label="\U0001f4be Memory Usage",
            value=f"{profile['memory_usage_mb']:.2f} MB"
        )
    
    with col4:
        # Count missing values
        total_missing = sum(profile['missing_values'].values())
        st.metric(
            label="\u26a0\ufe0f Missing Values",
            value=total_missing
        )


def display_data_info(df: pd.DataFrame) -> None:
    """
    Display detailed data information.
    
    Args:
        df: Input DataFrame
    """
    st.subheader("\U0001f4ca Data Information")
    
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
        missing_df = get_missing_values_report(df)
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
            title=f"\U0001f4ca {values_col} by {category_col}",
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
        st.error(f"\u274c Error creating pie chart: {str(e)}")


def create_sales_summary_dashboard(df: pd.DataFrame, sales_cols: List[str]) -> None:
    """
    Create a summary dashboard for sales data.
    
    Args:
        df: Input DataFrame
        sales_cols: List of sales column names
    """
    st.subheader("\U0001f4b0 Sales Summary Dashboard")
    
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
            
            with st.expander(f"\U0001f4c8 {col} Details"):
                st.write(f"**Average:** ${avg:,.2f}" if isinstance(avg, (int, float)) else f"**Average:** {avg:,.0f}")
                st.write(f"**Maximum:** ${max_val:,.2f}" if isinstance(max_val, (int, float)) else f"**Maximum:** {max_val:,.0f}")
                st.write(f"**Minimum:** ${df[col].min():,.2f}" if isinstance(df[col].min(), (int, float)) else f"**Minimum:** {df[col].min():,.0f}")


def _display_sales_pie_chart(
    df: pd.DataFrame,
    sales_col: str,
    category_columns: List[str],
) -> None:
    """
    Render a category selector, pie chart, and grouped-data expander for
    a single *sales_col*.  Extracted to eliminate the code that was
    duplicated across the single- and multi-column branches of
    ``display_pie_charts_section``.
    """
    selected_category = st.selectbox(
        f"Select category for {sales_col}",
        category_columns,
        key=f"category_{sales_col}",
    )

    create_pie_chart_by_category(df, sales_col, selected_category)

    with st.expander(f"\U0001f4cb View {sales_col} data"):
        grouped = (
            df.groupby(selected_category)[sales_col]
            .agg(["sum", "count", "mean"])
            .reset_index()
        )
        grouped.columns = [selected_category, "Total", "Count", "Average"]
        st.dataframe(grouped, use_container_width=True)


def display_pie_charts_section(df: pd.DataFrame) -> None:
    """
    Display pie chart visualizations section.
    
    Args:
        df: Input DataFrame
    """
    st.divider()
    st.subheader("\U0001f4c8 Sales Pie Charts Analysis")
    
    # Detect sales and category columns
    sales_columns = detect_sales_columns(df)
    category_columns = detect_category_columns(df)
    
    if not sales_columns:
        st.info("\u2139\ufe0f No sales-related columns detected. Add columns with names like 'Sales', 'Revenue', 'Amount', etc.")
        return
    
    if not category_columns:
        st.info("\u2139\ufe0f No category columns detected for grouping. Add columns with names like 'Category', 'Product', 'Region', etc.")
        return
    
    # Show sales summary
    create_sales_summary_dashboard(df, sales_columns)
    
    st.divider()
    st.write("### \U0001f50d Detailed Pie Charts")
    
    if len(sales_columns) > 1:
        tabs = st.tabs([f"\U0001f4ca {col}" for col in sales_columns])
        for tab, sales_col in zip(tabs, sales_columns):
            with tab:
                _display_sales_pie_chart(df, sales_col, category_columns)
    else:
        _display_sales_pie_chart(df, sales_columns[0], category_columns)


def display_numerical_distributions(df: pd.DataFrame) -> None:
    """
    Display distribution charts for numerical columns.
    
    Args:
        df: Input DataFrame
    """
    st.divider()
    st.subheader("\U0001f4ca Numerical Data Distributions")
    
    # Get numeric columns
    numeric_cols = get_numeric_columns(df)
    
    if not numeric_cols:
        st.info("\u2139\ufe0f No numerical columns found.")
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
                st.subheader("\U0001f4be Export Options")
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
        st.info("\U0001f446 Upload a CSV file to get started!")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    main()
