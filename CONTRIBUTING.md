# Contributing to Immunoassay Data Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/immunoassay-data-pipeline.git
   cd immunoassay-data-pipeline
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure:
   - Code follows PEP 8 style guidelines
   - Functions have clear docstrings
   - New features include tests
   - All tests pass

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for all functions
- Keep functions focused and single-purpose

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for high code coverage
- Test edge cases and error conditions

## Areas for Contribution

- **New Features**: Multi-plate support, additional curve fitting models
- **Visualizations**: Interactive plots, statistical comparisons
- **Documentation**: Tutorials, examples, improved docstrings
- **Performance**: Optimization, batch processing
- **Bug Fixes**: Address any issues found

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about usage
- Suggestions for improvement

Thank you for contributing to making laboratory data analysis more accessible!
