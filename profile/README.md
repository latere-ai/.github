# Latere

**Human intelligence in the loop.**

Latere builds applications and platform services for autonomous agents: software engineering and document work, on top of identity, a model gateway, sandboxes, storage, and orchestration.

*Latere* is Latin for "to be hidden." What is hidden is human intelligence. In increasingly autonomous systems, human judgment does not disappear. It recedes behind every layer of decision-making, invisible but indispensable. Latere exists to ensure that this hidden human intelligence remains present, remains effective, and is never engineered away.

Autonomous agents can now act across tools, models, data, and environments. The question is no longer whether they can move, but where judgment remains. Every system we ship follows one principle: the human stays in the loop. Work is visible. Authority is bounded. Output is reviewable. AI executes, humans decide.

## Products

Three applications you and your agents work in, on a platform of five shared services. Every product stands on its own. Pick the one that fits your problem, or combine them.

### Applications

**[Wallfacer](https://wf.latere.ai/)** is an AI engineering teammate that turns ideas into working software. Talk through a plan, watch it build, and stay in control at every step: chat for exploration, specs for design, tasks for parallel execution, and code for precise edits. [Open source](https://github.com/changkun/wallfacer), runs on your own machine, bring any LLM provider.

**[Lectio](https://lectio.latere.ai/)** turns any document into data. Submit almost any file, PDF, Word, spreadsheets, slides, images, or web pages, and get clean text or structured fields back, with every detail sourced to where it came from on the page. One request, predictable pricing, a full record.

**[ReplicHAI](https://replichai.latere.ai/)** audits whether a research paper actually reproduces. Give it a paper: it finds what the authors released, implements and re-runs the part a machine can run, records every decision the paper left unwritten, and returns a verdict you can take apart. What reproduced, what did not, and what could not be judged, component by component, published with the full transcript beside it. A study that needs human participants is never simulated. Finished audits are public in the [registry](https://replichai.latere.ai/registry).

### Platform

**[Identity](https://auth.latere.ai/)** is single sign-on for everything Latere. One account across every product, for people and agents alike, with access you grant or revoke from one place.

**[Topos](https://latere.ai/products/topos)** is managed runtime and orchestration for AI agents. Run Codex, Claude Code, or your own agents in the cloud with scoped access and enforced guardrails, full visibility into every action, and durable state to resume from. Its [Adversarial Review](https://latere.ai/products/adversarial-review) capability puts an independent critic on an agent's output before you see it, so only the disputes that survive reach a human.

**[Cella](https://latere.ai/products/cella)** provisions on-demand cloud sandboxes. One API call spins up an isolated environment for an agent or a quick experiment in seconds. Keep it as long as you need, tear it down when you are done.

**[Lux](https://latere.ai/products/lux)** is a single gateway to every major model provider. Reach OpenAI, Anthropic, Gemini, OpenRouter, and Ollama through one account, with per-key spend limits, secrets kept server-side, and an audit log of every request.

**[Drive](https://drive.latere.ai/)** is object storage for your files and everything agents produce. Your files stay yours and agents see only what you grant. Agent output is saved apart from your own work, versioned and reviewable. Share by link, with your team, or with no one.

Developer documentation for the platform lives at [platform.latere.ai](https://platform.latere.ai/).

## Open source

Build on the same pieces we build on.

| Project | What it is |
| --- | --- |
| [latere-cli](https://github.com/latere-ai/latere-cli) | One binary for Cella sandboxes, Lux model access, and adversarial code review. |
| [lux-python-sdk](https://github.com/latere-ai/lux-python-sdk) · [lux-typescript-sdk](https://github.com/latere-ai/lux-typescript-sdk) | Talk to every model Lux routes through one request, response, and stream shape. |
| [Topos Runtime](https://github.com/latere-ai/topos) | Embeddable Go runtime for multi-agent systems: sandboxed tools, sub-agents under attenuated permissions, deterministic traces. |
| [agent-skills](https://github.com/latere-ai/agent-skills) | Reusable workflows for coding agents. The same spec and release process in Claude Code or Codex. |
| [tgo](https://github.com/latere-ai/tgo) | Run open-weight LLMs from Go. No cgo, no Python, no vendor runtime. |
| [llmops](https://github.com/latere-ai/llmops) | Serve open-weight models on GPUs you control, from frozen weights to a health-checked OpenAI- and Anthropic-compatible endpoint. |
| [pay](https://github.com/latere-ai/pay) | Sell credit, hold a balance, and spend it, in Go: a processor-neutral payment port and a credit ledger. |
| [service-template](https://github.com/latere-ai/service-template) | Production template for a Go backend with a Bun + React frontend, tag-driven releases, and deploy evidence. |

**[AI as an Infrastructure](https://aaai.latere.ai/en/)** is our open book on inference, training, and evaluation, from engineering practice to theoretical foundations. Also in [中文](https://aaai.latere.ai/zh/).

## What we believe

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
- [Wallfacer](https://wf.latere.ai/) · [Lectio](https://lectio.latere.ai/) · [ReplicHAI](https://replichai.latere.ai/) · [Identity](https://auth.latere.ai/) · [Topos](https://latere.ai/products/topos) · [Cella](https://latere.ai/products/cella) · [Lux](https://latere.ai/products/lux) · [Drive](https://drive.latere.ai/)
- [Contact](mailto:contact@latere.ai) · [Security](https://github.com/latere-ai/.github/blob/main/SECURITY.md)
