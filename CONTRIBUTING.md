# Contributing to ScholarFlow

Thank you for your interest in contributing to **ScholarFlow**! We welcome contributions from researchers, developers, and knowledge management enthusiasts worldwide.

## How to Contribute

1. **Report Bugs & Suggest Features**: Open an issue on GitHub describing the bug or feature request.
2. **Submit Pull Requests**:
   - Fork the repository and create your feature branch: `git checkout -b feat/my-new-feature`.
   - Make your changes with clean commit messages.
   - Run tests to make sure all pass: `python -m pytest`.
   - Run the pipeline to ensure vault consistency: `python Scripts/run_pipeline.py`.
   - Push to your branch and submit a Pull Request.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/ScholarFlow.git
cd ScholarFlow

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install -e .
pip install pytest pyyaml

# Run tests
pytest
```

## Code Style & Guidelines
- Maintain 100% test pass rate.
- Follow Python PEP 8 conventions.
- Ensure all markdown templates support strict YAML schemas and bilingual annotations (`[EN]` / `[CN]`).
