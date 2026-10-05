# Repository integrity and evaluation review

2026-10-05. Authority U13; requirements R08/R11/R12/R14; tasks T44/T45. Reviewed by the implementing assistant, not an independent security assessor.

## Source policy
[LICENSE.md](../LICENSE.md) permits source inspection and the copies necessary for local evaluation with Python. It reserves source modification, redistribution, incorporation and commercial service use. [CONTRIBUTING.md](../CONTRIBUTING.md) accepts non-sensitive descriptive feedback, not external code contributions. GitHub viewing/forking rights and technically possible downloads remain platform limits. These notices cannot prevent copying technically.

## Observed boundaries
The inspected HTTP server binds 127.0.0.1 and checks Host/Origin before request routing. The published build is static; no shared source-upload or inference backend is supplied. Agent definitions are bounded local evaluation state, not repository source changes. No new execution tool is granted. A different local process can call the local server: this is not authenticated multiuser isolation.

The new verification workflow uses a read-only contents token and non-persistent checkout credentials. Its job runs only for the canonical repository and for same-repository PRs/pushes. This workflow condition is supplemental: untrusted code could alter a proposed workflow, so administrative fork-workflow approval settings still require review.
Pages is restricted to canonical main. A build job verifies the project and uploads a static artifact with read-only permissions. Only a separate deploy job, dependent on successful build, has Pages/OIDC permissions. It does not check out or run project code. The amended Pages deployment has not been executed before merge.
CODEOWNERS assigns review routing to Marco; it does not itself prevent writes or require approval.

## Administrative settings: BLOCKED by identity confirmation
The GitHub Branches screen showed no classic branch protections configured. Prepared a rule for main: PR required; verify (ubuntu-latest) and verify (windows-latest) from GitHub Actions required; up-to-date base and conversation resolution required; admin bypass disabled; force pushes/deletion disabled. Create led to GitHub Confirm access. The rule is not confirmed saved or active.
Collaborator access inspection also led to Confirm access. Collaborator permissions, rulesets, Actions approval for all external contributors, default token permissions and deployment-environment restrictions are NOT VERIFIED. No collaborator was removed or access broadened.
No mandatory second-reviewer approval is requested for the sole maintainer; this does not replace Marco's manual diff review. Existing owner PR-opening decision D20 is retained. Main and existing PR #4 were not modified by this increment.

## Checks and next action
C144: policy/document consistency review. C145: administrative protection/save, blocked by identity confirmation. C146: revised workflows and CI, pending this source revision. Prior 101-test results on 00d827b cover that earlier revision only.
The local execution tool could not start; no local PASS is claimed. Use branch CI to verify SDD, tests and static build. No live API, hostile payload execution, external workflow approval, merge or deployment has been performed.
Marco completes GitHub identity confirmation; maintainer then verifies saved main protection, collaborator list and external-workflow approvals before declaring repository hardening complete. Preserve source history and update this record with actual evidence. Passing tests does not certify the absence of malicious code.

Sources: [GitHub licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use).
