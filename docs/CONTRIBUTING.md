# Contributing Guide

Thank you for your interest in contributing to the Peru GDP Real-Time Dataset project! This document provides guidelines and best practices for contributing.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Contribution Workflow](#contribution-workflow)
4. [Code Standards](#code-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)
8. [Code of Conduct](#code-of-conduct)

---

## Getting Started

### Ways to Contribute

We welcome various types of contributions:

1. **Bug Reports**: Report issues you encounter
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Fix bugs or implement features
4. **Documentation**: Improve or expand documentation
5. **Testing**: Add or improve test coverage
6. **Examples**: Create tutorials or usage examples

### Before You Start

1. **Check existing issues**: See if someone already reported the bug or requested the feature
2. **Open an issue first**: For significant changes, discuss your ideas in an issue before coding
3. **Read the documentation**: Familiarize yourself with the project architecture

---

## Development Setup

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/peru_gdp_revisions.git
cd peru_gdp_revisions

# Add upstream remote
git remote add upstream https://github.com/JasonCruz18/peru_gdp_revisions.git
```

### Step 2: Create Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Step 3: Create Configuration

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml
```

### Step 4: Verify Setup

```bash
# Run smoke tests
python tests/test_smoke.py

# Expected output: All tests pass
```

### Step 5: Create Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## Contribution Workflow

### 1. Plan Your Changes

- Open an issue to discuss significant changes
- Review the [architecture documentation](ARCHITECTURE.md)
- Identify which modules will be affected

### 2. Make Your Changes

- Write clean, well-documented code
- Follow the code standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run smoke tests
python tests/test_smoke.py

# Run specific tests (if applicable)
pytest tests/test_your_module.py

# Test the complete pipeline
python scripts/update_rtd.py --dry-run
```

### 4. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description

Detailed explanation of what changed and why.
Fixes #issue_number (if applicable)"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

---

## Code Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

#### Line Length
```python
# Maximum line length: 100 characters (not 79)
# Configured in pyproject.toml for Black
```

#### Formatting
```bash
# Format code with Black
black peru_gdp_rtd/ scripts/ tests/

# Check before committing
black --check peru_gdp_rtd/
```

#### Import Sorting
```bash
# Sort imports with isort
isort peru_gdp_rtd/ scripts/ tests/

# Configuration in pyproject.toml
```

#### Type Hints

**Always include type hints** for function signatures:

```python
# Good
def extract_table(
    pdf_path: Path,
    pages: List[int],
    area: Optional[List[List[float]]] = None,
) -> List[pd.DataFrame]:
    """Extract tables from PDF."""
    ...

# Bad
def extract_table(pdf_path, pages, area=None):
    """Extract tables from PDF."""
    ...
```

#### Docstrings

Use **Google-style docstrings**:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed, explaining what the function does
    and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    ...
```

#### Naming Conventions

```python
# Variables and functions: snake_case
def calculate_revision(first_release: float, second_release: float) -> float:
    revision_size = second_release - first_release
    return revision_size

# Classes: PascalCase
class NewTableCleaner:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_DOWNLOADS = 60
DEFAULT_DECIMAL_PLACES = 1

# Private functions/methods: _leading_underscore
def _internal_helper_function():
    pass
```

### Configuration

**Never hardcode values** - use configuration:

```python
# Bad
browser = "chrome"
max_downloads = 60

# Good
settings = get_settings('config/config.yaml')
browser = settings.scraper.browser
max_downloads = settings.scraper.max_downloads
```

### Error Handling

Provide specific, informative error messages:

```python
# Good
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Data file not found at {file_path}. "
        f"Please run Step 1 to download PDFs first."
    )
except pd.errors.EmptyDataError:
    raise ValueError(
        f"File {file_path} is empty or corrupted. "
        f"Please re-download the data."
    )

# Bad
try:
    df = pd.read_csv(file_path)
except:
    print("Error reading file")
```

### Logging

Use the logging module instead of print:

```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed debugging information")
logger.info("General information about progress")
logger.warning("Warning about potential issues")
logger.error("Error occurred but execution continues")
logger.critical("Critical error - execution cannot continue")

# Avoid print statements in library code
# print("Processing file...") ❌
logger.info("Processing file...") ✓
```

---

## Testing Guidelines

### Test Structure

```python
"""Test module for component X.

This module tests functionality of component X including:
- Feature A
- Feature B
- Edge cases
"""

import pytest
from peru_gdp_rtd.module import function_to_test


def test_basic_functionality():
    """Test basic functionality works correctly."""
    result = function_to_test(input_data)
    assert result == expected_output


def test_edge_case():
    """Test edge case: empty input."""
    result = function_to_test([])
    assert result == []


def test_error_handling():
    """Test that appropriate error is raised."""
    with pytest.raises(ValueError):
        function_to_test(invalid_input)
```

### Running Tests

```bash
# Run all smoke tests
python tests/test_smoke.py

# Run with pytest (if available)
pytest tests/ -v

# Run specific test file
pytest tests/test_cleaners.py -v

# Run with coverage
pytest tests/ --cov=peru_gdp_rtd --cov-report=html
```

### Test Coverage

Aim for:
- **Critical paths**: 100% coverage
- **Normal functionality**: 80%+ coverage
- **Edge cases**: Document why not tested if coverage < 80%

---

## Documentation

### Code Documentation

1. **Module docstrings**: Explain module purpose
2. **Class docstrings**: Describe class responsibility
3. **Function docstrings**: Detail parameters, returns, raises
4. **Inline comments**: Explain complex logic (sparingly)

### Documentation Files

When adding new features, update:

- `README.md` - If user-facing feature
- `docs/USAGE.md` - If new usage pattern
- `docs/ARCHITECTURE.md` - If architectural change
- `CHANGELOG.md` - All changes

### Notebooks

For tutorial notebooks:

1. Clear explanations for each step
2. Visual outputs (plots, tables)
3. Realistic examples
4. Error handling demonstrations

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code follows style guidelines (Black formatted)
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issue
Fixes #issue_number

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code formatted with Black
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks**: CI/CD runs tests automatically
2. **Code review**: Maintainers review your code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, your PR will be merged

### After Merge

- Delete your feature branch
- Update your fork's main branch
- Celebrate your contribution!

---

## Code of Conduct

### Our Standards

**Positive behavior**:
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

**Unacceptable behavior**:
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

### Enforcement

Violations will be handled by project maintainers, who may:
- Issue warnings
- Temporarily ban contributors
- Permanently ban repeat offenders

### Reporting

Report violations to: jj.cruza@up.edu.pe

---

## Development Tips

### Common Tasks

#### Add a New Cleaning Function

```python
# 1. Add function to appropriate module
# peru_gdp_rtd/cleaners/custom_cleaners.py
def my_cleaning_function(df: pd.DataFrame) -> pd.DataFrame:
    """Clean specific pattern in data."""
    # Your logic
    return df

# 2. Import in __init__.py
# peru_gdp_rtd/cleaners/__init__.py
from .custom_cleaners import my_cleaning_function

# 3. Use in cleaner class
# peru_gdp_rtd/cleaners/new_table_cleaner.py
class NewTableCleaner:
    def clean(self):
        df = self.df
        df = my_cleaning_function(df)
        return df

# 4. Add test
# tests/test_custom_cleaners.py
def test_my_cleaning_function():
    input_df = pd.DataFrame(...)
    result = my_cleaning_function(input_df)
    assert ...
```

#### Add a New Configuration Option

```yaml
# 1. Add to config.yaml
new_feature:
  option1: "value1"
  option2: 42

# 2. Update Settings class
# peru_gdp_rtd/config/settings.py
class NewFeatureSettings(BaseModel):
    option1: str
    option2: int

class Settings(BaseModel):
    ...
    new_feature: NewFeatureSettings

# 3. Use in code
settings = get_settings('config/config.yaml')
value = settings.new_feature.option1
```

### Debugging Tips

```python
# Use logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for interactive debugging
import pdb; pdb.set_trace()

# Or use ipdb (better than pdb)
import ipdb; ipdb.set_trace()

# Use verbose flag
python scripts/update_rtd.py --verbose
```

### Performance Profiling

```python
# Time a function
import time
start = time.time()
result = slow_function()
print(f"Took {time.time() - start:.2f} seconds")

# Profile with cProfile
import cProfile
cProfile.run('slow_function()')

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    ...
```

---

## Getting Help

### Resources

- **Documentation**: Read [docs/](../docs/)
- **Issues**: Search [GitHub Issues](https://github.com/JasonCruz18/peru_gdp_revisions/issues)
- **Architecture**: Review [ARCHITECTURE.md](ARCHITECTURE.md)

### Asking Questions

When asking for help:
1. Search existing issues first
2. Provide context (what you're trying to do)
3. Include error messages and stack traces
4. Share relevant code snippets
5. Describe what you've tried

**Good question**:
```
I'm trying to add a custom cleaning function for sector names, but I'm getting
a KeyError when accessing the mapping dictionary.

Error:
KeyError: 'agricultura'

Code:
def clean_sector(name):
    return sector_mapping[name]  # Line 42

I've checked that 'agricultura' is in the config.yaml sector_mappings.
What am I missing?
```

---

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Project README (for significant contributions)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Your contributions make this project better for everyone. Whether you're fixing a typo or implementing a major feature, your effort is appreciated!

---

## Quick Reference

### Git Commands
```bash
# Update your fork
git fetch upstream
git merge upstream/main

# Create branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Description"

# Push changes
git push origin feature/my-feature
```

### Development Commands
```bash
# Format code
black peru_gdp_rtd/ scripts/ tests/
isort peru_gdp_rtd/ scripts/ tests/

# Run tests
python tests/test_smoke.py

# Run pipeline
python scripts/update_rtd.py --dry-run
python scripts/update_rtd.py --verbose
```

---

## Contact

**Maintainer**: Jason Cruz
**Email**: jj.cruza@up.edu.pe
**GitHub**: [@JasonCruz18](https://github.com/JasonCruz18)
