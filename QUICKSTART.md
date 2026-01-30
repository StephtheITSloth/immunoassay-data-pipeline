# Quick Start Guide

Get up and running with the Immunoassay Data Pipeline in 5 minutes!

## ⚡ Quick Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/immunoassay-data-pipeline.git
cd immunoassay-data-pipeline

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Run Your First Analysis

### Option 1: Basic Processing (3 steps)

```bash
# Run the basic processor
python elisa_processor.py

# When prompted, enter your data file path:
# Enter the path to the ELISA data CSV file: data/elisa_data.csv

# View results
cat elisa_result.csv
```

### Option 2: Advanced Analysis with Standard Curve (4 steps)

```bash
# Run the advanced analysis
python advanced_elisa_analysis.py

# When prompted, enter both file paths:
# Enter path to ELISA data CSV: data/elisa_data.csv
# Enter path to standard values CSV: data/standard_values.csv

# View outputs
cat elisa_report.txt          # Text report
open elisa_analysis.png       # Visualizations (use 'xdg-open' on Linux)
```

### Option 3: Interactive Jupyter Notebook

```bash
# Install Jupyter (if not already installed)
pip install jupyter

# Launch notebook
jupyter notebook notebooks/elisa_analysis_demo.ipynb

# Follow the step-by-step walkthrough in your browser
```

## 📊 Understanding the Output

### elisa_result.csv
```csv
Sample,OD1,OD2,AverageOD,CorrectedOD,Concentration (ng/ml)
Sample1,0.443,0.488,0.4655,0.3430,15.23
Sample2,0.433,0.430,0.4315,0.3090,12.87
...
```

### elisa_report.txt
```
======================================================================
ELISA ANALYSIS REPORT
======================================================================

Blank OD: 0.1225

Standard Curve Parameters (4PL Model):
  A (min asymptote): -0.0803
  B (Hill slope): 0.7351
  C (EC50): 7.3803
  D (max asymptote): 0.9279

Sample Results:
----------------------------------------------------------------------
Sample1: OD = 0.3430, Conc = 11.46 ng/ml
...
```

### elisa_analysis.png
- **Left panel**: Standard curve with data points and 4PL fit
- **Right panel**: Bar chart of calculated concentrations

## 📝 Using Your Own Data

### Data Format Requirements

**Immunoassay Data File** (e.g., `my_immunoassay_data.csv`):
```csv
Sample,OD1,OD2
Sample1,0.443,0.488
Sample2,0.433,0.430
BLANK,0.110,0.135
```

**Standard Values File** (e.g., `my_standards.csv`):
```csv
Samples,OD1,OD2,Concentration (ng/ml)
STD1,0.319,0.315,2.058
STD2,0.618,0.463,6.173
...
```

### Important Notes
- Blank sample MUST be labeled as "BLANK" (case-insensitive)
- Include duplicate measurements (OD1, OD2) for quality control
- Standard concentrations should span expected sample range
- Use at least 5-6 standard points for reliable curve fitting

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## 📚 Next Steps

1. **Explore the code**: Check out `elisa_processor.py` and `advanced_elisa_analysis.py`
2. **Read the documentation**: See `README.md` for detailed information
3. **Try the notebook**: Interactive demo in `notebooks/elisa_analysis_demo.ipynb`
4. **Customize for your needs**: Modify parameters, add features
5. **Contribute**: See `CONTRIBUTING.md` for guidelines

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: Blank not found warning
**Solution**: Ensure blank sample is labeled exactly as "BLANK" in CSV

**Issue**: Poor curve fit (low R²)
**Solution**: Check standard concentrations span appropriate range

**Issue**: Negative corrected OD values
**Solution**: This can happen if sample OD is lower than blank - may indicate experimental issue

## 💡 Pro Tips

- Use `input()` function for flexible file paths
- Check CV% to validate duplicate precision (should be < 15%)
- Verify R² > 0.95 for reliable concentration calculations
- Always include a blank to correct for background signal
- Use log scale for concentration when plotting standard curves

## 📞 Need Help?

- **Issues**: Open an issue on GitHub
- **Questions**: Check the README or ask in discussions
- **Contributions**: See CONTRIBUTING.md

---

Happy analyzing! 🔬📊
