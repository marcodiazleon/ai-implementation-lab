# AI Implementation Lab

**Marco Díaz de León · Forward Deployment / AI Implementation Strategy**

[Open the public preview](https://marcodiazleon.github.io/ai-implementation-lab/)

The current redesign makes **Session** a conversation workspace with provider, model, effort and agent controls. The public preview lets visitors explore the interface and create agent definitions; real API conversations require the local backend and the operator's own API key. Check the published revision: a branch change does not update Pages until merged.

I define the problem, choose the scope and coordinate delivery. This repository shows those decisions, requirements and verification records. Code was developed with AI assistance.

## Explore the application
1. **Session:** compose a message, choose OpenAI or Claude/Anthropic and a model, select compatible effort and an agent. Open connection settings within the conversation.
2. **Agents:** create, edit and export a text-only assistant.
3. **MCPs:** prepare client configurations; only the local Context7 adapter has an implemented connection.
4. **How it is built:** inspect components, decisions and the engineering method.
5. **Evidence:** follow requirements to cases, tests and recorded results.

The refund exercise and operation log are no longer part of the interface. Their code, CLI, fixtures and historical tests remain in the repository.

## Run locally for evaluation
Read the [evaluation-only license](LICENSE.md) first. Downloading and running a local copy is permitted solely to evaluate the demo. Source reuse, redistribution, modification and external code contributions require Marco's prior written authorization.
Requirements: Python 3.11+ and Git. Node is needed for Python/JavaScript parity tests. No third-party Python packages are required.

```sh
git clone https://github.com/marcodiazleon/ai-implementation-lab.git
cd ai-implementation-lab
python scripts/check_environment.py
python scripts/verify.py
python run.py serve
```

Open **http://127.0.0.1:8765**. In Session, choose connection settings and supply your own provider key with explicit consent. API usage may incur provider charges. ChatGPT/Claude subscriptions are separate from API credentials. Stop with Ctrl+C; use `--port 8766` if the port is occupied.

The public static build accepts no API keys. It is an interface preview, not a hosted inference service. Local keys/history stay in server memory; custom agent definitions persist in the ignored `.local` directory. Public definitions last only in the tab. MCP configuration export does not execute a server or grant tools to chat agents.

## Engineering and verification
[Active status](docs/project-status.json) selects S01 **1.0**. Start with [the adopted method](docs/sdd-adoption.md), then [specification](specs/001-support-demo/spec.md), [plan](specs/001-support-demo/plan.md), [tasks](specs/001-support-demo/tasks.md) and [acceptance cases](specs/001-support-demo/acceptance.csv).

`evidence/latest.json` records current automated source verification. Session browser checks are recorded separately in reports/CONTINUATION_REVIEW_2026-10-05.md; manual and live-provider cases retain their own states. Unit, integration, browser, live API and owner acceptance are separate results.

[Working method](docs/engineering-guide.md) · [Architecture](docs/architecture.md) · [Tools](docs/tools-and-capabilities.md) · [Limits](docs/capabilities.md) · [Security](SECURITY.md)

## Structure
| Location | Purpose |
|---|---|
| src/lab/ | Domain, HTTP, provider sessions, agents and MCP adapters |
| web/ | Session, agent builder, MCP configuration and evidence views |
| specs/ | Requirements, plans, tasks and acceptance matrices |
| tests/ and scripts/ | Behavior checks, static build and evidence generation |
| docs/ | Decisions, research, operating instructions and continuity |
| evidence/ and reports/ | Versioned observations and their interpretation |

## Debugging
- **Blank or outdated UI:** check the branch/commit and Pages deployment before comparing screenshots.
- **Server unavailable:** verify the printed address and selected port.
- **Provider connection rejected:** inspect the displayed error code, model access and consent. Keys stay out of reports.
- **Failing check:** preserve command, expected/observed behavior, source revision and environment; rerun after a bounded correction.
- **MCP configuration:** prepared JSON is not proof of a live connection.

[Operation and handoff](docs/operations.md) · [API guide](docs/OPENAI_API.md) · [Review and maintainer policy](CONTRIBUTING.md)

## Scope and contact
This is a demonstration for prospective employers and clients. It claims no production authentication, durable refund transactions, business outcomes or autonomous shell/file execution. Optional model calls are bounded text conversations.

The repository is public for inspection and bounded local evaluation under [LICENSE.md](LICENSE.md). No open-source reuse rights are granted. Public visibility does not permit source integration, redistribution or unauthorized changes to this repository or its application. GitHub platform viewing/forking rights still apply. Contact Marco through [GitHub](https://github.com/marcodiazleon).

Repository controls, remaining account-application audit and verification limits are recorded in [the security review](docs/repository-security.md). A policy is not a technical guarantee against malicious activity.

## Product documents

Project-specific package adapted from the owner's six structural references; canonical SDD and acceptance remain authoritative. Internal review, not owner acceptance.

- [Product Requirements Document](docs/product-documents/01_PRODUCT_REQUIREMENTS_DOCUMENT.md)
- [Technical Requirements Document](docs/product-documents/02_TECHNICAL_REQUIREMENTS_DOCUMENT.md)
- [App Flow](docs/product-documents/03_APP_FLOW.md)
- [Design Brief](docs/product-documents/04_DESIGN_BRIEF.md)
- [Backend Schema](docs/product-documents/05_BACKEND_SCHEMA.md)
- [Implementation Plan](docs/product-documents/06_IMPLEMENTATION_PLAN.md)
