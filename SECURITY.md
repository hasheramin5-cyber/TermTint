# Security Policy

## Supported versions

Security fixes are applied to the latest released version of TermTint.

| Version | Supported |
|:--------|:----------|
| 0.5.x   | Yes       |
| < 0.5   | No        |

## Reporting a vulnerability

Please do **not** report security problems in a public issue.

Use GitHub's private reporting instead:

1. Open the [Security tab](https://github.com/hasheramin5-cyber/TermTint/security) of this repository.
2. Click **Report a vulnerability**.
3. Describe the problem, the affected version and, if possible, steps to reproduce it.

You can expect an acknowledgement within a few days. Once a fix is ready, it will be
released and the report will be credited unless you prefer to stay anonymous.

## Scope

TermTint is a small, zero-runtime-dependency library that builds ANSI escape sequences
and reads a few environment variables (`NO_COLOR`, `FORCE_COLOR`, `COLORTERM`, `TERM`).
Examples of in-scope reports:

- escape-sequence injection through input that TermTint is expected to sanitise
- crashes or hangs caused by crafted input to `strip_ansi()` or `visible_len()`
- unsafe behaviour of the Windows console (`ctypes`) integration
