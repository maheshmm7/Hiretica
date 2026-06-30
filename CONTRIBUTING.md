# Contributing to Hiretica

First off, thank you for considering contributing to **Hiretica**! It's people like you that make Hiretica such a great AI Recruiting Agent.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

*   **Use a clear and descriptive title** for the issue to identify the problem.
*   **Describe the exact steps which reproduce the problem** in as many details as possible.
*   **Provide specific examples to demonstrate the steps**.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

*   **Use a clear and descriptive title**.
*   **Provide a step-by-step description of the suggested enhancement**.
*   **Explain why this enhancement would be useful** to most users.

### Pull Requests

1.  Fork the repo and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  If you've changed APIs, update the documentation.
4.  Ensure the test suite passes (`pytest` for backend).
5.  Make sure your code lints (`npm run lint` for frontend).
6.  Issue that pull request!

## Local Development Setup

### Backend (Python/FastAPI)
1. `cd backend`
2. Create virtual env: `python -m venv venv`
3. Install deps: `pip install -r requirements.txt`
4. Run server: `uvicorn main:app --reload`
5. Run tests: `pytest`

### Frontend (Next.js/React)
1. `cd frontend`
2. Install deps: `npm install`
3. Run dev server: `npm run dev`
4. Run linter: `npm run lint`

## Code Style

*   **Python**: Follow PEP 8 guidelines. Type hints are strongly encouraged.
*   **TypeScript/React**: Follow standard ESLint rules provided in the repository. Use functional components and hooks.

We look forward to your contributions!
