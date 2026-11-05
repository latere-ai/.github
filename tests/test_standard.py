"""Check standard/check.py: python3 -m unittest discover -s tests."""

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "standard"))

import check  # noqa: E402

README = """# Example

**Example is a server that does one thing.** It does it well enough to try.

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## Status

Version 0.1, see [the changelog](CHANGELOG.md#v010---2026-11-01).

## Quickstart

```sh
make build
```

## How it fits

```mermaid
flowchart LR
  a --> b
```

## Documentation

[Configuration](docs/configuration.md#settings)

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
"""

SECURITY = """# Security

## Reporting a vulnerability

Use https://github.com/latere-ai/example/security/advisories/new and
https://github.com/latere-ai/.github/blob/main/SECURITY.md.

## What is protected

## What is not defended

## Audit

## Supply chain
"""

CHANGELOG = """# Changelog

For whoever runs it.

## Unreleased

## v0.2.0 - 2026-11-03

### Added

- **A thing.**

### Fixed

- **Another.**

## v0.1.0 - 2026-11-01

### Added

- **The first release.**
"""

FILES = {
    "README.md": README,
    "LICENSE": "Apache License\n",
    "SECURITY.md": SECURITY,
    "CONTRIBUTING.md": "# Contributing\n\n## Getting set up\n\n## Sending a change\n",
    "CHANGELOG.md": CHANGELOG,
    ".github/ISSUE_TEMPLATE/bug_report.yml": "name: Bug report\n# See SECURITY.md\n",
    ".github/ISSUE_TEMPLATE/feature_request.yml": "name: Feature request\n",
    ".github/ISSUE_TEMPLATE/config.yml": "blank_issues_enabled: false\ncontact_links:\n  - url: https://github.com/latere-ai/example/blob/main/SECURITY.md\n",
    ".github/PULL_REQUEST_TEMPLATE.md": "## What this changes\n",
    "docs/README.md": "# Documentation\n",
    "docs/local.md": "# Running it locally\n",
    "docs/install.md": "# Install\n",
    "docs/configuration.md": "# Configuration\n\n## Settings\n",
    "docs/api.md": "# API\n",
    "docs/security.md": "# Security\n",
}


class Repo:
    """A checkout that meets the standard, in a temporary directory."""

    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "example"
        for rel, text in FILES.items():
            self.write(rel, text)
        shutil.copy(check.CONDUCT, self.root / "CODE_OF_CONDUCT.md")

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def check(self, kind="service", runner=None):
        return check.Check(self.root, "example", kind, runner=runner).run()

    def rules(self, **kw):
        return sorted({f.rule for f in self.check(**kw)})

    def close(self):
        shutil.rmtree(self.tmp)


class StandardTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)

    def test_a_repository_that_meets_the_standard_has_no_finding(self):
        self.assertEqual(self.repo.check(), [])

    def test_a_missing_file_is_a_finding(self):
        (self.repo.root / "SECURITY.md").unlink()
        (self.repo.root / "docs" / "api.md").unlink()
        self.repo.write("authorizer/doc.go", "package authorizer\n")
        found = {(f.path, f.rule) for f in self.repo.check()}
        self.assertIn(("SECURITY.md", "files"), found)
        self.assertIn(("docs/api.md", "docs"), found)
        self.assertIn(("docs/authorizer.md", "docs"), found)

    def test_the_readme_headings_are_in_order(self):
        text = README.replace("## Quickstart", "## Try it").replace("## Status", "## Quickstart")
        self.repo.write("README.md", text)
        messages = [f.message for f in self.repo.check() if f.rule == "readme"]
        self.assertTrue(any("no `## Status`" in m for m in messages), messages)

    def test_badges_come_after_the_paragraph(self):
        self.repo.write("README.md", README.replace("# Example\n\n", "# Example\n\n[![CI](x.svg)](y)\n\n", 1))
        self.assertIn("readme", self.repo.rules())

    def test_the_paragraph_opens_in_bold(self):
        self.repo.write("README.md", README.replace("**Example is a server that does one thing.**",
                                                    "Example is a server."))
        self.assertIn("readme", self.repo.rules())

    def test_a_content_repository_needs_fewer_headings(self):
        self.repo.write("README.md", "# Book\n\n**A book.**\n\n## Status\n\n## Contributing\n\n## License\n")
        self.assertNotIn("readme", self.repo.rules(kind="content"))
        self.assertNotIn("docs", self.repo.rules(kind="content"))

    def test_security_names_its_own_reporting_link(self):
        self.repo.write("SECURITY.md", SECURITY.replace("example/security", "other/security"))
        self.assertIn("security", self.repo.rules())

    def test_the_code_of_conduct_is_the_organizations(self):
        self.repo.write("CODE_OF_CONDUCT.md", "# Be nice\n")
        self.assertIn("conduct", self.repo.rules())

    def test_blank_issues_are_off(self):
        self.repo.write(".github/ISSUE_TEMPLATE/config.yml", "blank_issues_enabled: true\n")
        self.assertIn("templates", self.repo.rules())

    def test_the_changelog_is_ordered(self):
        self.repo.write("CHANGELOG.md", CHANGELOG.replace("## v0.2.0 - 2026-11-03", "## v0.0.9 - 2026-11-03"))
        self.assertIn("changelog", self.repo.rules())
        self.repo.write("CHANGELOG.md", CHANGELOG.replace("### Fixed\n\n- **Another.**\n", "")
                        .replace("### Added\n\n- **A thing.**\n", "### Fixed\n\n- **x**\n\n### Added\n\n- **y**\n"))
        self.assertIn("changelog", self.repo.rules())
        self.repo.write("CHANGELOG.md", CHANGELOG.replace("### Fixed", "### Bugs"))
        self.assertIn("changelog", self.repo.rules())

    def test_writing_rules(self):
        self.repo.write("docs/api.md", "# API\n\nIt waits — then answers.\n")
        self.assertEqual(self.repo.rules(), ["dashes"])
        self.repo.write("docs/api.md", "# API\n\nThe behaviour is to organise it.\n")
        found = [f for f in self.repo.check() if f.rule == "spelling"]
        self.assertEqual(len(found), 2)

    def test_code_is_not_prose(self):
        self.repo.write("docs/api.md", "# API\n\nThe status `cancelled` is a wire value.\n\n```\nbehaviour\n```\n")
        self.assertEqual(self.repo.check(), [])

    def test_a_box_drawing_is_not_a_diagram(self):
        self.repo.write("docs/api.md", "# API\n\n```\n┌──┐\n```\n")
        self.assertEqual(self.repo.rules(), ["diagrams"])

    def test_links_reach_a_file_and_a_heading(self):
        self.repo.write("docs/api.md", "# API\n\n[a](missing.md) [b](configuration.md#nothing) [c](#api)\n")
        found = [f.message for f in self.repo.check() if f.rule == "links"]
        self.assertEqual(len(found), 2, found)

    def test_a_link_to_this_repository_on_github_names_a_file_it_has(self):
        self.repo.write("docs/api.md", "# API\n\n[a](https://github.com/latere-ai/example/blob/main/nothing.md)\n")
        self.assertEqual(self.repo.rules(), ["links"])

    def test_the_slug_is_githubs(self):
        self.assertEqual(check.slug("v0.1.0 - 2026-11-01"), "v010---2026-11-01")
        self.assertEqual(check.slug("The `SERMO_*` settings"), "the-sermo_-settings")
        self.assertEqual(check.slug("What is protected?"), "what-is-protected")


def settings_runner(repo=None, pvr=True, packages=(), public=("example", ".github"), single=None):
    base = {
        "visibility": "public", "description": "A server that does one thing.",
        "topics": ["go", "server", "mls", "e2ee", "oidc"], "homepage": "",
        "has_issues": True, "has_wiki": False, "has_projects": False, "has_discussions": False,
        "security_and_analysis": {"secret_scanning": {"status": "enabled"},
                                  "secret_scanning_push_protection": {"status": "enabled"}},
    }
    base.update(repo or {})

    def run(args):
        if args[:2] == ["repo", "list"]:
            return "\n".join(public)
        path = args[1]
        if path == "repos/latere-ai/example":
            return json.dumps(base)
        if path.endswith("/private-vulnerability-reporting"):
            return json.dumps({"enabled": pvr})
        if path.startswith("orgs/latere-ai/packages?package_type=container"):
            return json.dumps(list(packages) if path.endswith("&page=1") else [])
        if path.startswith("orgs/latere-ai/packages/container/"):
            name = path.rsplit("/", 1)[1]
            if single and name in single:
                return json.dumps(single[name])
            raise RuntimeError("gh: Package not found. (HTTP 404)")
        if path.startswith("orgs/latere-ai/packages"):
            return "[]"
        raise RuntimeError(f"unexpected {args}")
    return run


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        # The homepage is fetched over the network; the tests leave it unset
        # and expect that one finding.
        self.base = ["no homepage; set the project's documentation"]

    def messages(self, **kw):
        return [f.message for f in self.repo.check(runner=settings_runner(**kw)) if f.rule == "settings"]

    def test_settings_that_meet_the_standard(self):
        self.assertEqual(self.messages(), self.base)

    def test_each_setting_is_read(self):
        got = self.messages(repo={
            "description": "Two sentences here. And another one", "topics": ["go"],
            "has_wiki": True, "has_projects": True,
            "security_and_analysis": {},
        }, pvr=False, packages=[{"name": "exampled", "visibility": "private",
                                 "repository": {"name": "example"}}])
        joined = "\n".join(got)
        for want in ("ending in a period", "more than one sentence", "1 topics", "wiki is on",
                     "projects are on", "secret scanning is off", "push protection is off",
                     "private vulnerability reporting is off", "exampled is private"):
            self.assertIn(want, joined)

    def test_a_named_package_the_list_leaves_out_is_read_on_its_own(self):
        runner = settings_runner(single={"exampled": {"name": "exampled", "visibility": "private"},
                                         "examplectl": {"name": "examplectl", "visibility": "public"}})
        found = check.Check(self.repo.root, "example", "service", runner=runner,
                            packages=["exampled", "examplectl", "gone"]).run()
        got = [f.message for f in found if f.rule == "settings"]
        self.assertIn("the container package exampled is private; its settings page is "
                      "https://github.com/orgs/latere-ai/packages/container/exampled/settings", got)
        self.assertFalse(any("examplectl" in m for m in got), got)
        self.assertTrue(any("cannot read orgs/latere-ai/packages/container/gone" in m for m in got), got)

    def test_a_package_in_the_list_is_not_read_twice(self):
        listed = [{"name": "exampled", "visibility": "private", "repository": {"name": "example"}}]
        found = check.Check(self.repo.root, "example", "service", runner=settings_runner(packages=listed),
                            packages=["exampled"]).run()
        self.assertEqual(sum("exampled is private" in f.message for f in found), 1)

    def test_a_link_to_a_private_repository_is_a_finding(self):
        self.repo.write("docs/api.md", "# API\n\n[x](https://github.com/latere-ai/secret)\n")
        found = [f for f in self.repo.check(runner=settings_runner()) if f.rule == "links"]
        self.assertEqual(len(found), 1)

    def test_every_public_repository_is_listed(self):
        found = check.check_listed({"example": {"kind": "service"}, "gone": {"kind": "tool"}},
                                   settings_runner(public=("example", "new")))
        self.assertEqual(sorted(f.message for f in found),
                         ["gone is listed and not public", "new is public and not listed"])


class RegistryTest(unittest.TestCase):
    def test_every_entry_has_a_kind_or_a_reason(self):
        for name, entry in check.load_registry().items():
            with self.subTest(name=name):
                self.assertTrue(entry.get("kind") in check.KINDS or entry.get("exempt"), entry)

    def test_the_standard_lists_every_rule_the_script_checks(self):
        text = (ROOT / "standard" / "README.md").read_text(encoding="utf-8")
        for rule in ("files", "readme", "docs", "security", "contributing", "conduct", "templates",
                     "changelog", "spelling", "dashes", "diagrams", "links", "settings", "listed"):
            self.assertIn(f"| `{rule}` |", text)

    def test_the_standard_meets_its_own_writing_rules(self):
        found = check.Check(ROOT, ".github", "organization").run()
        self.assertEqual([str(f) for f in found], [])

    def test_main_reports_and_exits(self):
        repo = Repo()
        self.addCleanup(repo.close)
        out = io.StringIO()
        with redirect_stdout(out):
            code = check.main([str(repo.root), "--kind", "service"])
        self.assertEqual((code, out.getvalue()), (0, ""))
        (repo.root / "LICENSE").unlink()
        with redirect_stdout(out):
            code = check.main([str(repo.root), "--kind", "service"])
        self.assertEqual(code, 1)
        self.assertIn("LICENSE:1: files: missing", out.getvalue())


if __name__ == "__main__":
    unittest.main()
