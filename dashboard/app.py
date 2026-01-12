"""Streamlit Dashboard for Peru GDP Real-Time Dataset.

Fully customizable interactive dashboard with theme support, logo, and advanced visualizations.

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
import base64

# Import dashboard configuration
try:
    from dashboard import config as cfg
except ImportError:
    import config as cfg

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=cfg.PROJECT_NAME,
    page_icon="📊",
    layout=cfg.PAGE_LAYOUT,
    initial_sidebar_state=cfg.SIDEBAR_STATE,
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_rtd_data():
    """Load RTD datasets from data/output/ directory."""
    data_dir = Path(__file__).parent.parent / "data" / "output"

    datasets = {}

    dataset_files = {
        "Monthly RTD": "vintages/monthly_gdp_vintages.csv",
        "Quarterly RTD": "vintages/quarterly_gdp_vintages.csv",
        "Monthly Releases": "releases/monthly_gdp_releases.csv",
        "Quarterly Releases": "releases/quarterly_gdp_releases.csv",
        "Monthly Benchmark": "vintages/monthly_gdp_vintages_benchmark.csv",
        "Quarterly Benchmark": "vintages/quarterly_gdp_vintages_benchmark.csv",
        "BY-Adjusted Monthly": "vintages/monthly_gdp_vintages_adjusted.csv",
        "BY-Adjusted Quarterly": "vintages/quarterly_gdp_vintages_adjusted.csv",
    }

    for name, filename in dataset_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            try:
                datasets[name] = pd.read_csv(filepath, index_col=0)
            except Exception as e:
                st.warning(f"Error loading {name}: {e}")

    return datasets


def get_base64_image(image_path):
    """Convert image to base64 for embedding."""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


def calculate_revision_stats(releases_df):
    """Calculate revision statistics from releases dataset."""
    if 'first_release' not in releases_df.columns or 'second_release' not in releases_df.columns:
        return None, None

    revisions = releases_df['second_release'] - releases_df['first_release']

    stats = {
        'mean': revisions.mean(),
        'std': revisions.std(),
        'min': revisions.min(),
        'max': revisions.max(),
        'median': revisions.median(),
        'count': revisions.count(),
        'mae': revisions.abs().mean(),  # Mean Absolute Error
    }

    return stats, revisions


def create_custom_metric(label, value, delta=None, prefix="", suffix=""):
    """Create a custom styled metric card."""
    delta_html = ""
    if delta is not None:
        delta_color = cfg.COLORS['success'] if delta >= 0 else cfg.COLORS['error']
        delta_symbol = "▲" if delta >= 0 else "▼"
        delta_html = f"""
        <div style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.25rem;">
            {delta_symbol} {abs(delta):.2f}
        </div>
        """

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# APPLY THEME AND CUSTOM CSS
# ============================================================================

st.markdown(cfg.get_theme_css(), unsafe_allow_html=True)

# ============================================================================
# HEADER WITH LOGO
# ============================================================================

# Logo (if enabled and exists)
if cfg.USE_LOGO and cfg.LOGO_PATH.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(cfg.LOGO_PATH), width=cfg.LOGO_WIDTH)
elif cfg.USE_LOGO and not cfg.LOGO_PATH.exists():
    # Create placeholder for logo
    st.info(f"💡 **Tip**: Add your project logo at `{cfg.LOGO_PATH}` to customize the header!")

# Project title and subtitle
st.markdown(f'<p class="main-header">{cfg.PROJECT_NAME}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="main-subtitle">{cfg.PROJECT_SUBTITLE}</p>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown(f"### {cfg.SIDEBAR_TITLE}")

    # Load data
    with st.spinner("Loading datasets..."):
        datasets = load_rtd_data()

    if not datasets:
        st.error("❌ No datasets found!")
        st.info("**Please run the pipeline first:**")
        st.code("python scripts/update_rtd.py", language="bash")
        st.stop()

    st.success(f"✅ Loaded {len(datasets)} datasets")

    # Dataset selector
    st.markdown("---")
    selected_dataset_name = st.selectbox(
        "📊 Select Dataset",
        options=list(datasets.keys()),
        index=0,
    )

    selected_df = datasets[selected_dataset_name]

    # Dataset info (if enabled)
    if cfg.SHOW_DATASET_INFO:
        st.markdown("---")
        st.markdown("### 📋 Dataset Info")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", selected_df.shape[0])
        with col2:
            st.metric("Columns", selected_df.shape[1])

        # Missing data percentage
        missing_pct = (selected_df.isna().sum().sum() / (selected_df.shape[0] * selected_df.shape[1])) * 100
        st.metric("Missing", f"{missing_pct:.1f}%")

    # Theme selector
    if cfg.ENABLE_DARK_MODE_TOGGLE:
        st.markdown("---")
        st.markdown("### 🎨 Theme")
        theme_options = list(cfg.THEMES.keys())
        current_theme_idx = theme_options.index(cfg.THEME_PRESET) if cfg.THEME_PRESET in theme_options else 0

        new_theme = st.selectbox(
            "Color Scheme",
            options=theme_options,
            index=current_theme_idx,
            help="Change the dashboard color theme"
        )

        if new_theme != cfg.THEME_PRESET:
            st.info("💡 To permanently change the theme, edit `dashboard/config.py` and set `THEME_PRESET`")

    # Last updated (if enabled)
    if cfg.SHOW_LAST_UPDATED:
        st.markdown("---")
        st.caption(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# MAIN CONTENT TABS
# ============================================================================

# Build tab list based on enabled features
tab_list = []
tab_names = []

if cfg.ENABLE_OVERVIEW:
    tab_list.append(f"{cfg.TAB_ICONS['overview']} Overview")
    tab_names.append("overview")

if cfg.ENABLE_VISUALIZATION:
    tab_list.append(f"{cfg.TAB_ICONS['visualization']} Visualization")
    tab_names.append("visualization")

if cfg.ENABLE_REVISION_ANALYSIS:
    tab_list.append(f"{cfg.TAB_ICONS['revision']} Revision Analysis")
    tab_names.append("revision")

if cfg.ENABLE_DATA_EXPLORER:
    tab_list.append(f"{cfg.TAB_ICONS['explorer']} Data Explorer")
    tab_names.append("explorer")

if cfg.ENABLE_DOCUMENTATION:
    tab_list.append(f"{cfg.TAB_ICONS['docs']} Documentation")
    tab_names.append("docs")

if cfg.ENABLE_SETTINGS:
    tab_list.append(f"{cfg.TAB_ICONS['settings']} Settings")
    tab_names.append("settings")

tabs = st.tabs(tab_list)

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

if cfg.ENABLE_OVERVIEW:
    tab_idx = tab_names.index("overview")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Dataset Overview: {selected_dataset_name}</div>', unsafe_allow_html=True)

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            create_custom_metric(
                "Total Observations",
                cfg.format_number(selected_df.shape[0] * selected_df.shape[1], 0),
                prefix=""
            )

        with col2:
            create_custom_metric(
                "Vintages/Periods",
                str(selected_df.shape[0]),
                prefix=""
            )

        with col3:
            non_null = selected_df.notna().sum().sum()
            create_custom_metric(
                "Non-null Values",
                cfg.format_number(non_null, 0),
                prefix=""
            )

        with col4:
            coverage = (non_null / (selected_df.shape[0] * selected_df.shape[1])) * 100
            create_custom_metric(
                "Data Coverage",
                cfg.format_percentage(coverage),
                prefix=""
            )

        # Data preview
        st.markdown(f'<div class="section-header">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(
            selected_df.head(cfg.ROWS_PER_PAGE),
            use_container_width=True,
            height=400
        )

        # Summary statistics
        st.markdown(f'<div class="section-header">Summary Statistics</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Descriptive Statistics**")
            st.dataframe(selected_df.describe(), use_container_width=True)

        with col2:
            st.markdown("**Data Types**")
            dtypes_df = pd.DataFrame({
                'Column': selected_df.dtypes.index,
                'Type': selected_df.dtypes.values.astype(str)
            })
            st.dataframe(dtypes_df, use_container_width=True, height=300)

# ============================================================================
# TAB 2: VISUALIZATION
# ============================================================================

if cfg.ENABLE_VISUALIZATION:
    tab_idx = tab_names.index("visualization")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Data Visualization</div>', unsafe_allow_html=True)

        viz_type = st.radio(
            "Select Visualization Type",
            ["Heatmap", "Time Series", "Distribution", "Comparison"],
            horizontal=True,
        )

        if viz_type == "Heatmap":
            st.markdown("**Real-Time Dataset Heatmap**")
            st.caption("Visualize GDP growth rates across all vintages and periods")

            # Heatmap configuration
            col1, col2 = st.columns([3, 1])

            with col2:
                color_scale = st.selectbox(
                    "Color Scale",
                    ["RdBu_r", "RdYlGn", "Viridis", "Plasma", "Blues", "Reds"],
                    index=0
                )

            with col1:
                fig = go.Figure(data=go.Heatmap(
                    z=selected_df.values,
                    x=selected_df.columns,
                    y=selected_df.index,
                    colorscale=color_scale,
                    zmid=0,
                    hovertemplate='Vintage: %{y}<br>Period: %{x}<br>Value: %{z:.2f}%<extra></extra>',
                ))

                fig.update_layout(
                    title=f"{selected_dataset_name} - Heatmap View",
                    xaxis_title="Target Period",
                    yaxis_title="Vintage",
                    height=cfg.CHART_HEIGHT_LARGE,
                    template=cfg.CHART_TEMPLATE,
                    font=dict(family=cfg.FONT_FAMILY_BODY),
                )

                st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Time Series":
            st.markdown("**Time Series Analysis**")
            st.caption("Compare GDP growth rates across selected periods")

            # Column selection
            default_cols = selected_df.columns[:5].tolist() if len(selected_df.columns) >= 5 else selected_df.columns.tolist()
            cols_to_plot = st.multiselect(
                "Select periods to visualize",
                options=selected_df.columns.tolist(),
                default=default_cols,
            )

            if cols_to_plot:
                fig = go.Figure()

                for i, col in enumerate(cols_to_plot):
                    color = cfg.CHART_LINE_COLORS[i % len(cfg.CHART_LINE_COLORS)]
                    fig.add_trace(go.Scatter(
                        x=selected_df.index,
                        y=selected_df[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(color=color, width=2.5),
                        marker=dict(size=6),
                        hovertemplate='%{y:.2f}%<extra></extra>',
                    ))

                fig.update_layout(
                    title=f"{selected_dataset_name} - Time Series View",
                    xaxis_title="Vintage",
                    yaxis_title="GDP Growth Rate (%)",
                    height=cfg.CHART_HEIGHT_MEDIUM,
                    template=cfg.CHART_TEMPLATE,
                    hovermode='x unified',
                    font=dict(family=cfg.FONT_FAMILY_BODY),
                    showlegend=True,
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one period to visualize")

        elif viz_type == "Distribution":
            st.markdown("**Value Distribution Analysis**")
            st.caption("Examine the distribution of GDP growth rates")

            # Flatten all values
            all_values = selected_df.values.flatten()
            all_values = all_values[~pd.isna(all_values)]

            col1, col2 = st.columns([3, 1])

            with col2:
                bins = st.slider("Number of bins", 10, 100, 50)

            with col1:
                fig = px.histogram(
                    x=all_values,
                    nbins=bins,
                    title=f"{selected_dataset_name} - Distribution",
                    labels={'x': 'GDP Growth Rate (%)', 'y': 'Frequency'},
                    color_discrete_sequence=[cfg.COLORS['primary']],
                )

                # Add mean line
                mean_val = all_values.mean()
                fig.add_vline(
                    x=mean_val,
                    line_dash="dash",
                    line_color=cfg.COLORS['error'],
                    annotation_text=f"Mean: {mean_val:.2f}%",
                    annotation_position="top",
                )

                # Add median line
                median_val = pd.Series(all_values).median()
                fig.add_vline(
                    x=median_val,
                    line_dash="dot",
                    line_color=cfg.COLORS['success'],
                    annotation_text=f"Median: {median_val:.2f}%",
                    annotation_position="bottom",
                )

                fig.update_layout(
                    height=cfg.CHART_HEIGHT_MEDIUM,
                    template=cfg.CHART_TEMPLATE,
                    font=dict(family=cfg.FONT_FAMILY_BODY),
                )

                st.plotly_chart(fig, use_container_width=True)

                # Distribution statistics
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.metric("Mean", f"{mean_val:.2f}%")
                with col_b:
                    st.metric("Median", f"{median_val:.2f}%")
                with col_c:
                    st.metric("Std Dev", f"{all_values.std():.2f}%")
                with col_d:
                    st.metric("Range", f"{all_values.max() - all_values.min():.2f}%")

        elif viz_type == "Comparison":
            st.markdown("**Dataset Comparison**")
            st.caption("Compare two or more datasets side-by-side")

            if len(datasets) < 2:
                st.warning("Need at least 2 datasets for comparison")
            else:
                compare_datasets = st.multiselect(
                    "Select datasets to compare",
                    options=[name for name in datasets.keys() if name != selected_dataset_name],
                    default=[list(datasets.keys())[0]] if list(datasets.keys())[0] != selected_dataset_name else [list(datasets.keys())[1]]
                )

                if compare_datasets:
                    # Create comparison chart
                    fig = go.Figure()

                    # Add main dataset
                    fig.add_trace(go.Box(
                        y=selected_df.values.flatten(),
                        name=selected_dataset_name,
                        marker_color=cfg.COLORS['primary']
                    ))

                    # Add comparison datasets
                    for i, comp_name in enumerate(compare_datasets):
                        color = cfg.CHART_LINE_COLORS[(i+1) % len(cfg.CHART_LINE_COLORS)]
                        fig.add_trace(go.Box(
                            y=datasets[comp_name].values.flatten(),
                            name=comp_name,
                            marker_color=color
                        ))

                    fig.update_layout(
                        title="Dataset Comparison - Box Plots",
                        yaxis_title="GDP Growth Rate (%)",
                        height=cfg.CHART_HEIGHT_MEDIUM,
                        template=cfg.CHART_TEMPLATE,
                        font=dict(family=cfg.FONT_FAMILY_BODY),
                    )

                    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: REVISION ANALYSIS
# ============================================================================

if cfg.ENABLE_REVISION_ANALYSIS:
    tab_idx = tab_names.index("revision")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Revision Analysis</div>', unsafe_allow_html=True)

        if "Releases" in selected_dataset_name:
            stats, revisions = calculate_revision_stats(selected_df)

            if stats:
                # Revision statistics
                st.markdown("**Revision Statistics (2nd - 1st Release)**")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    create_custom_metric("Mean Revision", f"{stats['mean']:.3f} pp")
                with col2:
                    create_custom_metric("Std Deviation", f"{stats['std']:.3f} pp")
                with col3:
                    create_custom_metric("Mean Abs Error", f"{stats['mae']:.3f} pp")
                with col4:
                    create_custom_metric("Observations", str(stats['count']))

                col1, col2, col3 = st.columns(3)
                with col1:
                    create_custom_metric("Minimum", f"{stats['min']:.3f} pp")
                with col2:
                    create_custom_metric("Median", f"{stats['median']:.3f} pp")
                with col3:
                    create_custom_metric("Maximum", f"{stats['max']:.3f} pp")

                # Revision distribution
                st.markdown("**Revision Distribution**")

                fig = px.histogram(
                    x=revisions,
                    nbins=30,
                    title="Distribution of Revisions (2nd - 1st Release)",
                    labels={'x': 'Revision (percentage points)', 'y': 'Frequency'},
                    color_discrete_sequence=[cfg.COLORS['primary']],
                )

                fig.add_vline(x=0, line_dash="dash", line_color="black", line_width=2)
                fig.add_vline(
                    x=stats['mean'],
                    line_dash="dash",
                    line_color=cfg.COLORS['error'],
                    annotation_text=f"Mean: {stats['mean']:.3f}",
                )

                fig.update_layout(
                    height=cfg.CHART_HEIGHT_MEDIUM,
                    template=cfg.CHART_TEMPLATE,
                    font=dict(family=cfg.FONT_FAMILY_BODY),
                )

                st.plotly_chart(fig, use_container_width=True)

                # Revision over time
                st.markdown("**Revision Magnitude Over Time**")

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=selected_df.index,
                    y=revisions,
                    mode='lines+markers',
                    name='Revision',
                    line=dict(color=cfg.COLORS['primary'], width=2),
                    marker=dict(size=6),
                ))

                fig.add_hline(
                    y=0,
                    line_dash="dash",
                    line_color="black",
                    annotation_text="Zero revision"
                )

                fig.add_hline(
                    y=stats['mean'],
                    line_dash="dot",
                    line_color=cfg.COLORS['error'],
                    annotation_text=f"Mean: {stats['mean']:.3f}"
                )

                fig.update_layout(
                    title="Revision Magnitude by Target Period",
                    xaxis_title="Target Period",
                    yaxis_title="Revision (pp)",
                    height=cfg.CHART_HEIGHT_MEDIUM,
                    template=cfg.CHART_TEMPLATE,
                    font=dict(family=cfg.FONT_FAMILY_BODY),
                )

                st.plotly_chart(fig, use_container_width=True)

                # Revision diagnostics
                st.markdown("**Revision Diagnostics**")

                col1, col2 = st.columns(2)

                with col1:
                    # Upward vs downward revisions
                    upward = (revisions > 0).sum()
                    downward = (revisions < 0).sum()
                    zero = (revisions == 0).sum()

                    fig = go.Figure(data=[go.Pie(
                        labels=['Upward', 'Downward', 'Zero'],
                        values=[upward, downward, zero],
                        marker_colors=[cfg.COLORS['success'], cfg.COLORS['error'], cfg.COLORS['sidebar']],
                        hole=0.4,
                    )])

                    fig.update_layout(
                        title="Revision Direction",
                        height=cfg.CHART_HEIGHT_SMALL,
                        template=cfg.CHART_TEMPLATE,
                        font=dict(family=cfg.FONT_FAMILY_BODY),
                    )

                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Revision magnitude categories
                    small = (revisions.abs() < 0.5).sum()
                    medium = ((revisions.abs() >= 0.5) & (revisions.abs() < 1.0)).sum()
                    large = (revisions.abs() >= 1.0).sum()

                    fig = go.Figure(data=[go.Pie(
                        labels=['Small (<0.5pp)', 'Medium (0.5-1.0pp)', 'Large (>1.0pp)'],
                        values=[small, medium, large],
                        marker_colors=[cfg.COLORS['success'], cfg.COLORS['warning'], cfg.COLORS['error']],
                        hole=0.4,
                    )])

                    fig.update_layout(
                        title="Revision Magnitude",
                        height=cfg.CHART_HEIGHT_SMALL,
                        template=cfg.CHART_TEMPLATE,
                        font=dict(family=cfg.FONT_FAMILY_BODY),
                    )

                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Revision analysis is only available for 'Releases' format datasets. Please select a releases dataset from the sidebar.")

# ============================================================================
# TAB 4: DATA EXPLORER
# ============================================================================

if cfg.ENABLE_DATA_EXPLORER:
    tab_idx = tab_names.index("explorer")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Data Explorer</div>', unsafe_allow_html=True)

        # Search and filter
        col1, col2 = st.columns([2, 1])

        with col1:
            search_term = st.text_input("🔍 Search in data", "")

        with col2:
            show_nulls_only = st.checkbox("Show null values only", False)

        # Apply filters
        display_df = selected_df.copy()

        if search_term:
            # Search in index and columns
            mask = display_df.index.astype(str).str.contains(search_term, case=False)
            display_df = display_df[mask]

        if show_nulls_only:
            # Show only rows with null values
            display_df = display_df[display_df.isna().any(axis=1)]

        # Display table
        st.markdown(f"**Showing {len(display_df)} of {len(selected_df)} rows**")

        st.dataframe(
            display_df,
            use_container_width=True,
            height=cfg.DEFAULT_TABLE_HEIGHT
        )

        # Download buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            csv = display_df.to_csv().encode('utf-8')
            timestamp = datetime.now().strftime(cfg.DOWNLOAD_TIMESTAMP_FORMAT)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{cfg.DOWNLOAD_FILENAME_PREFIX}_{selected_dataset_name.lower().replace(' ', '_')}_{timestamp}.csv",
                mime='text/csv',
                use_container_width=True
            )

        with col2:
            excel_buffer = BytesIO()
            try:
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    display_df.to_excel(writer, sheet_name='Data')
                excel_data = excel_buffer.getvalue()

                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_data,
                    file_name=f"{cfg.DOWNLOAD_FILENAME_PREFIX}_{selected_dataset_name.lower().replace(' ', '_')}_{timestamp}.xlsx",
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            except:
                st.info("Install openpyxl to enable Excel export")

        with col3:
            json_str = display_df.to_json(orient='index', indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"{cfg.DOWNLOAD_FILENAME_PREFIX}_{selected_dataset_name.lower().replace(' ', '_')}_{timestamp}.json",
                mime='application/json',
                use_container_width=True
            )

# ============================================================================
# TAB 5: DOCUMENTATION
# ============================================================================

if cfg.ENABLE_DOCUMENTATION:
    tab_idx = tab_names.index("docs")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Documentation</div>', unsafe_allow_html=True)

        st.markdown(f"""
        ## About This Dashboard

        This interactive dashboard provides comprehensive visualization and exploration tools for the **{cfg.PROJECT_NAME}**.

        ### Dataset Types

        1. **RTD (Real-Time Dataset)**: Vintage format showing how GDP data evolved over time
        2. **Releases Dataset**: Release format showing 1st, 2nd, 3rd... releases for each target period
        3. **Benchmark Dataset**: Vintages immediately before base-year changes
        4. **Base-Year Adjusted**: Removes revisions caused by base-year updates

        ### Dashboard Features

        - **Overview**: Dataset summary statistics, preview, and key metrics
        - **Visualization**: Interactive charts including heatmaps, time series, distributions, and comparisons
        - **Revision Analysis**: Statistical analysis of GDP revisions (for releases format datasets)
        - **Data Explorer**: Full dataset browsing with search, filter, and download capabilities
        - **Settings**: Customize dashboard appearance and behavior

        ### Usage Tips

        - 📊 **Select datasets** from the sidebar dropdown
        - 🎨 **Change themes** in the sidebar (Settings tab for more options)
        - 📈 **Hover over charts** for detailed information
        - 📥 **Download data** in CSV, Excel, or JSON format
        - 🔍 **Search and filter** data in the Data Explorer tab

        ### Keyboard Shortcuts

        - `R` - Rerun the dashboard
        - `C` - Clear cache
        - `Ctrl/Cmd + K` - Focus search box

        ### Resources

        - 📖 [Main README](../README.md)
        - 📚 [Usage Guide](../docs/USAGE.md)
        - 🏗️ [Architecture Documentation](../docs/ARCHITECTURE.md)
        - 🤝 [Contributing Guide](../docs/CONTRIBUTING.md)
        - 💻 [GitHub Repository](https://github.com/JasonCruz18/peru_gdp_revisions)

        ### Running the Pipeline

        To update the RTD with the latest data:

        ```bash
        # Complete pipeline
        python scripts/update_rtd.py

        # Specific steps only
        python scripts/update_rtd.py --steps 3,4,5,6

        # Verbose mode
        python scripts/update_rtd.py --verbose
        ```

        ### Citation

        If you use this dataset in your research, please cite:

        ```bibtex
        @article{{cruz2025gdp,
          title={{Rationality and Nowcasting on Peruvian GDP Revisions}},
          author={{Cruz, Jason}},
          year={{2025}},
          institution={{{cfg.PROJECT_INSTITUTION}}}
        }}
        ```

        ### Contact & Support

        - **Author**: {cfg.PROJECT_AUTHOR}
        - **Institution**: {cfg.PROJECT_INSTITUTION}
        - **GitHub**: [@JasonCruz18](https://github.com/JasonCruz18)

        ### Customization

        This dashboard is fully customizable! Edit `dashboard/config.py` to:

        - Change color themes
        - Add your project logo
        - Adjust font sizes and families
        - Configure chart settings
        - Enable/disable features
        - And much more!

        See the **Settings** tab for live customization options.
        """)

# ============================================================================
# TAB 6: SETTINGS (Optional)
# ============================================================================

if cfg.ENABLE_SETTINGS:
    tab_idx = tab_names.index("settings")
    with tabs[tab_idx]:
        st.markdown(f'<div class="section-header">Dashboard Settings</div>', unsafe_allow_html=True)

        st.markdown("""
        ### Theme Customization

        To permanently customize the dashboard, edit `dashboard/config.py`.

        **Current Theme**: `{}`

        **Available Themes**:
        - `professional` - Blue and orange (default)
        - `academic` - Dark blue and purple
        - `ocean` - Blue tones
        - `forest` - Green tones
        - `sunset` - Red and blue
        - `custom` - Define your own colors
        """.format(cfg.THEME_PRESET))

        st.markdown("### Current Color Scheme")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            **Primary Colors**
            - Primary: <span style="color:{cfg.COLORS['primary']}">●</span> `{cfg.COLORS['primary']}`
            - Secondary: <span style="color:{cfg.COLORS['secondary']}">●</span> `{cfg.COLORS['secondary']}`
            - Accent: <span style="color:{cfg.COLORS['accent']}">●</span> `{cfg.COLORS['accent']}`
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            **Background Colors**
            - Background: <span style="color:{cfg.COLORS['background']}">●</span> `{cfg.COLORS['background']}`
            - Sidebar: <span style="color:{cfg.COLORS['sidebar']}">●</span> `{cfg.COLORS['sidebar']}`
            - Text: <span style="color:{cfg.COLORS['text']}">●</span> `{cfg.COLORS['text']}`
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            **Status Colors**
            - Success: <span style="color:{cfg.COLORS['success']}">●</span> `{cfg.COLORS['success']}`
            - Warning: <span style="color:{cfg.COLORS['warning']}">●</span> `{cfg.COLORS['warning']}`
            - Error: <span style="color:{cfg.COLORS['error']}">●</span> `{cfg.COLORS['error']}`
            """, unsafe_allow_html=True)

        st.markdown("### Typography")

        st.markdown(f"""
        - **Headings**: {cfg.FONT_FAMILY_HEADING}
        - **Body**: {cfg.FONT_FAMILY_BODY}
        - **Monospace**: {cfg.FONT_FAMILY_MONO}
        """)

        st.markdown("### Features")

        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("Dark Mode Toggle", cfg.ENABLE_DARK_MODE_TOGGLE, disabled=True)
            st.checkbox("Export Charts", cfg.ENABLE_EXPORT_CHARTS, disabled=True)
            st.checkbox("Advanced Filters", cfg.ENABLE_ADVANCED_FILTERS, disabled=True)

        with col2:
            st.checkbox("Comparison Mode", cfg.ENABLE_COMPARISON_MODE, disabled=True)
            st.checkbox("Show Footer", cfg.SHOW_FOOTER, disabled=True)
            st.checkbox("Use Logo", cfg.USE_LOGO, disabled=True)

        st.info("💡 These settings are read from `dashboard/config.py`. Edit that file to make permanent changes.")

# ============================================================================
# FOOTER
# ============================================================================

if cfg.SHOW_FOOTER:
    st.markdown("---")

    footer_content = f"<div class='footer'>{cfg.FOOTER_TEXT}"

    if cfg.FOOTER_LINKS:
        footer_content += " | "
        links = [f"<a href='{url}'>{name}</a>" for name, url in cfg.FOOTER_LINKS.items()]
        footer_content += " · ".join(links)

    footer_content += "</div>"

    st.markdown(footer_content, unsafe_allow_html=True)

# Add BytesIO import for Excel export
from io import BytesIO
