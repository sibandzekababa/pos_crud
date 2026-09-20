# SME Supermarket POS API

A FastAPI backend for a small supermarket point-of-sale system: authentication
and staff management, categories, suppliers, products (with barcode/camera
scanning), customers, sales/checkout, payments and receipts.

The production app talks to PostgreSQL (see `database.py` / `DATABASE_URL`),
but the automated test suite below runs entirely against an isolated
in-memory SQLite database, so it never touches your real dev database.

## Requirements

- Python 3.10+ (the app is developed against 3.10; the test suite also runs
  fine on 3.12)
- pip

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

pip install -r requirements
```

## Running the API locally

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"  # or leave unset for the default
uvicorn main:app --reload
```

## Running the tests locally

The tests live in `app/tests/` and use `pytest`, `fastapi.testclient.TestClient`,
and an in-memory SQLite database created fresh for every test (via fixtures in
`app/tests/conftest.py`), so nothing in your PostgreSQL dev database is ever
read or written.

1. Install the test dependencies (on top of the runtime ones):

   ```bash
   pip install -r requirements -r requirements-dev.txt
   ```

2. Run the full suite from the repository root:

   ```bash
   pytest
   ```

   This picks up every test file under `app/tests/`, including:
   - CRUD + validation + permission tests for categories, suppliers,
     customers, products and staff users
   - the full sales/checkout flow (stock deduction, change calculation,
     loyalty points, cancellation/restocking)
   - payments and auto-generated receipts
   - auth (login, registration bootstrap, role-based access) and password
     hashing
   - a couple of system-level checks (root endpoint, docs, the IoT
     barcode-scan websocket broadcast)

3. Useful variations:

   ```bash
   pytest -v                              # verbose, one line per test
   pytest app/tests/test_sale_routers.py  # just one file
   pytest --cov=app --cov-report=term-missing  # with coverage
   ```

No environment variables need to be set by hand for the tests - `conftest.py`
points the app at `sqlite:///:memory:` before importing it, overriding
whatever `DATABASE_URL` you may have configured for local development.

## Continuous Integration

Every push and pull request triggers `.github/workflows/ci.yml`, which
checks out the repo, sets up Python, installs dependencies, and runs the
full test suite - the build fails if any test fails.
