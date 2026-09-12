# AICIS-control Credential Remediation

## Status

**OPEN — historical public credential exposure requires provider-side closure.**

On 12 September 2026, a repository review found hard-coded exchange API credentials in `aicis_trading.py` on the public default branch.

The current branch tip has been remediated by replacing hard-coded values with environment-variable loading and fail-closed behavior when credentials are absent.

## Important limitation

Removing credentials from the current branch tip does **not** revoke them and does **not** remove them from Git history, existing clones, caches or mirrors.

Any real credential that appeared in public repository history must therefore be treated as compromised until it has been rotated or revoked at the provider.

## Required closure steps

1. Inventory the exchange/provider credential classes that were historically committed without copying secret values into tickets, documentation or chat.
2. At each affected provider, revoke the historical key and create a new key only if the integration is still required.
3. Prefer read-only or least-privilege permissions unless trading permission is explicitly necessary.
4. Disable withdrawal permissions for automated trading credentials unless there is a separately reviewed requirement.
5. Restrict keys by IP/address where the provider supports it.
6. Store replacement credentials only in a dedicated secret manager, deployment secret store or local untracked environment variables.
7. Review the full repository history for additional plaintext credentials or secret-bearing configuration files.
8. Consider history rewriting only **after** provider-side revocation/rotation; history rewriting alone is not credential revocation.
9. Re-scan the current tree and repository history after remediation.
10. Record non-secret evidence of provider-side rotation/revocation and the completion date.

## Current code rule

`aicis_trading.py` now reads provider credentials through environment variables and skips exchanges whose required credentials are absent. No real credentials belong in source control.

## Portfolio implication

Until provider-side credential closure is evidenced, `AICIS-control` should remain classified as:

**LEGACY INDEPENDENT TRADING PROTOTYPE / SECURITY REMEDIATION OPEN / PRESERVE**

It must not be described as production-ready or used as evidence that the modern AICIS Divine Core security programme is complete.
