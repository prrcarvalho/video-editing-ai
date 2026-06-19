# FlowKit is an independently versioned Generation Connector submodule

FlowKit should live under `tools/flowkit` as a Git submodule pointing at the reusable `prrcarvalho/flowkit` fork. The main `video_editing_ai` repo tracks the approved FlowKit commit for the Recreation pipeline, while FlowKit keeps its own branches, commits, releases, and use in other projects.

Omni mapping artifacts should live inside the FlowKit submodule, not the parent repo: `tools/flowkit/research/omni/`. The parent repo can keep high-level orchestration plans, but sanitized captures, schemas, fixtures, contract tests, and FlowKit gap matrices are part of FlowKit's reusable connector evidence.

## Considered Options

- **Submodule:** preserves FlowKit as an independent reusable project while letting this repo pin an exact connector version.
- **Vendored copy:** simpler day to day, but mixes FlowKit history into the video workspace and makes reuse harder.
- **Subtree:** keeps one checkout but blurs ownership more than needed for a connector that should evolve independently.
