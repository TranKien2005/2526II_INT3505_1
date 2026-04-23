# Week8 Test Guide

## 0) Install dependencies in your shared .venv
Run from project root:

```bash
pip install -r requirements.txt
```

## 1) Unit tests
Run:

```bash
pytest Week8/tests/unit -q
```

## 2) Integration tests
Run:

```bash
pytest Week8/tests/integration -q
```

## 3) Full Python tests
Run:

```bash
pytest Week8/tests -q
```

## 4) Performance tests (k6)
Start API first (`docker compose -f Week8/docker-compose.yml up --build`), then run:

```bash
k6 run Week8/tests/performance/k6_library.js
```

You can override target URL:

```bash
k6 run -e BASE_URL=http://localhost:8000 Week8/tests/performance/k6_library.js
```
