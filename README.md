# AICIS-control — Legacy Trading Prototype

> **Status: historical independent prototype / security remediation open.**

This repository is **not** the maintained AICIS Divine Core application and should not be treated as a control-plane component of the current AICIS product.

The maintained AICIS repository is:

**https://github.com/stanleymay20/aicis-divine-core-6d24171b**

## What this repository is

`AICIS-control` is an earlier Python/Firebase-era experimental system containing cryptocurrency/exchange automation and related frontend/function assets. Its Git history predates the modern TypeScript/Supabase AICIS Divine Core lineage and is not reachable from the maintained repository.

Because this repository represents a different technical era and problem domain, it should be retained as **legacy research/prototype evidence**, not merged into the current Divine Core codebase simply to reduce repository count.

## Security status

A repository review on 12 September 2026 found hard-coded exchange credentials in the public `aicis_trading.py` branch tip. The current file has been repaired to load credentials only from environment variables, but that does **not** make historically committed credentials safe.

Any real credential that appeared in public Git history must be treated as exposed and rotated or revoked at the relevant provider.

See [SECURITY_REMEDIATION.md](SECURITY_REMEDIATION.md) for the closure requirements. Do not use this repository for live trading or production credentials until those requirements are completed.

## Development rule

Do not add new AICIS Divine Core product development here. New resilience, forecasting, world-model, evidence-fabric, authentication, governance and decision-support work belongs in `aicis-divine-core-6d24171b` unless a controlled handoff explicitly states otherwise.
