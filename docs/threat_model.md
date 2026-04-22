# Threat Model

## Claim

In MCP-style local `stdio` clients, server configuration can function as authority to execute local code.

## Threat Actor

A malicious or weakly trusted party who can influence local server config, copied setup snippets, templates, or onboarding instructions.

## Trust Boundary Failure

The client treats launch metadata as ordinary configuration, then uses it to start a local process. The boundary fails when input that should be reviewed as authority is accepted as setup data.

## Assets at Risk

- developer workstations
- test environments
- CI-like runners
- agent hosts
- local secrets and files reachable by the launched process

## Safety Constraints

This demo stays local-only. Payloads may print markers or write benign files under `artifacts/`, but they must not persist, exfiltrate data, or modify the host outside the repository.
