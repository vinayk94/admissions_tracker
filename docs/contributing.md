

# Contributing to Django Admissions Tracker

We welcome contributions to the Django Admissions Tracker project! This document outlines the process for contributing to the project.

## Code of Conduct

We are committed to fostering a welcoming and inclusive community. We expect all contributors to adhere to our Code of Conduct, which can be found in the `CODE_OF_CONDUCT.md` file in the root of the repository.

## How to Contribute

1. Fork the Repository
   - Visit the [Django Admissions Tracker repository](https://github.com/vinayk94/admissions_tracker.git) on GitHub.
   - Click the "Fork" button in the upper right corner.

2. Clone Your Fork
   ```
   git clone https://github.com/vinayk94/admissions_tracker.git
   cd django-admissions-tracker
   ```

3. Create a Feature Branch
   ```
   git checkout -b feature/your-feature-name
   ```

4. Make Your Changes
   - Write your code following the style guide below.
   - Commit your changes with clear, descriptive commit messages.

5. Write or Update Tests
   - Ensure your code is covered by unit tests.
   - Run the existing test suite to make sure you haven't broken anything:
     ```
     python manage.py test
     ```

6. Update Documentation
   - If your changes require it, update the relevant documentation in the `docs/` directory.

7. Submit a Pull Request
   - Push your changes to your fork:
     ```
     git push origin feature/your-feature-name
     ```
   - Go to the original repository on GitHub and click "New pull request".
   - Select your feature branch and submit the pull request with a clear description of your changes.

## Style Guide

- Follow PEP 8 style guide for Python code.
- Use 4 spaces for indentation (not tabs).
- Use descriptive variable names and follow Python naming conventions.
- Keep lines to a maximum of 120 characters.
- Write docstrings for all functions, classes, and modules.

## Testing

- Write unit tests for all new functionality.
- Aim for at least 80% test coverage for new code.
- Run the full test suite before submitting a pull request.

## Reporting Issues

- Use the GitHub issue tracker to report bugs or suggest features.
- Before creating a new issue, please check if a similar issue already exists.
- Provide as much detail as possible, including steps to reproduce for bugs.

Thank you for contributing to Django Admissions Tracker!
