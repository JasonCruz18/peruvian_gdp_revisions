# Peru GDP RTD Dashboard

Interactive Streamlit dashboard for exploring and visualizing the Peru GDP Real-Time Dataset.

## Features

- **Dataset Overview**: Summary statistics and data preview
- **Interactive Visualizations**:
  - Heatmaps showing GDP evolution over vintages
  - Time series plots for specific periods
  - Distribution plots of GDP growth rates
- **Revision Analysis**:
  - Statistical analysis of revisions
  - Revision distribution plots
  - Revision magnitude over time
- **Data Explorer**: Browse and download datasets
- **Documentation**: In-app user guide

## Installation

### Prerequisites

Install the main project first:

```bash
cd peru_gdp_revisions
pip install -r requirements.txt
```

### Install Dashboard Dependencies

```bash
pip install -r dashboard/requirements.txt
```

Or install specific packages:

```bash
pip install streamlit plotly pandas
```

## Usage

### Run the Dashboard

```bash
# From project root
streamlit run dashboard/app.py

# Or from dashboard directory
cd dashboard
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

### Generate Data First

Before running the dashboard, ensure you have generated the RTD datasets:

```bash
# Run complete pipeline
python scripts/update_rtd.py

# Or run specific steps
python scripts/update_rtd.py --steps 3,4,5,6
```

The dashboard will look for datasets in `data/output/` directory.

## Available Datasets

The dashboard can visualize these datasets:

1. **Monthly RTD** (`monthly_gdp_rtd.csv`)
2. **Quarterly RTD** (`quarterly_annual_gdp_rtd.csv`)
3. **Monthly Releases** (`monthly_gdp_releases.csv`)
4. **Quarterly Releases** (`quarterly_annual_gdp_releases.csv`)
5. **Monthly Benchmark** (`monthly_gdp_benchmark.csv`)
6. **Quarterly Benchmark** (`quarterly_annual_gdp_benchmark.csv`)

Plus base-year adjusted versions of each.

## Dashboard Tabs

### 1. Overview
- Dataset dimensions and statistics
- Data preview (first 20 rows)
- Summary statistics table

### 2. Visualization
Three visualization types:
- **Heatmap**: Color-coded matrix of all values
- **Time Series**: Line plots for selected periods
- **Distribution**: Histogram of all growth rates

### 3. Revision Analysis
Available for "Releases" format datasets:
- Mean, median, min, max revision statistics
- Revision distribution histogram
- Revision magnitude over time

### 4. Data Explorer
- Full dataset table (scrollable)
- Download as CSV button
- Search and filter capabilities

### 5. Documentation
- User guide
- Dataset explanations
- Links to additional resources

## Configuration

### Customize Appearance

Edit `app.py` to customize:

```python
# Page configuration
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="📊",
    layout="wide",  # or "centered"
)
```

### Custom CSS

Modify the CSS in the `st.markdown()` section to change styling.

## Keyboard Shortcuts

- `R`: Rerun the app
- `C`: Clear cache
- `Ctrl/Cmd + K`: Focus search
- `Ctrl/Cmd + /`: Show keyboard shortcuts

## Performance Tips

1. **Cache data loading**: Already implemented with `@st.cache_data`
2. **Limit data size**: For very large datasets, consider:
   - Loading subset of data
   - Aggregating before visualization
   - Using Parquet format

3. **Optimize plots**:
   - Limit number of time series lines
   - Reduce histogram bins for large datasets

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `dashboard/app.py` as main file
5. Deploy!

### Deploy Locally with Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install -r dashboard/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t peru-gdp-dashboard .
docker run -p 8501:8501 peru-gdp-dashboard
```

## Troubleshooting

### Issue: "No datasets found"

**Solution**: Run the pipeline first to generate datasets:
```bash
python scripts/update_rtd.py
```

### Issue: Dashboard won't start

**Solution**: Check dependencies are installed:
```bash
pip install -r dashboard/requirements.txt
```

### Issue: Slow performance

**Solution**:
- Clear cache: Press 'C' in the app
- Restart: Press 'R' in the app
- Restart server: `Ctrl+C` and rerun

### Issue: Port already in use

**Solution**: Use different port:
```bash
streamlit run dashboard/app.py --server.port 8502
```

## Examples

### Load Custom Dataset

```python
# In app.py, modify load_rtd_data():
datasets["My Custom Data"] = pd.read_csv("path/to/custom.csv", index_col=0)
```

### Add Custom Visualization

```python
# In Tab 2 (Visualization), add new option:
elif viz_type == "My Custom Plot":
    st.subheader("Custom Plot")

    fig = px.line(selected_df, ...)
    st.plotly_chart(fig, use_container_width=True)
```

### Add Custom Metric

```python
# In Tab 1 (Overview), add new metric:
st.metric("My Metric", calculated_value)
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Main Project README](../README.md)
- [Usage Guide](../docs/USAGE.md)

## Contributing

To contribute improvements:

1. Fork the repository
2. Make changes to `dashboard/app.py`
3. Test locally: `streamlit run dashboard/app.py`
4. Submit pull request

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Contact

**Jason Cruz**
Email: jj.cruza@up.edu.pe
GitHub: [@JasonCruz18](https://github.com/JasonCruz18)
