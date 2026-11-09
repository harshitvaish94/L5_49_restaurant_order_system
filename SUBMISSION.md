# Lab 5: Static Code Analysis — Submission

**Name:** Harshit Vaish
**SRN:** PES1G24AM116
**Program analysed:** `restaurant_order_system.py` (Restaurant Order System)

## Summary

I ran Pylint, Bandit and Flake8 on the program, documented the findings, fixed them, and reran the tools to confirm.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.00/10 | 10.00/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues identified |
| Flake8 | 8 warnings | 0 warnings |

## What I fixed

- **Security:** removed `os.system` (shell injection), replaced `eval()` with a validated numeric discount rate, replaced MD5 with SHA-256, used `secrets` instead of `random` for the PIN, and stopped hard-coding and printing the POS secret (now read from the `POS_TERMINAL_SECRET_TOKEN` environment variable).
- **Bugs:** fixed the mutable default argument (`order_log=[]`), replaced the bare `except: pass` with an explicit check, used a `with` block for file writing, and added an `if __name__ == "__main__":` guard.
- **Style:** snake_case function names, docstrings, removed unused imports and variables, simplified boolean returns, fixed line lengths, and used f-strings.

The program still works the same way: it places table T4, voids T2, reports pending tables, calculates the discounted bill (40.5), writes the kitchen ticket file, and shows 3 pending tables.

## Files

| File | Purpose |
|------|---------|
| `restaurant_order_system.py` | Cleaned and fixed program |
| `issues.md` | Issue table (18 issues, with type, line, description, fix) |
| `reflection.md` | Reflection answers |
| `pylint_report_before.txt` / `pylint_report_after.txt` | Pylint reports |
| `bandit_report_before.txt` / `bandit_report_after.txt` | Bandit reports |
| `flake8_report_before.txt` / `flake8_report_after.txt` | Flake8 reports (the "after" file is empty because there are no warnings) |

## Commits

1. Add original static analysis reports
2. Fix Bandit, Flake8 and Pylint issues
3. Add issues table and reflection

## How to reproduce

```bash
pip install pylint bandit flake8
pylint restaurant_order_system.py
bandit -r restaurant_order_system.py
flake8 restaurant_order_system.py
python restaurant_order_system.py
```
