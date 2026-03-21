# UI and API Automation Framework

This is a demo automation project, in Python. It covers UI tests for [Swag Labs](https://www.saucedemo.com/) and API tests for [JSONPlaceholder](https://jsonplaceholder.typicode.com/).

Test scenarios use **Given-When-Then** and Allure

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Allure CLI](https://allurereport.org/docs/install/)

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/MihaiBalica/demo_automation_framework
cd demo_automation_framework
```

2. **Install dependencies** (uv creates the virtual environment automatically)

```bash
uv sync --all-groups

# optional, to make sure virtual env was created. It should display the path to project + '/.env' 
uv run python -c "import sys; print(sys.prefix)"

```

3. **Install Playwright browsers**

```bash
uv run playwright install chromium
```

4. **Install pre-commit hooks**

```bash
uv run pre-commit install
```

## Running Tests

Run **all tests** (UI + API):

```bash
uv run pytest
```

Run only **UI tests**:

```bash
uv run pytest -m ui
```

Run only **API tests**:

```bash
uv run pytest -m api
```

Run a specific test file:

```bash
uv run pytest tests/ui/test_swag_labs.py
uv run pytest tests/api/test_jsonplaceholder.py
```

Run tests with verbose output:

```bash
uv run pytest -v
```

### Parallel Test Execution

Run tests in parallel using [pytest-xdist](https://github.com/pytest-dev/pytest-xdist):

```bash
# auto-detect number of CPUs
uv run pytest -n auto

# use a specific number of workers
uv run pytest -n 4

# run only API tests in parallel
uv run pytest -m api -n auto

# run only UI tests in parallel
uv run pytest -m ui -n auto
```

> Allure result files (JSON) are written to `allure-results/` automatically on every run
> (configured in `pyproject.toml` via `addopts`).

## Viewing Test Reports

### Allure Report (recommended)

After running the tests, generate and open the interactive Allure HTML report:

```bash
allure serve allure-results
```

This starts a local web server and opens the report in your browser. The report shows:

- Feature/Story hierarchy with executed steps
- Severity labels (Blocker → Critical → Normal → Minor)
- Screenshots attached on UI test failures
- Pass/fail timeline and trends

To generate a static report folder run:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### HTML Report (quick view)

Generate a self-contained HTML report with pytest-html:

```bash
mkdir -p reports
pytest --html=reports/report.html --self-contained-html
```

Open it in any browser:

```bash
open reports/report.html       # macOS
xdg-open reports/report.html   # Linux
start reports/report.html      # Windows
```

## Linting, Formatting & Type-checking

```bash
# lint with ruff
uv run ruff check .

# auto-fix lint issues
uv run ruff check --fix .

# format code
uv run ruff format .

# type-check with pyright
uv run pyright
```

## Pre-commit Hooks

The `.pre-commit-config.yaml` runs the following on every commit:

| Hook | Description |
|---|---|
| `trailing-whitespace` | Remove trailing whitespace |
| `end-of-file-fixer` | Ensure files end with a newline |
| `check-yaml` / `check-json` / `check-toml` | Validate config file syntax |
| `check-added-large-files` | Prevent accidental large file commits |
| `ruff` | Lint + auto-fix |
| `ruff-format` | Code formatting |
| `pyright` | Static type checking |

## Test Scenarios

### UI Tests (Swag Labs)

| # | Scenario | Allure Feature | Severity |
|---|----------|---------------|---------|
| 1 | Successful login with valid credentials | Authentication | Critical |
| 2 | Failed login with invalid credentials | Authentication | Critical |
| 3 | Locked out user sees error | Authentication | Normal |
| 4 | Add a product to the shopping cart | Shopping Cart | Critical |
| 5 | Remove a product from the shopping cart | Shopping Cart | Critical |
| 6 | Cart badge count is updated correctly | Shopping Cart | Normal |
| 7 | Complete checkout process (end-to-end) | Checkout | Blocker |
| 8 | Sort products by price (low to high) | Product Catalogue | Minor |
| 9 | Sort products by price (high to low) | Product Catalogue | Minor |
| 10 | Sort products by name (A to Z) | Product Catalogue | Minor |

### API Tests (JSONPlaceholder)

| # | Scenario | Allure Story | Severity |
|---|----------|-------------|---------|
| 1 | GET /posts — status 200 | GET /posts | Critical |
| 2 | GET /posts — non-empty list | GET /posts | Critical |
| 3 | GET /posts — Post schema valid | GET /posts | Normal |
| 4 | GET /posts/1 — status 200 | GET /posts/{id} | Critical |
| 5 | GET /posts/1 — correct id returned | GET /posts/{id} | Critical |
| 6 | GET /posts/1 — all fields present | GET /posts/{id} | Normal |
| 7 | POST /posts — status 201 | POST /posts | Critical |
| 8 | POST /posts — created resource returned | POST /posts | Critical |
| 9 | PUT /posts/1 — status 200 | PUT /posts/{id} | Critical |
| 10 | PUT /posts/1 — updated fields returned | PUT /posts/{id} | Critical |
| 11 | DELETE /posts/1 — status 200 | DELETE /posts/{id} | Critical |
| 12 | DELETE /posts/1 — empty body returned | DELETE /posts/{id} | Normal |
| 13 | GET /posts?userId=1 — status 200 | GET /posts?userId={id} | Normal |
| 14 | GET /posts?userId=1 — filtered results | GET /posts?userId={id} | Normal |
| 15 | GET /posts/99999 — 404 Not Found | Non-existent Resource | Normal |
| 16 | GET /posts/99999 — empty body | Non-existent Resource | Normal |

## CI/CD

The GitHub Actions workflow (`.github/workflows/tests.yml`) runs automatically on every push and pull request to the `main` branch. It contains two jobs:

1. **Lint & Type-check** — runs `ruff check`, `ruff format --check`, and `pyright` using `uv`
2. **Tests** — runs all API and UI tests (after linting passes)

Both jobs use [uv](https://docs.astral.sh/uv/) for fast, reproducible dependency installation.

Two artifacts are uploaded after each test run:

- **`allure-results`** — raw JSON result files; download and run `allure serve` locally to view the interactive report
- **`html-reports`** — self-contained HTML files for quick online viewing
