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
from typing import Optional, Tuple
import io


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
    
    # Check file size (max 50MB)
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 50:
        return False, f"⚠️ File size ({file_size_mb:.2f}MB) exceeds 50MB limit"
    
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
    except pd.errors.ParserError as e:
        st.error(f"❌ Error parsing CSV file: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
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
                
                # Step 7: Download processed data option
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
