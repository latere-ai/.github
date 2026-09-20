# Latere

**Human intelligence in the loop.**

Latere builds applications and platform services for autonomous agents: software engineering and document work, on top of identity, a model gateway, sandboxes, Git hosting, storage, and orchestration.

*Latere* is Latin for "to be hidden." What is hidden is human intelligence. In increasingly autonomous systems, human judgment does not disappear. It recedes behind every layer of decision-making, invisible but indispensable. Latere exists to ensure that this hidden human intelligence remains present, remains effective, and is never engineered away.

Autonomous agents can now act across tools, models, data, and environments. The question is no longer whether they can move, but where judgment remains. Every system we ship follows one principle: the human stays in the loop. Work is visible. Authority is bounded. Output is reviewable. AI executes, humans decide.

## Core Platform

One identity across five capabilities, each built on an open-source component.

**[Identity](https://auth.latere.ai)** provides single sign-on through OpenID Connect, with federated login, organizations, teams, and token issuance. It powers one account across every Latere product, for people and agents alike.

**[Agents](https://platform.latere.ai/console/agents)** runs and orchestrates AI agents with scoped access, visibility into every action, and durable state to resume from. To build multi-agent systems in your own Go application, check the open source core: [Topos](https://github.com/latere-ai/topos).

**[Models](https://platform.latere.ai/console/models)** puts one gateway in front of your model providers. Issue and revoke access without handing out provider keys, set spend limits, and track usage through one API. Check the open source core: [Lux](https://github.com/latere-ai/lux).

**[Environments](https://platform.latere.ai/console/environments)** manages environments for agents and workloads. Run commands, attach a terminal, move files in and out, and tear down an environment when you are done. Check the open source core: [Cella](https://github.com/latere-ai/cella).

**[Code](https://platform.latere.ai/console/code)** hosts Git repositories over HTTPS and SSH. Give each project, sandbox, or agent run its own Git remote, with S3 compatible storage as the source of truth. Check the open source core: [Origo](https://github.com/latere-ai/origo).

**[Storage](https://platform.latere.ai/console/storage)** keeps files and workspaces durable for people, agents, and sandboxes, with version history and permissioned sharing over S3 compatible storage and Postgres. Check the open source core: [Arca](https://github.com/latere-ai/arca).

Developer documentation for the platform lives at [platform.latere.ai](https://platform.latere.ai/).

## Inference

Open-source components for running models on compute you control.

**[llmops](https://github.com/latere-ai/llmops)** is the deployment and serving layer for open-weight models, from a single GPU host to a Kubernetes fleet. Freeze and verify model weights, start an inference engine, and expose OpenAI- and Anthropic-compatible endpoints with health checks. These endpoints can sit behind Lux for model routing and access control.

**[Forma](https://github.com/latere-ai/forma)** is an inference framework for running open-weight LLMs in Go. No cgo, no Python, no vendor runtime.

## Research

**[ReplicHAI](https://replichai.latere.ai/)** audits whether a research paper actually reproduces. Give it a paper: it finds what the authors released, implements and re-runs the work, records every decision the paper left unwritten, and returns a verdict you can take apart. What reproduced, what did not, and what could not be judged, component by component, published with the full transcript beside it. Finished audits are public in the [registry](https://replichai.latere.ai/registry).

## Applications

**[Wallfacer](https://wf.latere.ai/)** is an AI engineering teammate that turns ideas into working software. Talk through a plan, watch it build, and stay in control at every step: chat for exploration, specs for design, tasks for parallel execution, and code for precise edits. [Open source](https://github.com/changkun/wallfacer), runs on your own machine, bring any LLM provider.

**[Lectio](https://lectio.latere.ai/)** turns any document into data. Submit almost any file, PDF, Word, spreadsheets, slides, images, or web pages, and get clean text or structured fields back, with every detail sourced to where it came from on the page. One request, predictable pricing, a full record.

## More Open Source

Tools and libraries to build with the platform and beyond.

| Project | What it is |
| --- | --- |
| [latere-cli](https://github.com/latere-ai/latere-cli) | One binary for Cella sandboxes, Lux model access, and adversarial code review. |
| [agent-skills](https://github.com/latere-ai/agent-skills) | Reusable workflows for coding agents. The same spec and release process in Claude Code or Codex. |
| [pay](https://github.com/latere-ai/pay) | Sell credit, hold a balance, and spend it, in Go: a processor-neutral payment port and a credit ledger. |
| [service-template](https://github.com/latere-ai/service-template) | Production template for a Go backend with a Bun + React frontend, tag-driven releases, and deploy evidence. |

**[AI as an Infrastructure](https://aaai.latere.ai/en/)** is our open book on inference, training, and evaluation, from engineering practice to theoretical foundations. Also in [中文](https://aaai.latere.ai/zh/).

## What we Believe

- **Human judgment is irreplaceable.** AI can execute, even reason. But deciding what matters, what is worth doing, and what trade-offs are acceptable still requires a human in the loop.
- **Transparency over magic.** Every AI action should be visible, auditable, and reversible. AI that cannot be inspected cannot be trusted.
- **Autonomy is a spectrum.** Full AI autonomy and full manual control are both valid. Where to draw the line should always be a human decision.
- **Build for the long term.** AI capabilities will keep evolving, paradigms will keep shifting. But the principle that human judgment belongs in the loop will not.

## Security

Found a vulnerability in a Latere service or repository? Read the
[security policy](https://github.com/latere-ai/.github/blob/main/SECURITY.md)
and report it through GitHub private vulnerability reporting or to
[security@latere.ai](mailto:security@latere.ai). It covers scope, testing rules,
response times, and safe harbour for good-faith research.

## Links

- [latere.ai](https://latere.ai) · [Products](https://latere.ai/products) · [Developer docs](https://platform.latere.ai/) · [Blog](https://latere.ai/blog)
- [Wallfacer](https://wf.latere.ai/) · [Lectio](https://lectio.latere.ai/) · [ReplicHAI](https://replichai.latere.ai/)
- [Identity](https://auth.latere.ai) · [Agents](https://platform.latere.ai/console/agents) · [Models](https://platform.latere.ai/console/models) · [Environments](https://platform.latere.ai/console/environments) · [Code](https://platform.latere.ai/console/code) · [Storage](https://platform.latere.ai/console/storage)
- [Contact](mailto:contact@latere.ai) · [Security](https://github.com/latere-ai/.github/blob/main/SECURITY.md)
