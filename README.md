# AI Implementation Lab

**Marco Díaz de León · AI implementation strategy**

I turn an AI idea into a bounded first version: I define the problem and the scope, set the acceptance criteria, coordinate the build and verify the result. This repository is a small working lab that shows that method on a fictional case.

The code was written with AI assistance. The problem definition, scope, acceptance criteria and verification are my work.

**First action: [open the public demo](https://marcodiazleon.github.io/ai-implementation-lab/)** and press *Start the three-minute tour*. No account, key or model is needed.

![Session in the public demo: presentation, three-step orientation and composer](docs/assets/presentation-20261011.jpg)

Screenshot from the public build of the revision that added it, served locally.

## Three routes

- **30 seconds.** Read the presentation at the top of Session: who I am, what I contribute, what is pending.
- **3 minutes.** Follow the tour in *How it is built*. Each step names what you do, the expected result and the control it demonstrates, with a link to its evidence.
- **Technical review.** Start at the [documentation index](docs/INDEX.md): specification, architecture, decisions, tests, evidence, the [requirement matrix](docs/requirements-matrix.md) and one requirement traced from need to evidence.

## What the lab demonstrates

- **Controls before effects.** In a fictional refund case, a simulated proposal cannot execute until a person approves it. A simulated failure creates no receipt, a retry creates exactly one, and repeating returns the same receipt.
- **Traceability.** Every requirement links to tasks, acceptance cases, tests and recorded evidence. A requirement is PASS only when all its applicable cases passed; otherwise partial, pending, blocked or failed.
- **Honest records.** Automated verification, independent review, owner acceptance, integration and deployment are recorded separately; none is implied by another.
- **Bounded AI connections.** The local lab converses with OpenAI or Anthropic with your own key and consent. Agents are text-only; the MCP adapter is read-only.

## Public demo, local lab and pending

| | Public demo | Local lab |
|---|---|---|
| Needs | A browser | Python 3.11+ and Git; your own API key only for conversations |
| Session | Presentation, model catalog and agent drafts; no model replies | Conversation with your own provider key |
| Refund case | Described in the tour; not run in the interface by the owner's decision (U13) | `python run.py tour` and the test suite |
| Evidence | Committed run, cases and project records | The same, plus `python scripts/verify.py` |

Pending: a new-visitor test, a recorded live provider call, an owner decision on a visible refund route, and the reconciliation of pull requests #4 to #6 ([capabilities.md](docs/capabilities.md)). What was verified, reviewed, accepted, integrated and published, revision by revision: the Evidence view and [project-status.json](docs/project-status.json).

## Published or candidate

The public URL serves main at the revision recorded under `deployment` in `docs/project-status.json`. Every build's Evidence view says whether it has the same content as the published and the accepted revisions; a branch never borrows the status of main. To review an unpublished candidate, fetch its branch and compare the commit with the SHA in its pull request:

```sh
git fetch origin <branch>
git checkout --detach FETCH_HEAD
git rev-parse HEAD        # must equal the reported SHA; otherwise: git checkout --detach <reported SHA>
python scripts/check_evidence.py
python run.py serve
```

## Run locally

```sh
git clone https://github.com/marcodiazleon/ai-implementation-lab.git
cd ai-implementation-lab
python scripts/check_environment.py
python run.py tour
python scripts/verify.py
python run.py serve
```

Open http://127.0.0.1:8765. Node is needed only for browser parity tests.

## Troubleshooting

- `python --version` must show Python 3.11 or later; on Windows use `py -3` if `python` opens the Store.
- Port 8765 busy: `python run.py serve --port 8766`.
- `scripts/verify.py` rewrites four generated files; to discard only those: `git checkout -- evidence/latest.json evidence/sdd-check.json specs/001-support-demo/acceptance.csv docs/requirements-matrix.md` (never reset the whole tree).
- A console that cannot encode a character (ASCII code pages; cp1252 does print Spanish accents) shows `?` instead; `python -X utf8 run.py tour` prints everything.

## Limits

Fictional data and simulated effects only: no real customers, refunds, integrations or commercial results. The reviewer role has no real authentication; state lives in memory. [Security boundaries](SECURITY.md), [threat model and control catalog](docs/threat-model.md), [supply chain](docs/supply-chain.md).

## Reuse and contact

Public for inspection; no open-source license is granted in this version. To discuss an implementation, contact Marco through [his GitHub profile](https://github.com/marcodiazleon).

---

## En español

Convierto una idea de IA en una primera versión acotada: defino el problema y el alcance, fijo los criterios de aceptación, coordino la construcción y verifico el resultado. El código se escribió con asistencia de IA; las decisiones, el alcance y la verificación son trabajo mío.

Primera acción: abre la demo pública y pulsa *Empezar el recorrido de 3 minutos*. La URL pública sirve main en la revisión que registra project-status.json; en Evidencia ves si la versión que miras es la publicada y la aceptada. Para revisar un candidato no publicado, sigue *Published or candidate*. En 30 segundos lees la presentación de Sesión; en 3 minutos sigues el recorrido de *Cómo está construido*; para la revisión técnica, empieza en el índice de documentación. La [guía en español](docs/START_HERE_ES.md) explica la instalación local.
