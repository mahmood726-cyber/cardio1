# Contributing to the Cardiology Meta-Analysis Dataset

Thank you for your interest in contributing! This project aims to create the world's largest and most comprehensive cardiology meta-analysis dataset.

## How to Contribute

### Types of Contributions

1. **New Data Sources**
   - Identify additional cardiology datasets
   - Implement data collectors for new sources
   - Document access procedures

2. **Data Quality Improvements**
   - Report data errors or inconsistencies
   - Improve data cleaning scripts
   - Enhance validation rules

3. **Code Contributions**
   - Bug fixes
   - Performance improvements
   - New features
   - Documentation improvements

4. **Research Contributions**
   - Quality assessment of studies
   - Meta-analysis implementations
   - Statistical method improvements

5. **Documentation**
   - Tutorial improvements
   - Use case examples
   - API documentation

## Getting Started

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write or update tests
5. Update documentation
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Submit a pull request

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and modular

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Run: `pytest tests/`

### Documentation

- Update README.md if adding new features
- Update GETTING_STARTED.md for user-facing changes
- Add docstrings to all new functions
- Update DATA_SOURCES.md for new data sources

### Commit Messages

Use clear, descriptive commit messages:

```
Add ClinicalTrials.gov detailed results extraction

- Implement results section parser
- Add baseline characteristics extraction
- Include outcome measures parsing
- Add unit tests for parser functions
```

## Data Contributions

### Adding New Data Sources

1. Research the data source
2. Document access requirements
3. Implement collector in `scripts/collection/`
4. Add configuration to `config/sources.yaml`
5. Update `DATA_SOURCES.md`
6. Add example usage to documentation

### Data Quality Standards

All contributed data must:

- Be from reputable sources
- Include proper citations
- Be de-identified (patient-level data)
- Follow data use agreements
- Meet quality thresholds

### Quality Assessment

When contributing quality assessments:

- Use standardized tools (Cochrane RoB, Newcastle-Ottawa)
- Document assessment criteria
- Include assessor information
- Note conflicts of interest

## Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. You'll be added to contributors list

## Community Guidelines

### Be Respectful

- Treat all contributors with respect
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

### Be Collaborative

- Discuss major changes before implementing
- Share knowledge and expertise
- Help others when possible
- Acknowledge contributions

### Be Professional

- Follow ethical research standards
- Respect data privacy
- Cite sources appropriately
- Disclose conflicts of interest

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version)
- Error messages or logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Impact on existing functionality

### Data Quality Issues

Include:
- Data source
- Specific record(s) affected
- Nature of the issue
- Suggested correction
- Supporting evidence

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in publications using the dataset
- Invited to collaborate on research projects

## Questions?

- Open an issue for general questions
- Email the maintainers for private inquiries
- Join our discussion forum (link TBD)

## License

By contributing, you agree that your contributions will be licensed under CC BY 4.0.

---

Thank you for helping build the world's largest cardiology meta-analysis dataset!
