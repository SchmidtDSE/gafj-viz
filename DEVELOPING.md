# Development Setup Guide

This guide provides instructions for setting up a local development environment for the GAFJ visualization project.

## Prerequisites

- Python 3.10+ (Note: Python 3.12 requires special environment variables for bezier)
- Git
- `unzip` command-line tool

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd gafj-viz
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# Or on Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Note: For older versions of sketchingpy with bezier issues on Python 3.12+:
```bash
BEZIER_IGNORE_VERSION_CHECK=1 BEZIER_NO_EXTENSION=1 pip install -r requirements.txt
```

### 4. Install Development Tools

```bash
pip install mypy pycodestyle pyflakes nose2
```

### 5. Download Third-Party Dependencies

Run the dependency loader script to download fonts and web assets:

```bash
bash support/load_deps.sh
```

This will download:
- IBM Plex Mono font
- D3.js library
- Tabby UI components
- Sketchingpy self-hosting files

## Validation Commands

### Linting and Code Quality

Run these commands to ensure code quality:

```bash
# Check for Python syntax errors and undefined names
pyflakes *.py

# Check code style (PEP 8 compliance)
pycodestyle *.py

# Type checking
mypy *.py
```

### Running Tests

```bash
# Unit tests
nose2

# Integration tests
bash support/test_integration.sh
```

### Full Validation Suite

To run all validation checks (matching CI/CD):

```bash
# Run all checks in sequence
pyflakes *.py && \
pycodestyle *.py && \
mypy *.py && \
nose2 && \
bash support/test_integration.sh
```

## Project Structure

- `*.py` - Main Python source files for visualizations
- `test_*.py` - Unit test files
- `support/` - Build and deployment scripts
- `third_party/` - External Python dependencies (self-hosted)
- `third_party_web/` - External web dependencies (fonts, JS libraries)
- `css/`, `js/`, `img/` - Web assets
- `csv/`, `geojson/`, `sql/`, `txt/` - Data files
- `.github/workflows/` - GitHub Actions CI/CD configuration

## Configuration

- `setup.cfg` - Contains pycodestyle configuration
  - Max line length: 100 characters
  - Ignored rules: E125, E128, E502, E731, E722, E402

## Deployment

The project includes automated deployment via GitHub Actions:
- **Test Job**: Runs on every push
- **Deploy Web**: Deploys to production on main branch
- **Deploy Lambda**: Updates AWS Lambda functions on main branch

## Common Issues

### bezier Installation Error (Older Versions)

If using older versions of sketchingpy and encountering bezier version compatibility issues:
```bash
BEZIER_IGNORE_VERSION_CHECK=1 BEZIER_NO_EXTENSION=1 pip install -r requirements.txt
```

### Missing unzip Command

Install unzip if not available:
```bash
# Ubuntu/Debian
sudo apt-get install unzip

# macOS
brew install unzip

# Or use your system's package manager
```

## Development Workflow

1. Create a new branch for your feature/fix
2. Make your changes
3. Run the validation suite
4. Commit your changes
5. Push to GitHub and create a pull request
6. CI/CD will automatically run tests on your PR

## Additional Resources

- [README.md](README.md) - Project overview and usage
- [GitHub Actions Workflow](.github/workflows/build.yml) - CI/CD configuration