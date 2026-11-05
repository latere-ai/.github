# The public repository standard

What every public repository under [github.com/latere-ai](https://github.com/latere-ai)
carries, and how each piece is written. It is for whoever maintains one of
them, a person or an agent. A repository either meets it or has an open
reason not to.

[`check.py`](check.py) checks a checkout and the repository's settings
against it:

```sh
python3 standard/check.py ../sermo --github
```

Everything the script can decide, it checks. What it cannot, such as
whether a quickstart works on a fresh machine or a sentence is written for
its reader, is listed under [Review](#review) and is checked by a person
before a change lands.

## Kinds

A repository is one of four kinds, and the kind decides which pieces it
carries. [`repositories.json`](repositories.json) names the kind of every
public repository; a public repository missing from it fails the check.

| Kind | What it is | Examples |
|---|---|---|
| `service` | a program someone runs as a server | sermo, pons, cella |
| `library` | a module other code imports | pkg, sdk-go, latere-ui |
| `tool` | a command, an image or a building block of continuous integration someone runs | latere-cli, ci-gate, sandbox-images |
| `content` | a book or a site someone reads | ai-as-an-infrastructure |

This repository is the one of kind `organization`: GitHub shows the
community files here on every repository of the organization that has
none, so it carries no project files of its own, and only the
[writing rules](#writing) apply to it. A maintained fork, which keeps its
upstream's files, and an archived repository are listed with the reason
the standard does not apply.

## What each repository carries

| Piece | service | library | tool | content |
|---|---|---|---|---|
| `README.md` in the order of [The README](#the-readme) | yes | yes | yes | yes |
| `LICENSE` | yes | yes | yes | yes |
| `CHANGELOG.md` in the form of [Releases](#releases) | yes | yes | yes | when it is tagged |
| `SECURITY.md` | yes | yes | yes | yes |
| `CONTRIBUTING.md` | yes | yes | yes | yes |
| `CODE_OF_CONDUCT.md`, identical to [this repository's](../CODE_OF_CONDUCT.md) | yes | yes | yes | yes |
| `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `feature_request.yml`, `config.yml` | yes | yes | yes | yes |
| `.github/PULL_REQUEST_TEMPLATE.md` | yes | yes | yes | yes |
| `docs/` with the [service set](#a-services-docs) | yes | | | |

Each repository carries its own copy of every community file, the code
of conduct included. GitHub falls back to this organization's files only
inside the organization, and a fork or a mirror loses them; a project
that someone else runs keeps its rules with its code.

## The README

The README is for someone who found the repository and is deciding
whether to use it. It answers, in this order, what the project is,
whether it is ready, how to try it, where it sits, and where to read
more. Its level-two headings are these, in this order. A repository adds
others between them where its reader needs one, such as an end-to-end
example.

1. **The title and one paragraph** before any heading: what the project
   is and does, in words a newcomer knows, with the first sentence in
   bold. Badges, if any, go after the paragraph, never before it.
2. **`## Status`**: how far along it is, said plainly. The latest
   release, whether its API may still change, what works today and what
   is designed and not yet built, as a table where there is more than a
   sentence to say. A project that protects anyone's data says here
   whether it has had an external security audit.
3. **`## Quickstart`**: the shortest path from a fresh machine to seeing
   it work, with every command, each block runnable in order in one
   shell. It names what to install first. A service starts its server
   and makes one real request; a library installs and runs a complete
   program. It is run as written before every change to it lands.
4. **`## How it fits`**: the pieces it works with, drawn as one
   [diagram](#diagrams), and what each is for: what a service calls and
   is called by, the client a library is for, the service a client
   library reaches.
5. **`## Documentation`**: a table of the documentation, one row per
   page or reference, each with what the reader finds there.
6. **`## Contributing`**: one paragraph linking `CONTRIBUTING.md` and
   `SECURITY.md`, saying not to report a vulnerability in an issue.
7. **`## License`**: the license by its SPDX identifier, linking
   `LICENSE`.

A `content` repository needs only the paragraph, Status, Contributing
and License.

## A service's docs

A service's `docs/` holds one page per question an operator or a builder
asks, written for that reader. The pages and their file names are fixed,
so a reader of one Latere service finds the same page in the next:

| Page | Reader | What it holds |
|---|---|---|
| `docs/README.md` | everyone | the index: one table per reader, each page with what it answers |
| `docs/local.md` | someone trying it | the server on one machine with every dependency it needs, from a clone, ending in requests that show it working |
| `docs/install.md` | an operator | the image and its signature, the database, keys, probes, upgrading, and what a production installation needs |
| `docs/configuration.md` | an operator | every setting the server reads: its name, its default, what it does, and what refuses a start, one table per area |
| `docs/api.md` | a builder | the concepts, the flows a client follows, the errors to branch on, the limits, and where the full reference is |
| `docs/security.md` | an operator and a builder | what the service guarantees, what it sees, what it does not defend, and what an operator must keep safe |
| `docs/authorizer.md` | someone writing an authorizer | the integration contract, when the service asks an endpoint for decisions: the question, the vocabulary, the answer, failing closed, and the default without one |

A service with another integration contract, such as a manifest or a
catalog format, gives it a page of its own beside these. A `library`
documents its API where its language's readers look for it, such as
pkg.go.dev, and its README links there. A `tool` documents every command
and setting in `docs/` or in its README.

Every number a reader acts on, such as a default, a limit or a timeout,
is stated on one page and linked from the others, so a change to it is
one edit.

## Security

`SECURITY.md` is for someone who found a vulnerability and for someone
deciding whether to trust the project. It has these sections:

- **`## Reporting a vulnerability`**: report through GitHub private
  vulnerability reporting, linked as
  `https://github.com/latere-ai/<repository>/security/advisories/new`,
  or by email to security@latere.ai; never in a public issue. It links
  the [organization's policy](../SECURITY.md) for the response times,
  disclosure and safe harbor rather than restating them, and names the
  release lines that receive fixes.
- **`## What is protected`**: who could attack and what the project
  commits to against each. Each commitment is held by a test in the
  repository; a control without a test is a claim, and no claim is
  listed.
- **`## What is not defended`**: what an attacker in each position can
  still do, and what the project leaves to whoever runs it. Silence reads
  as a guarantee, so a known limit is written down.
- **`## Audit`**: whether the code has had an external security audit,
  by whom and when, or that it has not. A project built on cryptography
  of its own says which parts of it are unaudited.
- **`## Supply chain`**: how a release is built and signed, and the
  commands that verify a downloaded release and image.

A `content` repository needs only the first section. A service's
`docs/security.md` says the same for the people who run and build on it,
and adds what the service can see: what it stores, what it logs, and the
metadata it needs to do its work.

## Contributing

`CONTRIBUTING.md` is for someone changing the project. It says how to get
a working checkout and run the full check (`## Getting set up`), how a
change is sent and what it must carry (`## Sending a change`), and where
code belongs. It holds the design rules that are not style, the ones a
reviewer refuses a change for. It points to `specs/` where the design
lives, and to `SECURITY.md` for vulnerabilities.

Contributions are accepted under the repository's license, as the
license itself provides. There is no contributor agreement and no
sign-off line.

## Issue and pull request templates

Issues are filed through forms, and a blank issue is not offered.
`config.yml` sets `blank_issues_enabled: false` and links the security
policy and the documentation, so a question the docs do not answer is
filed as a documentation bug.

- `bug_report.yml` asks for what happened, how to reproduce it, the
  version as the project reports it, and the project's own facts that
  decide a bug (for a service: the store, the authorizer, the logs). It
  opens with the warning not to report a vulnerability there.
- `feature_request.yml` asks for the problem before the solution, and
  for the workaround in use.
- `PULL_REQUEST_TEMPLATE.md` asks what changes for whoever runs or calls
  the project, and why, and lists the repository's own checks: the full
  check passes, a bug fix carries a failing test, the docs and the
  changelog follow the change, and each invariant `CONTRIBUTING.md`
  names.

## Diagrams

A diagram is mermaid in the Markdown file that explains it, so it renders
on GitHub and changes in the same commit as the text. One diagram shows
one mechanism: what a request passes through, how a record is vouched
for, what a release runs. A sentence before it says what it shows. Its
labels are the reader's words, the ones the page uses, not package or
function names, and it has at most a dozen nodes. A box drawing in
characters is never a diagram.

## Writing

Every file is written for one reader, and the register follows the
reader:
[the registers](https://github.com/latere-ai/pkg/blob/main/docs/writing/registers.md)
is the rule. On top of it, in every public file:

- American spelling: behavior, license, organization, catalog.
- No em dashes. A period or a comma does the work.
- No private reference: no private repository, internal hostname,
  internal spec number, tracker item or person's account. A link to
  another Latere repository goes to a public one.
- The project's public vocabulary, the words its API and its users use,
  never a working name.
- Plain, exact sentences: the mechanism, its values and its limits. No
  marketing, no claims about quality, and no promise the code does not
  keep.
- Every relative link resolves, to a file and to a heading.

## Releases

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and is written for whoever runs or calls the project, not for whoever
wrote the change. It opens with `# Changelog` and a sentence on who it is
for, keeps `## Unreleased` at the top, and has one section per release,
newest first, headed `## vX.Y.Z - YYYY-MM-DD`. Inside a section, the
groups are `### Added`, `### Changed`, `### Deprecated`, `### Removed`,
`### Fixed` and `### Security`, in that order and only those. An entry
says what is different for the reader, starting with a bold sentence, and
names the setting, route or command it concerns. A change that needs an
operator to act, such as a migration or a new required setting, says so
in its entry.

A tag without a section is refused, and the GitHub release carries the
section as its notes. Versions follow semantic versioning; before 1.0,
the Status section says what may still change.

## Repository settings

| Setting | Value |
|---|---|
| Description | one sentence of at most 120 characters, ending in a period: what the project is, in the words of the README's first sentence, distinct from every other repository's |
| Topics | 5 to 20: the language, the kind of software, the protocols and standards it implements, and the problem it solves |
| Homepage | the project's documentation: its page outside GitHub where one exists, or its `docs/` on GitHub |
| Private vulnerability reporting | on |
| Secret scanning and push protection | on |
| Issues | on |
| Wiki | off; documentation lives in `docs/`, under review with the code |
| Projects | off, unless `repositories.json` names the project board the repository uses |
| Discussions | off, unless `repositories.json` names them as used |
| Published packages and images | public, so the quickstart and the install page work without a sign-in |

## What lives in this repository

This repository, `latere-ai/.github`, holds what is the same for every
repository: the organization's [security policy](../SECURITY.md), the
canonical [code of conduct](../CODE_OF_CONDUCT.md) each repository
copies, this standard, its checker and the list of repositories. A
repository's own README, docs, security file, contribution guide,
templates and changelog live in that repository, because they describe
that project.

## Checking

`python3 standard/check.py <checkout>` reads a checkout. Its name is the
checkout's directory name unless `--name` gives another, and its kind
comes from `repositories.json` unless `--kind` gives one. With
`--github`, it also reads the repository's settings, its published
packages and the list of public repositories through the `gh` command,
which must be signed in. GitHub's list of the organization's packages can
leave one out, so a repository's entry in `repositories.json` names the
container images it publishes under `packages`, and each is read on its
own. It prints one line per finding, as `path:line: rule: what is wrong`,
and exits 1 when there is any.

What it checks, by rule:

| Rule | What it checks |
|---|---|
| `files` | the pieces the kind carries are present |
| `readme` | the title, the bold first sentence, and the level-two headings in order |
| `docs` | a service's docs pages are present |
| `security` | the sections, and the private reporting link for this repository |
| `contributing` | the two sections |
| `conduct` | the code of conduct is identical to this repository's |
| `templates` | the issue forms, `blank_issues_enabled: false`, a link to the security policy |
| `changelog` | the heading, `## Unreleased`, the release headings, their order, and the groups |
| `spelling` | British spellings from a list |
| `dashes` | no em dash |
| `diagrams` | no box drawing in a code block |
| `links` | relative links reach a file and a heading; with `--github`, links to latere-ai repositories reach public ones |
| `settings` | with `--github`, every row of [Repository settings](#repository-settings) |
| `listed` | with `--github`, every public repository is in `repositories.json` |

### Review

What a script cannot decide, a reviewer checks before a change lands:

- The quickstart and `docs/local.md` were run as written on a machine
  that had none of the project's state.
- Each sentence is written for the reader of its file.
- Every security commitment names the test that holds it, and every
  known limit is written down.
- Every setting, route and error the code has is in the docs, and
  nothing the docs describe is missing from the code.
