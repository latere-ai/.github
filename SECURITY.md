# Security policy

This policy covers the repositories in the [latere-ai](https://github.com/latere-ai)
organization and the services they run: latere.ai and its product subdomains.
GitHub applies it to every repository in the organization that does not publish
its own `SECURITY.md`; a repository with its own file overrides this one for
that repository.

Some Latere software is published outside this organization. Repositories under
a personal account, including
[changkun/wallfacer](https://github.com/changkun/wallfacer), do not inherit this
policy. Report an issue in one of those through the same contact below, and say
which repository you mean.

## Reporting a vulnerability

Report through **GitHub private vulnerability reporting** on the affected
repository, or by email to **security@latere.ai**.

Include what you have. The reports that get fixed fastest carry:

- The affected service or repository, and the version, commit, or date.
- What an attacker gains, in one sentence.
- The steps to reproduce, and the request or input that triggers it.
- Anything you already know about the scope: which accounts, which data.

Please do not open a public issue for an unfixed vulnerability, and do not
disclose it publicly before a fix ships.

## What happens next

| Stage | Target |
| --- | --- |
| Acknowledgement | 3 working days |
| Initial assessment and severity | 10 working days |
| Fix for a critical issue | 30 days, or a stated plan if it needs longer |
| Public disclosure | After the fix is released |

We will tell you what we found, what we changed, and when it shipped. We credit
reporters by name or handle unless you prefer otherwise.

## How we disclose

When a fix ships in a public repository, the tracking issue and the release note
describe the impact and the affected surface. They do not carry a working
exploit. A reporter who wants the full reproduction, and anyone who needs it to
verify their own deployment, receives it privately.

This is deliberate. A public repository's issue history is a search index, and a
complete exploit published there arms everyone still running the old version.

## Scope

In scope:

- The services on latere.ai and its product subdomains.
- Source code in this organization's repositories.
- Our published container images, packages, and their release artifacts.
- Authentication, authorization, tenancy, and data isolation between accounts
  and between organizations.
- Supply-chain issues in how we build and publish: a compromised pipeline
  identity, an unverified artifact, a dependency we introduced.

Out of scope:

- Findings from an automated scanner with no demonstrated impact.
- Missing hardening headers or a weak configuration with no exploit path. These
  are welcome as ordinary issues, not as vulnerability reports.
- Denial of service through volume, and any test that degrades service for other
  users.
- Social engineering of our people, and physical access.
- Vulnerabilities in a third-party service we consume. Report those to that
  vendor. Tell us as well if our configuration of it is what exposes you.

## Testing rules

Test against your own account and your own data. Do not access, modify, or
retain another user's data. If you reach data that is not yours, stop, and tell
us what you reached.

Do not run automated scanning that degrades the service for others. Rate-limit
yourself.

## Safe harbour

We will not pursue or support legal action against research that follows this
policy: testing in good faith, within the scope and the rules above, reported
promptly, and not disclosed publicly before a fix ships. If a third party brings
action against you for research that followed this policy, we will say that it
was authorized.

This is not a paid bounty programme. We do not currently pay for reports.

## Supported versions

Services on latere.ai run one production version, and that version is the
supported one. For a published library or image, the current major line receives
security fixes; earlier lines do not.
