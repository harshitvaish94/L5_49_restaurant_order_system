# Lab 5: Static Code Analysis — Issues Table

**Name:** Harshit Vaish
**SRN:** PES1G24AM116
**File analysed:** `restaurant_order_system.py` (Restaurant Order System)

**Results:** Pylint 5.00/10 → **10.00/10** · Bandit 5 issues (2 High, 1 Medium, 2 Low) → **0** · Flake8 8 warnings → **0**

Line numbers refer to the **original** file. Ordered by severity (High → Medium → Low).

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Shell command injection via `os.system` (Bandit B605, High) | Security | 58 | `os.system("echo ... " + filename)` builds a shell command from a string. A filename such as `x; rm -rf ~` would run arbitrary commands. | Removed the shell call entirely and used `print()` to report the export. (If a real printer command were needed: `subprocess.run([...], shell=False)` with an argument list.) |
| 2 | Weak MD5 hash (Bandit B324, High) | Security | 47 | `hashlib.md5` is cryptographically broken and flagged for security use. | Replaced with `hashlib.sha256`. |
| 3 | Use of `eval()` on a caller-supplied string (Bandit B307, Medium; Pylint W0123) | Security / Bug | 40–43 | `calculate_discounted_bill` evaluates an arbitrary expression (`promo_expr`), allowing arbitrary code execution. The `base_bill` variable is only "used" through `eval`, so Pylint/Flake8 also reported it as unused (W0612/F841). | Replaced the expression string with a numeric `discount_rate` (validated to 0.0–1.0 with `ValueError`). Result is `base_bill * (1 - discount_rate)`; `main()` now passes `0.10` and still gets 40.5. |
| 4 | Hard-coded secret and secret printed to console | Security | 71, 80 | `pos_terminal_key = "POS_TERMINAL_SECRET_TOKEN_2026"` is committed in source and then printed in the output (not caught by the tools, found by reading the program output). | Read the token from the `POS_TERMINAL_SECRET_TOKEN` environment variable and only print whether it is configured, never its value. |
| 5 | Mutable default argument (Pylint W0102) | Bug | 15 | `order_log=[]` is created once and shared across all calls, so log entries leak between unrelated calls. | Changed default to `None` and create a new list inside the function. Verified: separate calls get separate logs. |
| 6 | Bare `except` + silent `pass` (Pylint W0702, Flake8 E722, Bandit B110 Low) | Bug / Reliability | 23–27 | `voidTableOrder` swallows every exception (even `KeyboardInterrupt`) and gives the caller no feedback on whether a void happened. | Removed the try/except; check `table_id in orders` first and return `True`/`False`. |
| 7 | Insecure random for a PIN (Bandit B311, Low) | Security | 50–51 | `random.randint` is predictable and unsuitable for POS PINs. | Used `secrets.randbelow(9000) + 1000` (still a 4-digit PIN). |
| 8 | Resource leak / unsafe file handling (Pylint R1732, W1514) | Bug / Style | 54–57 | File opened manually with `open()`/`close()` (not closed if `write` raises) and no encoding specified. | Used `with open(filename, "w", encoding="utf-8")`. |
| 9 | Code runs on import (no `__main__` guard) | Bug / Design | 83 | `main()` is called at module level, so importing the module places orders, writes a file and prints output. | Wrapped in `if __name__ == "__main__":`. |
| 10 | Variable shadows global (Pylint W0621) | Style | 61 | Parameter `orders` shadows the module-level `orders` dict. | Renamed parameter to `order_book`. |
| 11 | Comparison to `None` with `==` (Pylint C0121, Flake8 E711) | Style | 32 | `orders.get(x) == None` should use identity. | Changed to `is None`. |
| 12 | Redundant if/else returning booleans (Pylint R1703, R1705) | Style | 34–37 | `if ...: return True else: return False` is just a boolean expression. | `return not order["is_settled"]`. |
| 13 | Unused import and variables (Pylint W0611, W0612; Flake8 F401, F841) | Style | 6, 31, 41, 63 | `math` imported but unused; `service_tax`, `base_bill` (original), and loop variable `t` unused. | Removed `math` and `service_tax`; used `.values()` in a generator expression for the pending count. |
| 14 | Function names not snake_case (Pylint C0103) | Style | 15, 23, 30, 40 | `placeTableOrder`, `voidTableOrder`, `checkTableStatus`, `calculateDiscountedBill` use camelCase. | Renamed to `place_table_order`, `void_table_order`, `check_table_status`, `calculate_discounted_bill` and updated all callers. |
| 15 | Missing docstrings (Pylint C0116) | Style | 15–66 | Nine functions had no docstring. | Added a docstring to every function. |
| 16 | Line too long (Pylint C0301, Flake8 E501) | Style | 18, 19, 75 | Lines exceeded 79 characters. | Wrapped the dict literal and long calls across lines. |
| 17 | f-string preferred (Pylint C0209) | Style | 19 | `%`-formatting used for the log message. | Converted to an f-string. |
| 18 | Magic number for dish price | Maintainability | 18 | `15.0` hard-coded inside the function. | Extracted to the constant `PRICE_PER_DISH`. |

## Verification (before → after)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.00/10 (26 messages) | **10.00/10** |
| Bandit | 5 issues: 2 High, 1 Medium, 2 Low | **No issues identified** |
| Flake8 | 8 warnings | **0 warnings** |

Reports saved as `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt` and the matching `_after.txt` files.

The program still does its job: `python restaurant_order_system.py` places T4, voids T2, reports T1 as pending, prints the discounted bill (40.50), the ticket hash, a PIN, writes `kitchen_orders.txt`, and shows 3 pending tables.

## Note on behaviour that "looked wrong"
The README says the program "asks one question", but the supplied file contains no `input()` call, so there is nothing to answer. The output problems I did notice were the printed secret token (#4) and the silent failure of voiding a non-existent table (#6).
