# Lab 5: Reflection

**Name:** Harshit Vaish
**SRN:** PES1G24AM116

*(The handout PDF refers to reflection questions but does not print them; these answer the four standard Lab 5 reflection questions.)*

## 1. Which issues were the easiest and hardest to fix?

The easiest were mechanical style issues: removing the unused `math` import and variables, changing `== None` to `is None`, adding docstrings, renaming camelCase functions to snake_case, and wrapping long lines. Flake8 and Pylint point at the exact line and the fix is obvious.

The hardest was the `eval()` in `calculate_discounted_bill`. Simply deleting it would break the feature, so I had to change the design: the caller now passes a numeric `discount_rate` (validated to 0–1) instead of an arbitrary expression string, and `main()` was updated accordingly. The hard-coded secret and the `os.system` call also needed small design decisions (environment variable; replacing the shell call with a print).

## 2. Did the tools report any false positives, or miss anything?

Mostly the reports were accurate. A few findings are low-risk in this specific program: Bandit's B311 (`random`) and B110 (try/except/pass) are Low severity, and the MD5 hash here is only a ticket identifier, so the "weak hash" High rating overstates the real risk — though SHA-256 costs nothing and is the safer habit. Pylint also reported `base_bill` as unused even though `eval` string-references it, which is a symptom of the real problem (hidden dynamic code) rather than a true false positive.

The tools missed things I found by running and reading the program: the secret token is hard-coded and printed to the console (Bandit did not flag it), `main()` runs on import, and `voidTableOrder` silently does nothing for a non-existent table. The README also mentions an interactive question that does not exist in the file. Static analysis complements, but does not replace, running and reviewing the code.

## 3. How could static analysis be integrated into a real development workflow?

Run all three tools automatically: as pre-commit hooks so style and obvious security problems never reach the repo, and in a CI pipeline (e.g. GitHub Actions) on every pull request, failing the build on any Bandit High/Medium finding, any Flake8 error, or a Pylint score below an agreed threshold (like 9.5). Editors can also run them live while coding. Teams should keep a shared config (`.pylintrc`, `setup.cfg`/`.flake8`, `bandit.yaml`) and document any justified suppressions (`# nosec`, `# pylint: disable=...`) with a comment explaining why, so exceptions stay deliberate.

## 4. What tangible improvements did you see in code quality, readability, and security?

- **Security:** removed shell injection (`os.system`), arbitrary code execution (`eval`), weak hashing (MD5), predictable PINs (`random`), and the hard-coded/printed secret. Bandit went from 5 findings (2 High, 1 Medium) to none.
- **Robustness:** fixed the shared mutable default argument, replaced the bare `except: pass` with an explicit check that returns a result, used a `with` block for the file, added input validation for the discount rate, and added a `__main__` guard so importing the module has no side effects.
- **Readability/maintainability:** consistent snake_case names, docstrings on every function, a named `PRICE_PER_DISH` constant, simplified boolean logic, and lines under 79 characters.
- **Score:** Pylint improved from 5.00/10 to 10.00/10, Flake8 from 8 warnings to 0, with the program output unchanged (discounted bill still 40.5, 3 pending tables).
