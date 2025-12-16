"""Dashboard configuration file.

Customize the dashboard appearance by modifying the values in this file.
Changes take effect immediately when you refresh the dashboard.
"""

from pathlib import Path

# ============================================================================
# PROJECT BRANDING
# ============================================================================

PROJECT_NAME = "Peru GDP Real-Time Dataset"
PROJECT_SUBTITLE = "Interactive Exploration of GDP Revisions and Real-Time Data"
PROJECT_AUTHOR = "Jason Cruz"
PROJECT_INSTITUTION = "Universidad del Pacífico - CIUP"
PROJECT_YEAR = "2025"

# Logo configuration
# Place your logo file in dashboard/assets/ directory
LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"
USE_LOGO = True  # Set to False to hide logo
LOGO_WIDTH = 200  # Logo width in pixels

# ============================================================================
# COLOR SCHEME
# ============================================================================

# Choose a preset theme or define custom colors below
# Available presets: "professional", "academic", "ocean", "forest", "sunset", "custom"
THEME_PRESET = "professional"

# Theme Presets (automatically applied based on THEME_PRESET)
THEMES = {
    "professional": {
        "primary": "#1f77b4",      # Blue
        "secondary": "#ff7f0e",    # Orange
        "accent": "#2ca02c",       # Green
        "background": "#ffffff",    # White
        "sidebar": "#f0f2f6",      # Light gray
        "text": "#262730",         # Dark gray
        "success": "#28a745",      # Green
        "warning": "#ffc107",      # Yellow
        "error": "#dc3545",        # Red
    },
    "academic": {
        "primary": "#003f5c",      # Dark blue
        "secondary": "#bc5090",    # Purple
        "accent": "#ffa600",       # Gold
        "background": "#ffffff",    # White
        "sidebar": "#f8f9fa",      # Light gray
        "text": "#2b2d42",         # Dark blue-gray
        "success": "#06d6a0",      # Teal
        "warning": "#f77f00",      # Orange
        "error": "#d62828",        # Red
    },
    "ocean": {
        "primary": "#006994",      # Ocean blue
        "secondary": "#0099cc",    # Sky blue
        "accent": "#00cc99",       # Turquoise
        "background": "#f0f8ff",   # Alice blue
        "sidebar": "#e6f3ff",      # Light blue
        "text": "#003d5c",         # Dark blue
        "success": "#00cc99",      # Turquoise
        "warning": "#ff9933",      # Coral
        "error": "#cc3333",        # Red
    },
    "forest": {
        "primary": "#2d6a4f",      # Forest green
        "secondary": "#52b788",    # Light green
        "accent": "#95d5b2",       # Mint
        "background": "#f8fff8",   # White-green
        "sidebar": "#e8f5e9",      # Very light green
        "text": "#1b4332",         # Dark green
        "success": "#40916c",      # Green
        "warning": "#f4a261",      # Tan
        "error": "#e76f51",        # Terra cotta
    },
    "sunset": {
        "primary": "#e63946",      # Red
        "secondary": "#f1faee",    # Off-white
        "accent": "#a8dadc",       # Light blue
        "background": "#ffffff",    # White
        "sidebar": "#f1faee",      # Off-white
        "text": "#1d3557",         # Navy
        "success": "#06d6a0",      # Teal
        "warning": "#ffb703",      # Yellow
        "error": "#e63946",        # Red
    },
    "custom": {
        # Define your own colors here when THEME_PRESET = "custom"
        "primary": "#1f77b4",
        "secondary": "#ff7f0e",
        "accent": "#2ca02c",
        "background": "#ffffff",
        "sidebar": "#f0f2f6",
        "text": "#262730",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545",
    },
}

# Get current theme colors
COLORS = THEMES.get(THEME_PRESET, THEMES["professional"])

# ============================================================================
# TYPOGRAPHY
# ============================================================================

# Font families (Google Fonts or system fonts)
FONT_FAMILY_HEADING = "'Roboto Slab', serif"
FONT_FAMILY_BODY = "'Inter', 'Segoe UI', sans-serif"
FONT_FAMILY_MONO = "'Fira Code', 'Courier New', monospace"

# Font sizes (in rem)
FONT_SIZE_TITLE = "2.5rem"
FONT_SIZE_HEADING = "1.75rem"
FONT_SIZE_SUBHEADING = "1.25rem"
FONT_SIZE_BODY = "1rem"
FONT_SIZE_SMALL = "0.875rem"

# ============================================================================
# LAYOUT
# ============================================================================

# Page layout
PAGE_LAYOUT = "wide"  # "wide" or "centered"
SIDEBAR_STATE = "expanded"  # "expanded" or "collapsed"

# Component spacing
SECTION_SPACING = "2rem"
COMPONENT_SPACING = "1rem"

# Border radius for cards and components
BORDER_RADIUS = "0.5rem"
BORDER_RADIUS_LARGE = "1rem"

# Shadows
BOX_SHADOW = "0 2px 4px rgba(0,0,0,0.1)"
BOX_SHADOW_HOVER = "0 4px 8px rgba(0,0,0,0.15)"

# ============================================================================
# CHART SETTINGS
# ============================================================================

# Default chart template
# Options: "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"
CHART_TEMPLATE = "plotly_white"

# Chart color scales
CHART_COLOR_SCALE = "RdBu_r"  # For heatmaps
CHART_LINE_COLORS = [
    COLORS["primary"],
    COLORS["secondary"],
    COLORS["accent"],
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-green
    "#17becf",  # Cyan
]

# Chart dimensions
CHART_HEIGHT_SMALL = 300
CHART_HEIGHT_MEDIUM = 500
CHART_HEIGHT_LARGE = 700

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

SIDEBAR_TITLE = "Navigation"
SHOW_DATASET_INFO = True
SHOW_LAST_UPDATED = True

# ============================================================================
# TAB CONFIGURATION
# ============================================================================

# Enable/disable tabs
ENABLE_OVERVIEW = True
ENABLE_VISUALIZATION = True
ENABLE_REVISION_ANALYSIS = True
ENABLE_DATA_EXPLORER = True
ENABLE_DOCUMENTATION = True
ENABLE_SETTINGS = True  # NEW: Settings tab for live customization

# Tab icons (requires streamlit-extras or emoji)
TAB_ICONS = {
    "overview": "📊",
    "visualization": "📈",
    "revision": "🔍",
    "explorer": "📋",
    "docs": "📖",
    "settings": "⚙️",
}

# ============================================================================
# ADVANCED CUSTOMIZATION
# ============================================================================

# Custom CSS (applied in addition to theme)
CUSTOM_CSS = """
/* Add your custom CSS here */

/* Example: Custom button styling */
.stButton > button {
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* Example: Custom metric styling */
.metric-value {
    font-weight: 700;
}

/* Example: Gradient header */
.gradient-header {
    background: linear-gradient(90deg, {primary} 0%, {secondary} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
"""

# JavaScript for advanced interactions (optional)
CUSTOM_JS = """
// Add custom JavaScript here if needed
console.log('Peru GDP RTD Dashboard loaded');
"""

# ============================================================================
# DATA DISPLAY SETTINGS
# ============================================================================

# Number formatting
DECIMAL_PLACES = 2
PERCENTAGE_FORMAT = "{:.2f}%"

# Table settings
DEFAULT_TABLE_HEIGHT = 600
ROWS_PER_PAGE = 20

# Download settings
DOWNLOAD_FILENAME_PREFIX = "peru_gdp_rtd"
DOWNLOAD_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ============================================================================
# FEATURES FLAGS
# ============================================================================

ENABLE_DARK_MODE_TOGGLE = True
ENABLE_EXPORT_CHARTS = True
ENABLE_ADVANCED_FILTERS = True
ENABLE_COMPARISON_MODE = True

# ============================================================================
# METADATA DASHBOARD SETTINGS (for metadata_dashboard.py)
# ============================================================================

METADATA_CHART_COLORS = {
    "base_year_timeline": COLORS["primary"],
    "benchmark_periods": COLORS["secondary"],
    "affected_vintages": COLORS["accent"],
}

# ============================================================================
# FOOTER CONFIGURATION
# ============================================================================

SHOW_FOOTER = True
FOOTER_TEXT = f"© {PROJECT_YEAR} {PROJECT_AUTHOR} | {PROJECT_INSTITUTION}"
FOOTER_LINKS = {
    "GitHub": "https://github.com/JasonCruz18/peru_gdp_revisions",
    "Documentation": "../docs/USAGE.md",
    "Paper": "#",  # Add link when available
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_theme_css():
    """Generate CSS from theme configuration."""
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Slab:wght@400;700&family=Fira+Code&display=swap');

        /* Global styles */
        :root {{
            --primary-color: {COLORS['primary']};
            --secondary-color: {COLORS['secondary']};
            --accent-color: {COLORS['accent']};
            --background-color: {COLORS['background']};
            --sidebar-color: {COLORS['sidebar']};
            --text-color: {COLORS['text']};
            --success-color: {COLORS['success']};
            --warning-color: {COLORS['warning']};
            --error-color: {COLORS['error']};
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {FONT_FAMILY_HEADING};
            color: var(--text-color);
        }}

        body, p, div, span {{
            font-family: {FONT_FAMILY_BODY};
            color: var(--text-color);
        }}

        code, pre {{
            font-family: {FONT_FAMILY_MONO};
        }}

        /* Main header */
        .main-header {{
            font-size: {FONT_SIZE_TITLE};
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            text-align: center;
        }}

        .main-subtitle {{
            font-size: {FONT_SIZE_SUBHEADING};
            color: var(--text-color);
            text-align: center;
            margin-bottom: {SECTION_SPACING};
            opacity: 0.8;
        }}

        /* Logo container */
        .logo-container {{
            text-align: center;
            margin-bottom: {COMPONENT_SPACING};
            padding: 1rem;
        }}

        /* Metric cards */
        .metric-card {{
            background: linear-gradient(135deg, {COLORS['sidebar']} 0%, {COLORS['background']} 100%);
            padding: 1.5rem;
            border-radius: {BORDER_RADIUS_LARGE};
            margin: {COMPONENT_SPACING} 0;
            box-shadow: {BOX_SHADOW};
            transition: all 0.3s ease;
            border-left: 4px solid var(--primary-color);
        }}

        .metric-card:hover {{
            box-shadow: {BOX_SHADOW_HOVER};
            transform: translateY(-2px);
        }}

        .metric-label {{
            font-size: {FONT_SIZE_SMALL};
            color: var(--text-color);
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .metric-value {{
            font-size: {FONT_SIZE_HEADING};
            font-weight: 700;
            color: var(--primary-color);
        }}

        /* Section headers */
        .section-header {{
            font-size: {FONT_SIZE_HEADING};
            font-weight: 600;
            color: var(--primary-color);
            margin: {SECTION_SPACING} 0 {COMPONENT_SPACING} 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary-color);
        }}

        /* Info boxes */
        .info-box {{
            background-color: var(--sidebar-color);
            padding: 1rem;
            border-radius: {BORDER_RADIUS};
            margin: {COMPONENT_SPACING} 0;
            border-left: 4px solid var(--accent-color);
        }}

        .success-box {{
            background-color: rgba(40, 167, 69, 0.1);
            border-left-color: var(--success-color);
        }}

        .warning-box {{
            background-color: rgba(255, 193, 7, 0.1);
            border-left-color: var(--warning-color);
        }}

        .error-box {{
            background-color: rgba(220, 53, 69, 0.1);
            border-left-color: var(--error-color);
        }}

        /* Buttons */
        .stButton > button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: {BORDER_RADIUS};
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: {BOX_SHADOW};
        }}

        .stButton > button:hover {{
            background-color: var(--secondary-color);
            box-shadow: {BOX_SHADOW_HOVER};
            transform: translateY(-2px);
        }}

        /* Sidebar */
        .css-1d391kg {{
            background-color: var(--sidebar-color);
        }}

        /* Tables */
        .dataframe {{
            border-radius: {BORDER_RADIUS};
            overflow: hidden;
            box-shadow: {BOX_SHADOW};
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: {SECTION_SPACING} 0;
            margin-top: {SECTION_SPACING};
            border-top: 1px solid var(--sidebar-color);
            font-size: {FONT_SIZE_SMALL};
            color: var(--text-color);
            opacity: 0.7;
        }}

        .footer a {{
            color: var(--primary-color);
            text-decoration: none;
            margin: 0 0.5rem;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        /* Custom additions */
        {CUSTOM_CSS.format(**COLORS)}
    </style>
    """
    return css


def format_number(value, decimal_places=None):
    """Format number with configured decimal places."""
    if decimal_places is None:
        decimal_places = DECIMAL_PLACES
    return f"{value:.{decimal_places}f}"


def format_percentage(value):
    """Format value as percentage."""
    return PERCENTAGE_FORMAT.format(value)
