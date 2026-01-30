# immunoassay-data-pipeline
Data processing pipeline for immunoassay analysis (ELISA, ELORA, etc.) with  4-parameter logistic curve fitting, automated concentration calculations, and  publication-quality visualizations

cd immunoassay-data-pipeline

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test it works
python elisa_processor.py
