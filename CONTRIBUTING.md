# Contributing to browserstate-nova-adapter

Thank you for your interest in contributing to the browserstate-nova-adapter project! This document outlines the process for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally: 
   ```bash
   git clone https://github.com/YOUR-USERNAME/browserstate-nova-adapter.git
   cd browserstate-nova-adapter
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Process

1. Create a branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and write tests to verify them

3. Run the test suite:
   ```bash
   pytest
   ```

4. Ensure code quality with linting:
   ```bash
   flake8
   ```

5. Commit your changes with descriptive commit messages:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a Pull Request on GitHub

## Pull Request Guidelines

- Fill in the required PR template
- Include tests for new functionality
- Keep changes focused on a single issue
- Make sure all tests pass before submitting

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We strive to maintain a welcoming and inclusive environment for all contributors. 