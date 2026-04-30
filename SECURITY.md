# Security policy

If you believe you have found a security issue affecting `al-am.in` or any
code published in this repository, please report it privately.

**Contact:** hire.credibly374@passinbox.com

Please include:

1. A short description of the issue and its impact.
2. Steps to reproduce (a minimal proof-of-concept is ideal).
3. Any suggested remediation, if you have one.

I aim to acknowledge reports within 3 business days and to provide a remediation
timeline within 10 business days. Please give me a reasonable window to ship a
fix before any public disclosure; coordinated disclosure is appreciated.

## Scope

In scope:

- The static site at `https://al-am.in/` and its subpaths.
- Supabase Edge Functions under this project (e.g. `hire-contact`).
- Data handling for the `photos` and `contact_requests` tables.

Out of scope:

- Issues that require a compromised end-user device or browser.
- Denial of service via volumetric traffic.
- Social engineering of the site owner.

## Safe harbor

Good-faith research that follows this policy will not trigger legal action.
