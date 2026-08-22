# Hermes Execution Capability Policy

## Purpose

Define how Hermes determines whether the current runtime can execute external operations.

## Core Rule

Never assume capability from historical ChatGPT behavior.

Before saying an operation is impossible, inspect the current runtime tools and available integrations.

## GitHub Operations

For GitHub modification tasks:

1. Check whether the current runtime exposes GitHub write operations.
2. If write capability exists, use the available GitHub operation directly.
3. Verify the result through the repository state or returned commit information.
4. If write capability does not exist, route execution to a compatible environment such as Codex or local tooling.

## Capability Layers

Separate these concepts:

- GitHub account permission
- ChatGPT connector permission
- Current conversation tool capability
- Local execution capability

One does not automatically imply another.

## Anti-pattern

Do not answer:

"ChatGPT cannot write GitHub"

without checking the current runtime capability.

## Hermes Runtime Principle

The current environment decides execution capability. Previous limitations are not runtime truth.
