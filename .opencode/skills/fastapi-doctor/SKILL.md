---
name: fastapi-therapist
description: Use when finishing a feature, fixing a bug, before committing FastAPI code.
version: "1.0.0"
---

# FastAPI Therapist

Scans FastAPI codebases for security, performance, correctness, and architecture issues. Outputs a 0–100 health score.

## Setup

```bash
pip install fastapi-therapist
```

## After making FastAPI code changes:

Run `fastapi-therapist . --verbose` and check the score did not regress.

If the score dropped, fix the regressions before committing.

## For general cleanup or code improvement:

Run `fastapi-therapist . --verbose` to scan the full codebase. Fix issues by severity — errors first, then warnings.

## Command

```bash
fastapi-therapist . --verbose
```

| Flag        | Purpose                                       |
| ----------- | --------------------------------------------- |
| `.`         | Scan current directory                        |
| `--verbose` | Show affected files and line numbers per rule |
| `--score`   | Output only the numeric score                 |
