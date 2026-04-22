# MCP Trust Boundary Demo

## Project Context

## Executive Summary

This repository is a small, local-only educational demo that illustrates a specific security failure mode in MCP-style clients: the collapse of the trust boundary between configuration and execution authority.

In local `stdio` deployments, an MCP client starts a server as a subprocess. That makes server configuration operationally significant. A configuration object may appear to be routine metadata, yet in practice it can determine what the client executes on the local host.

This project exists to make that boundary visible. It does not claim a universal protocol exploit, a novel zero-day, or a product-specific vulnerability. It demonstrates a narrow architectural issue in a controlled setting and shows how basic launch policy controls materially reduce the risk.

## Why This Matters

Security concerns around MCP are already public and well understood at a high level. Official guidance discusses risks associated with local servers, including arbitrary code execution, local compromise, data exfiltration, and command obfuscation. The issue is especially relevant for `stdio` transport because the client is responsible for launching the server process.

That architecture is convenient, but it is also security-sensitive. Once a client treats configuration as input to process launch, the distinction between setup data and execution authority becomes thin. If configuration is imported, generated, or influenced by an untrusted party, that boundary can fail.

The broader ecosystem reflects the same concern. Current hardening work around MCP-style systems increasingly assumes stronger isolation for local server execution rather than direct, unconstrained command launch. This demo is useful because it turns an abstract warning into something concrete, reproducible, and easy to inspect.

## Background

The Model Context Protocol provides a standard way for LLM-powered clients to connect to external tools, resources, and prompts. MCP clients can communicate with servers over multiple transports, including local `stdio` and remote HTTP-based mechanisms. In the `stdio` model, the client launches the server locally and exchanges JSON-RPC messages over standard input and output.

That model is practical and often the fastest path to local tool integration. It also means the security posture depends heavily on what the client is willing to launch, how launch metadata is represented, and which safeguards are enforced before execution occurs.

## Problem Statement

This repository focuses on one narrow issue:

**config-driven process launch in MCP-style local clients**

The concern is not simply that the client uses subprocesses. The concern is that server configuration may be handled as ordinary setup data even though it effectively controls local code execution.

If a user imports configuration without understanding its consequences, or if a third party can influence that configuration, the client may grant execution authority through what appears to be harmless metadata. That is the trust-boundary collapse this project is designed to demonstrate.

## Scope of the Claim

This project makes a limited and defensible claim:

> In MCP-style local `stdio` setups, server configuration can function as authority to execute local code.

This repository does **not** claim that:

- MCP is inherently a universal remote code execution vulnerability
- every MCP client is vulnerable
- the protocol itself is the sole source of risk
- this demo represents a novel zero-day
- containerization alone fully solves MCP security

The point is narrower and more useful: some implementation patterns treat launch configuration too casually for the level of authority it carries.

## Threat Model

### Threat Actor

A malicious or weakly trusted party who can influence local MCP server setup, copied configuration, project templates, installation instructions, or launch metadata.

### Asset at Risk

The local machine running the MCP client, including developer workstations, test environments, CI-like systems, and agent sandboxes.

### Trust Boundary Failure

The client loads configuration that appears to represent tool setup, but the runtime interprets that configuration as permission to spawn or control a local process.

### Consequences

In the minimal case, the result is unintended local command execution. In realistic environments, that can lead to broader host access, credential exposure, misuse of downstream tools, or data loss, depending on the runtime privileges and surrounding environment.

## Why Agentic Systems Increase the Risk

This issue becomes more important as workflows become more automated.

When server onboarding, registration, tool selection, or execution is partially automated, there is less opportunity for a human to inspect what is being launched and why. In agentic systems, that matters. The more steps the system performs on behalf of the user, the more dangerous vague trust boundaries become.

This repository is not a full prompt-injection demonstration. It addresses a narrower issue. Still, it sits in the same class of problems: systems that combine untrusted input, automation, and powerful local tooling need explicit boundaries or they fail in predictable ways.

## What This Demo Should Show

The repository should present two paths.

### Unsafe Path

A minimal client reads local configuration and launches the configured process with little or no policy enforcement.

### Guarded Path

A minimal policy layer blocks or constrains the same launch using simple, understandable controls such as:

- command allowlists
- approved registry entries
- argument validation
- working-directory restrictions
- digest pinning or signature checks
- explicit user approval for high-risk launch types

The goal is not to build a complete security framework. The goal is to make the effect of basic controls obvious.

## Positioning

This repository should be positioned as:

**A local architecture demo showing how config-to-execution trust-boundary collapse can happen in MCP-style clients, along with a minimal policy gate that prevents it.**

It should **not** be positioned as:

- an exploit kit
- a product takedown
- a generalized MCP security platform
- a compliance solution
- a full ecosystem scanner

The tone should remain technical, precise, and restrained.

## Safety Constraints

This project should remain clearly within safe boundaries.

### Acceptable Demo Behavior

- local-only execution
- harmless payloads
- writing a marker file inside the repository
- printing a visible demo marker to standard output or standard error
- creating a benign artifact such as `artifacts/pwned.txt`

### Out of Scope

- remote exploitation
- persistence or stealth
- credential harvesting
- destructive actions
- data exfiltration
- product-specific weaponization
- abuse of real targets

The point is educational clarity, not operational capability.

## Why This Project Is Worth Building

There is already a healthy amount of discussion around MCP security. What is still missing in many cases is a clean, minimal artifact that isolates one concrete failure mode and explains it well.

This project is valuable because it is narrow. It should help a reader quickly understand:

- where execution authority enters the system
- why launch configuration is security-sensitive
- how the unsafe assumption fails
- how lightweight controls change the outcome

That kind of clarity is useful for engineers, researchers, and technical decision-makers because it separates one architectural issue from the broader pile of MCP-adjacent debates.

## Intended Audience

This repository is intended for:

- security researchers working on AI systems and tool runtimes
- engineers building MCP clients, agents, or local tool integrations
- infrastructure and platform teams evaluating trust boundaries in agentic workflows
- technically literate readers who want a concrete explanation of why local MCP execution deserves scrutiny

## Success Criteria

The project succeeds if a reader can inspect the repository and immediately understand four things:

1. why local `stdio` launch is security-sensitive
2. how configuration can become execution authority
3. why the problem becomes sharper in agentic systems
4. why straightforward launch controls materially improve the situation

If the reaction is, “I see the exact boundary now,” the repository has done its job.

## Suggested README Opening

Use language along these lines:

> This repository demonstrates a narrow but important security issue in MCP-style local `stdio` workflows: server configuration may appear to be ordinary metadata, but it can function as authority to execute local code. The demo includes an unsafe path, where configuration is trusted too broadly, and a guarded path, where simple policy checks block the same action. This is a local educational artifact, not an exploit kit and not a claim that every MCP client is vulnerable.

## Suggested External Message

For a short public description, keep it simple:

> Built a small local demo showing how MCP-style server config can collapse the boundary between setup data and execution authority. Unsafe path runs it. Guarded path blocks it.

## References

1. Model Context Protocol, "Transports"  
   https://modelcontextprotocol.io/specification/draft/basic/transports

2. Model Context Protocol, "Security Best Practices"  
   https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

3. GitHub, "MCP Gateway Specification"  
   https://github.com/github/gh-aw/blob/main/docs/src/content/docs/reference/mcp-gateway.md

4. Model Context Protocol, "Architecture Overview"  
   https://modelcontextprotocol.io/docs/learn/architecture

5. Simon Willison, "Model Context Protocol has prompt injection security implications"  
   https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
