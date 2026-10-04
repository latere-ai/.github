# Latere

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/latere-ai/.github/main/profile/assets/teaser-dark.png">
  <img src="https://raw.githubusercontent.com/latere-ai/.github/main/profile/assets/teaser-light.png" alt="Latere: Trustworthy Superintelligence. Latere builds autonomous agents you can hand real work to, from a published website to a checked paper. They act within your rules and record every step." width="100%">
</picture>

Latere builds trustworthy superintelligence: proactive, autonomous agents that take initiative and carry real work forward in the background. They ship as applications, and as a platform built on open source cores you can run yourself.

*Latere* is Latin for "to be hidden." What is hidden is human intelligence. In increasingly autonomous systems, human judgment does not disappear. It recedes behind every layer of decision-making, invisible but indispensable. Latere exists to ensure that this hidden human intelligence remains present, remains effective, and is never engineered away, so that superintelligence stays trustworthy and people stay in control.

AI can now do real work: run a workflow from start to finish, turn an idea into a working product, build and ship software. As it grows more capable than the people it works for, the question that matters is whether it can be trusted. Every system we ship follows one principle: the human stays in the loop. Agents act within the rules people set, record every step, and seek human judgment when it matters.

## Core Platform

One sign-in, one console, and one API address across every capability. Each capability except Apps is built on an open source core you can run yourself.

**[Identity](https://auth.latere.ai)** is the sign-in and access every capability below shares: single sign-on through OpenID Connect, with federated login, organizations, teams, and token issuance. One account covers every Latere product, for people and agents alike.

**[Agents](https://platform.latere.ai/console/agents)** runs hosted agents: versioned agent definitions and the sessions people have with them, each in a sandbox of its own with every step in its log. A session survives the process that runs it and waits for a person where it should. Check the open source core: [Topos](https://github.com/latere-ai/topos).

**[Models](https://platform.latere.ai/console/models)** puts one gateway in front of your model providers. Issue and revoke access without handing out provider keys, set spend limits, and track usage through one API. Check the open source core: [Lux](https://github.com/latere-ai/lux).

**[Environments](https://platform.latere.ai/console/environments)** runs isolated workloads for agents and applications. Run commands, attach a terminal, and move files in and out, with credentials swapped in at egress so they never enter the workload. Check the open source core: [Cella](https://github.com/latere-ai/cella).

**[Repos](https://platform.latere.ai/console/repos)** hosts Git repositories over HTTPS and SSH. Give each project, sandbox, or agent run its own Git remote, with S3 compatible storage as the source of truth. Check the open source core: [Origo](https://github.com/latere-ai/origo), and [origo-web](https://github.com/latere-ai/origo-web) for browsing its repositories.

**[Storage](https://platform.latere.ai/console/storage)** keeps files and workspaces durable for people, agents, and sandboxes, with version history and permissioned sharing over S3 compatible storage and Postgres. Check the open source core: [Arca](https://github.com/latere-ai/arca).

**[Apps](https://platform.latere.ai/console/apps)** hosts web applications from a repository. Every push builds a preview, a version tag releases it, and each app answers at its own address. The contract its clients share is public in [apps](https://github.com/latere-ai/apps).

**[Parsing](https://platform.latere.ai/docs/parsing)** turns a file into pages, blocks, tables, and the fields of a schema you supply, each tied to its place on the page. Check the open source core: [Lectio](https://github.com/latere-ai/lectio).

Developer documentation for the platform lives at [platform.latere.ai](https://platform.latere.ai/).

## Inference

Two capabilities for running models on compute you control, each built on an open source core.

**Model Serving** deploys and operates open-weight models, from a single GPU host to a Kubernetes fleet. Freeze and verify model weights, start an inference engine, and expose OpenAI- and Anthropic-compatible endpoints with health checks. These endpoints can sit behind Lux for model routing and access control. Check the open source core: [Fornax](https://github.com/latere-ai/fornax).

**Model Execution** runs open-weight LLMs in pure Go, with no Python or vendor runtime. Check the open source core: [Forma](https://github.com/latere-ai/forma).

## Research

**[ReplicHAI](https://replichai.latere.ai/)** audits whether a research paper actually reproduces. Give it a paper: it finds what the authors released, implements and re-runs the work, records every decision the paper left unwritten, and returns a verdict you can take apart. What reproduced, what did not, and what could not be judged, component by component, published with the full transcript beside it. Finished audits are public in the [registry](https://replichai.latere.ai/registry).

## Applications

**[Wallfacer](https://wf.latere.ai/)** is an AI engineering teammate that turns ideas into working software. Talk through a plan, watch it build, and stay in control at every step: chat for exploration, specs for design, tasks for parallel execution, and code for precise edits. [Open source](https://github.com/changkun/wallfacer), runs on your own machine, bring any LLM provider.

## More Open Source

Tools and libraries to build with the platform and beyond.

| Project | What it is |
| --- | --- |
| [latere-cli](https://github.com/latere-ai/latere-cli) | One binary for the platform: environments, apps deployed with a git push, model access, agent sessions, repositories, and adversarial code review. |
| [agon](https://github.com/latere-ai/agon) | Adversarial review of an agent's change: independent critics cross-examine a diff, and a contention score decides the outcome. |
| [agent-skills](https://github.com/latere-ai/agent-skills) | Reusable workflows for coding agents. The same spec and release process in Claude Code or Codex. |
| [sandbox-images](https://github.com/latere-ai/sandbox-images) | Container images that run coding agents and computer-use sessions, under Cella or standalone with Docker or Podman. |
| [latere-ui](https://github.com/latere-ai/latere-ui) | Glass materials, interface components, and application chrome for Vue and React, in light and dark. |
| [pkg](https://github.com/latere-ai/pkg) | Shared Go packages behind Latere services: auth, telemetry, LLM dialect translation, storage clients, and utilities. |
| [pay](https://github.com/latere-ai/pay) | Sell credit, hold a balance, and spend it, in Go: a processor-neutral payment port and a credit ledger. |
| [service-template](https://github.com/latere-ai/service-template) | Template for production Go services, with an optional React frontend, tag-driven releases, and drift checks. |
| [ci-gate](https://github.com/latere-ai/ci-gate) | `lateregate`, one quality gate for Go repositories that runs the same way in hooks, locally, and in CI. |
| [ci](https://github.com/latere-ai/ci) | Reusable GitHub Actions workflows: the per-push gate and tag-driven releases. |
| [minio](https://github.com/latere-ai/minio), [mc](https://github.com/latere-ai/mc) | Maintained forks of the archived MinIO community edition and its client, kept current on dependencies and security fixes. |

**[AI as an Infrastructure](https://aaai.latere.ai/en/)** is our open book on AI as an infrastructure, from systems to agents: history, design decisions, and foundations, written for software engineers new to machine learning. Also in [中文](https://aaai.latere.ai/zh/).

## What We Believe

- **Human judgment is irreplaceable.** AI can execute, even reason. But deciding what matters, what is worth doing, and what trade-offs are acceptable still requires a human in the loop.
- **Transparency over magic.** People should be able to understand what an agent is doing and why. Progress, decisions, and results should be inspectable, with opportunities to intervene and correct course.
- **Autonomy is a spectrum.** Full AI autonomy and full manual control are both valid. Where to draw the line should always be a human decision.
- **Build for the long term.** AI capabilities will keep evolving, paradigms will keep shifting. But the principle that human judgment belongs in the loop will not. We build for that to remain true.

## Security

Found a vulnerability in a Latere service or repository? Read the
[security policy](https://github.com/latere-ai/.github/blob/main/SECURITY.md)
and report it through GitHub private vulnerability reporting or to
[security@latere.ai](mailto:security@latere.ai). It covers scope, testing rules,
response times, and safe harbor for good-faith research.

## Links

[latere.ai](https://latere.ai) · [Docs](https://platform.latere.ai/) · [Open Source](https://latere.ai/open-source) · [Blog](https://latere.ai/blog) · [Contact](mailto:contact@latere.ai)
