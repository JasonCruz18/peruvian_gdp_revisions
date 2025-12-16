"""Streamlit Dashboard for Peru GDP Real-Time Dataset.

This interactive dashboard provides visualization and exploration tools for
the Peru GDP RTD constructed by the pipeline.

Run with: streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Peru GDP Real-Time Dataset Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Helper functions
@st.cache_data
def load_rtd_data():
    """Load RTD datasets from data/output/ directory."""
    data_dir = Path(__file__).parent.parent / "data" / "output"

    datasets = {}

    # Load available datasets
    dataset_files = {
        "Monthly RTD": "monthly_gdp_rtd.csv",
        "Quarterly RTD": "quarterly_annual_gdp_rtd.csv",
        "Monthly Releases": "monthly_gdp_releases.csv",
        "Quarterly Releases": "quarterly_annual_gdp_releases.csv",
        "Monthly Benchmark": "monthly_gdp_benchmark.csv",
        "Quarterly Benchmark": "quarterly_annual_gdp_benchmark.csv",
    }

    for name, filename in dataset_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            datasets[name] = pd.read_csv(filepath, index_col=0)

    return datasets


def calculate_revision_stats(releases_df):
    """Calculate revision statistics from releases dataset."""
    if 'first_release' not in releases_df.columns or 'second_release' not in releases_df.columns:
        return None

    revisions = releases_df['second_release'] - releases_df['first_release']

    stats = {
        'mean': revisions.mean(),
        'std': revisions.std(),
        'min': revisions.min(),
        'max': revisions.max(),
        'median': revisions.median(),
        'count': revisions.count(),
    }

    return stats, revisions


# Main app
def main():
    # Header
    st.markdown('<p class="main-header">📊 Peru GDP Real-Time Dataset Explorer</p>', unsafe_allow_html=True)
    st.markdown("Interactive visualization and analysis of Peruvian GDP revisions")

    # Sidebar
    with st.sidebar:
        st.header("📁 Dataset Selection")

        # Load data
        with st.spinner("Loading datasets..."):
            datasets = load_rtd_data()

        if not datasets:
            st.error("No datasets found. Please run the pipeline first: `python scripts/update_rtd.py`")
            st.stop()

        st.success(f"✓ Loaded {len(datasets)} datasets")

        # Dataset selector
        selected_dataset_name = st.selectbox(
            "Select Dataset",
            options=list(datasets.keys()),
            index=0,
        )

        selected_df = datasets[selected_dataset_name]

        st.markdown("---")
        st.header("ℹ️ Dataset Info")
        st.metric("Shape", f"{selected_df.shape[0]} × {selected_df.shape[1]}")
        st.metric("Columns", selected_df.shape[1])
        st.metric("Rows", selected_df.shape[0])

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Visualization",
        "🔍 Revision Analysis",
        "📋 Data Explorer",
        "📖 Documentation"
    ])

    # Tab 1: Overview
    with tab1:
        st.header(f"Dataset Overview: {selected_dataset_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Observations", selected_df.shape[0] * selected_df.shape[1])
        with col2:
            st.metric("Vintages/Periods", selected_df.shape[0])
        with col3:
            non_null = selected_df.notna().sum().sum()
            st.metric("Non-null Values", non_null)

        st.subheader("Data Preview")
        st.dataframe(selected_df.head(20), use_container_width=True)

        st.subheader("Summary Statistics")
        st.dataframe(selected_df.describe(), use_container_width=True)

    # Tab 2: Visualization
    with tab2:
        st.header("Data Visualization")

        viz_type = st.radio(
            "Select Visualization Type",
            ["Heatmap", "Time Series", "Distribution"],
            horizontal=True,
        )

        if viz_type == "Heatmap":
            st.subheader("RTD Heatmap")

            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=selected_df.values,
                x=selected_df.columns,
                y=selected_df.index,
                colorscale='RdBu_r',
                zmid=0,
            ))

            fig.update_layout(
                title=f"{selected_dataset_name} Heatmap",
                xaxis_title="Target Period",
                yaxis_title="Vintage",
                height=600,
            )

            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Time Series":
            st.subheader("Time Series Plot")

            # Select columns to plot
            cols_to_plot = st.multiselect(
                "Select periods to plot",
                options=selected_df.columns.tolist(),
                default=selected_df.columns[:5].tolist() if len(selected_df.columns) >= 5 else selected_df.columns.tolist(),
            )

            if cols_to_plot:
                fig = go.Figure()

                for col in cols_to_plot:
                    fig.add_trace(go.Scatter(
                        x=selected_df.index,
                        y=selected_df[col],
                        mode='lines+markers',
                        name=col,
                    ))

                fig.update_layout(
                    title=f"{selected_dataset_name} - Time Series",
                    xaxis_title="Vintage",
                    yaxis_title="GDP Growth Rate (%)",
                    height=500,
                    hovermode='x unified',
                )

                st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Distribution":
            st.subheader("Distribution Plot")

            # Flatten all values
            all_values = selected_df.values.flatten()
            all_values = all_values[~pd.isna(all_values)]

            fig = px.histogram(
                x=all_values,
                nbins=50,
                title=f"{selected_dataset_name} - Value Distribution",
                labels={'x': 'GDP Growth Rate (%)', 'y': 'Frequency'},
            )

            fig.add_vline(
                x=all_values.mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mean: {all_values.mean():.2f}",
            )

            st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Revision Analysis
    with tab3:
        st.header("Revision Analysis")

        if "Releases" in selected_dataset_name:
            # Calculate revision statistics
            stats, revisions = calculate_revision_stats(selected_df)

            if stats:
                st.subheader("Revision Statistics")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean Revision", f"{stats['mean']:.3f} pp")
                    st.metric("Std Deviation", f"{stats['std']:.3f} pp")
                with col2:
                    st.metric("Minimum", f"{stats['min']:.3f} pp")
                    st.metric("Maximum", f"{stats['max']:.3f} pp")
                with col3:
                    st.metric("Median", f"{stats['median']:.3f} pp")
                    st.metric("Count", stats['count'])

                # Revision distribution
                st.subheader("Revision Distribution")

                fig = px.histogram(
                    x=revisions,
                    nbins=30,
                    title="Distribution of Revisions (2nd - 1st Release)",
                    labels={'x': 'Revision (percentage points)', 'y': 'Frequency'},
                )

                fig.add_vline(x=0, line_dash="dash", line_color="black")
                fig.add_vline(
                    x=stats['mean'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Mean: {stats['mean']:.3f}",
                )

                st.plotly_chart(fig, use_container_width=True)

                # Revision over time
                st.subheader("Revision Magnitude Over Time")

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=selected_df.index,
                    y=revisions,
                    mode='lines+markers',
                    name='Revision',
                ))

                fig.add_hline(y=0, line_dash="dash", line_color="black")
                fig.update_layout(
                    title="Revision Magnitude Over Time",
                    xaxis_title="Target Period",
                    yaxis_title="Revision (pp)",
                    height=400,
                )

                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Revision analysis is only available for 'Releases' format datasets. Please select a releases dataset from the sidebar.")

    # Tab 4: Data Explorer
    with tab4:
        st.header("Data Explorer")

        st.subheader("Full Dataset")
        st.dataframe(selected_df, use_container_width=True, height=600)

        # Download button
        csv = selected_df.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{selected_dataset_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )

    # Tab 5: Documentation
    with tab5:
        st.header("Documentation")

        st.markdown("""
        ## About This Dashboard

        This interactive dashboard provides visualization and exploration tools for the Peru GDP Real-Time Dataset (RTD).

        ### Dataset Types

        1. **RTD (Real-Time Dataset)**: Vintage format showing how data evolved over time
        2. **Releases Dataset**: Release format showing 1st, 2nd, 3rd... releases for each period
        3. **Benchmark Dataset**: Vintages immediately before base-year changes
        4. **Base-Year Adjusted**: Removes revisions caused by base-year updates

        ### Features

        - **Overview**: Dataset summary statistics and preview
        - **Visualization**: Interactive charts (heatmap, time series, distribution)
        - **Revision Analysis**: Statistical analysis of GDP revisions
        - **Data Explorer**: Full dataset view and download

        ### Usage Tips

        - Use the sidebar to switch between datasets
        - Hover over charts for detailed information
        - Download data for external analysis

        ### Resources

        - [Main README](../README.md)
        - [Usage Guide](../docs/USAGE.md)
        - [Architecture](../docs/ARCHITECTURE.md)
        - [GitHub Repository](https://github.com/JasonCruz18/peru_gdp_revisions)

        ### Run the Pipeline

        ```bash
        # Update the RTD
        python scripts/update_rtd.py

        # Run this dashboard
        streamlit run dashboard/app.py
        ```
        """)

    # Footer
    st.markdown("---")
    st.markdown("**Peru GDP Real-Time Dataset** | Built with Streamlit | [Documentation](../README.md)")


if __name__ == "__main__":
    main()
