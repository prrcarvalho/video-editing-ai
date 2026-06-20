# video_editing_ai

video_editing_ai is an open-source repository for experimenting with AI-assisted
video analysis and recreation workflows. The goal is to build reusable tooling
that learns reusable structure from an Exemplar and applies it to generate a
Recreation.

## Status
This project is a personal/non-commercial open-source project maintained as a
solo, public repository. It is not a paid SaaS, client deliverable, or
commercial company product.

## Repository goals
- Curate an Asset Knowledge Base from owned footage and stock sources.
- Extract reusable `Viral Pattern` structure and production signals from Exemplar
  content.
- Assemble repeatable video pipelines that can generate Recreations safely and
  auditable.

## Project structure
- `scripts/` — utility scripts and orchestration helpers.
- `tools/` — external connectors and integrations.
- `docs/` — architecture references, execution handoffs, and operational playbooks.
- `exemplars/` — sample Exemplar intake, evidence bundles, and analysis outputs.
- `recreations/` — concrete Recreation projects from brief to render.
- `patterns/` — reusable, reviewed Viral Patterns.
- `assets/` — reusable shared assets and Asset Knowledge Base material.

## Quick start
```bash
# clone the repo
git clone https://github.com/prrcarvalho/video-editing-ai.git
cd video-editing-ai

# install and run project-specific tooling (add the commands relevant to your
environment)
# python: create/activate a virtualenv and install deps
# node: npm install
```

## Contributing
Contributions, issues, and suggestions are welcome.
See `CONTRIBUTING.md`.

## License
This project is licensed under the MIT License. See `LICENSE`.

## Security
Security guidance is in `SECURITY.md`.
