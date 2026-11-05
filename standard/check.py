#!/usr/bin/env python3
"""Check a checkout of a public Latere repository against standard/README.md.

    python3 standard/check.py <checkout> [--name NAME] [--kind KIND] [--github]

Prints one line per finding, `path:line: rule: what is wrong`, and exits 1
when there is any, 2 on a usage error. With --github it also reads the
repository's settings, its packages and the organization's public
repositories through the `gh` command. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

HERE = Path(__file__).resolve().parent
ORG = "latere-ai"
REGISTRY = HERE / "repositories.json"
CONDUCT = HERE.parent / "CODE_OF_CONDUCT.md"
ORG_POLICY = f"https://github.com/{ORG}/.github/blob/main/SECURITY.md"

KINDS = ("service", "library", "tool", "content", "organization")

# The README's level-two headings, in order, by kind.
README_HEADINGS = {
    "service": ["Status", "Quickstart", "How it fits", "Documentation", "Contributing", "License"],
    "library": ["Status", "Quickstart", "How it fits", "Documentation", "Contributing", "License"],
    "tool": ["Status", "Quickstart", "How it fits", "Documentation", "Contributing", "License"],
    "content": ["Status", "Contributing", "License"],
}

SECURITY_HEADINGS = {
    "service": ["Reporting a vulnerability", "What is protected", "What is not defended", "Audit", "Supply chain"],
    "library": ["Reporting a vulnerability", "What is protected", "What is not defended", "Audit", "Supply chain"],
    "tool": ["Reporting a vulnerability", "What is protected", "What is not defended", "Audit", "Supply chain"],
    "content": ["Reporting a vulnerability"],
}

CONTRIBUTING_HEADINGS = ["Getting set up", "Sending a change"]

SERVICE_DOCS = ["README.md", "local.md", "install.md", "configuration.md", "api.md", "security.md"]

CHANGELOG_GROUPS = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]

TEMPLATES = [
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

# Directories whose files are not the repository's own writing.
SKIP_DIRS = {".git", ".worktrees", "node_modules", "vendor", "third_party", "testdata", "dist", "out"}

# British spellings, matched as whole words outside code. A stem takes the
# endings after it; a plain word matches as written.
BRITISH_STEMS = [
    "authoris", "capitalis", "categoris", "characteris", "customis", "deserialis", "finalis",
    "generalis", "initialis", "internationalis", "localis", "materialis", "maximis", "minimis",
    "normalis", "optimis", "organis", "prioritis", "realis", "recognis", "serialis",
    "specialis", "standardis", "summaris", "synchronis", "utilis", "visualis",
]
BRITISH_WORDS = [
    "analyse", "analysed", "analysing", "behaviour", "behaviours", "behavioural", "cancelled",
    "cancelling", "catalogue", "catalogues", "centre", "centres", "colour", "colours",
    "defence", "enrolment", "favour", "favourite", "fulfil", "fulfilment", "grey", "honour",
    "judgement", "labelled", "labelling", "labour", "licence", "licences", "metre", "modelled",
    "modelling", "neighbour", "offence", "programme", "programmes", "signalled", "signalling",
    "travelled", "travelling", "whilst",
]
BRITISH = re.compile(
    r"\b(?:(?:" + "|".join(BRITISH_STEMS) + r")(?:e|ed|es|ing|ation|ations|er|ers)"
    r"|" + "|".join(BRITISH_WORDS) + r")\b",
    re.IGNORECASE,
)

BOX = re.compile(r"[─-╿]|^\s*\+[-=]{3,}")
EM_DASH = "—"
LINK = re.compile(r"(!?)\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)")
HTML_ANCHOR = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"", re.IGNORECASE)
ORG_LINK = re.compile(rf"https://github\.com/{ORG}/([A-Za-z0-9._-]+)(?:/blob/main/([^#?\s)]+))?")
RELEASE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)(?:-[0-9A-Za-z.]+)? - (\d{4})-(\d{2})-(\d{2})$")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.message}"


# A runner calls `gh` with its arguments and answers its standard output; it
# raises RuntimeError when the call fails. Tests pass their own.
Runner = Callable[[list[str]], str]


def gh(args: list[str]) -> str:
    try:
        done = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise RuntimeError(f"gh {' '.join(args)}: {e}") from e
    if done.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}: {done.stderr.strip() or 'exit ' + str(done.returncode)}")
    return done.stdout


# Reading Markdown.


def prose_lines(text: str) -> list[tuple[int, str, bool]]:
    """Each line with its number and whether it sits inside a fenced code block."""
    out, fence = [], None
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker
                out.append((n, line, True))
                continue
            if marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
                out.append((n, line, True))
                continue
        out.append((n, line, fence is not None))
    return out


def without_code_spans(line: str) -> str:
    return re.sub(r"(`+)(.+?)\1", lambda m: " " * len(m.group(0)), line)


def headings(text: str, level: int) -> list[tuple[int, str]]:
    prefix = "#" * level + " "
    return [(n, line[len(prefix):].strip()) for n, line, code in prose_lines(text)
            if not code and line.startswith(prefix)]


def slug(heading: str) -> str:
    """The anchor GitHub gives a heading."""
    text = re.sub(r"<[^>]+>", "", heading)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in "-_" or cat[0] in "LN" or cat == "Mn":
            out.append(ch)
        elif ch == " ":
            out.append("-")
    return "".join(out)


def anchors(text: str) -> set[str]:
    seen: dict[str, int] = {}
    out = set()
    for n, line, code in prose_lines(text):
        if code:
            continue
        m = re.match(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            base = slug(m.group(2))
            count = seen.get(base, 0)
            seen[base] = count + 1
            out.add(base if count == 0 else f"{base}-{count}")
        for a in HTML_ANCHOR.findall(line):
            out.add(a)
    return out


def walk(root: Path, suffixes: tuple[str, ...]) -> Iterable[Path]:
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if p.is_file() and p.suffix in suffixes:
            yield p


# The checks. Each takes what it reads and returns findings.


class Check:
    def __init__(self, root: Path, name: str, kind: str, uses: Iterable[str] = (),
                 runner: Runner | None = None, packages: Iterable[str] = ()):
        self.root = root
        self.name = name
        self.kind = kind
        self.uses = set(uses)
        self.packages = list(packages)
        self.runner = runner
        self.found: list[Finding] = []

    def add(self, path: str, line: int, rule: str, message: str) -> None:
        self.found.append(Finding(path, line, rule, message))

    def read(self, rel: str) -> str | None:
        p = self.root / rel
        if not p.is_file():
            return None
        try:
            return p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            self.add(rel, 1, "files", f"cannot be read: {e}")
            return None

    def run(self) -> list[Finding]:
        if self.kind != "organization":
            self.files()
            self.readme()
            self.docs()
            self.security()
            self.contributing()
            self.conduct()
            self.templates()
            self.changelog()
        self.writing()
        if self.runner is not None:
            self.settings()
        return self.found

    def files(self) -> None:
        need = ["README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", *TEMPLATES]
        if self.kind != "content" or self.tags():
            need.append("CHANGELOG.md")
        for rel in need:
            if not (self.root / rel).is_file():
                self.add(rel, 1, "files", f"missing: a {self.kind} repository carries it")

    def readme(self) -> None:
        text = self.read("README.md")
        if text is None:
            return
        lines = prose_lines(text)
        first = next(((n, line) for n, line, _ in lines if line.strip()), None)
        if first is None or not first[1].startswith("# "):
            self.add("README.md", first[0] if first else 1, "readme", "the file starts with the title as `# Name`")
        else:
            para = next(((n, line) for n, line, code in lines if n > first[0] and line.strip()), None)
            if para is None or para[1].lstrip().startswith("#"):
                self.add("README.md", first[0], "readme", "one paragraph says what the project is before any heading")
            elif para[1].lstrip().startswith(("[![", "<img", "<p", "![")):
                self.add("README.md", para[0], "readme", "the paragraph comes before any badge or image")
            elif not para[1].lstrip().startswith("**"):
                self.add("README.md", para[0], "readme", "the paragraph's first sentence is in bold")
        want = README_HEADINGS[self.kind]
        have = headings(text, 2)
        names = [h for _, h in have]
        at = 0
        for h in want:
            if h not in names:
                self.add("README.md", 1, "readme", f"no `## {h}` heading")
                continue
            i = names.index(h)
            if i < at:
                self.add("README.md", have[i][0], "readme",
                         f"`## {h}` comes after the headings before it in the standard: {', '.join(want)}")
            at = max(at, i)

    def docs(self) -> None:
        if self.kind != "service":
            return
        need = list(SERVICE_DOCS)
        if (self.root / "authorizer").is_dir():
            need.append("authorizer.md")
        for page in need:
            if not (self.root / "docs" / page).is_file():
                self.add(f"docs/{page}", 1, "docs", "missing: every service has this page")

    def security(self) -> None:
        text = self.read("SECURITY.md")
        if text is None:
            return
        names = [h for _, h in headings(text, 2)]
        for h in SECURITY_HEADINGS[self.kind]:
            if h not in names:
                self.add("SECURITY.md", 1, "security", f"no `## {h}` section")
        report = f"https://github.com/{ORG}/{self.name}/security/advisories/new"
        if report not in text:
            self.add("SECURITY.md", 1, "security", f"the private reporting link is {report}")
        if ORG_POLICY not in text:
            self.add("SECURITY.md", 1, "security", f"links the organization's policy, {ORG_POLICY}")

    def contributing(self) -> None:
        text = self.read("CONTRIBUTING.md")
        if text is None:
            return
        names = [h for _, h in headings(text, 2)]
        for h in CONTRIBUTING_HEADINGS:
            if h not in names:
                self.add("CONTRIBUTING.md", 1, "contributing", f"no `## {h}` section")

    def conduct(self) -> None:
        p = self.root / "CODE_OF_CONDUCT.md"
        if not p.is_file():
            return
        if not CONDUCT.is_file():
            self.add("CODE_OF_CONDUCT.md", 1, "conduct", f"the canonical copy {CONDUCT} cannot be found")
            return
        if p.read_bytes() != CONDUCT.read_bytes():
            self.add("CODE_OF_CONDUCT.md", 1, "conduct",
                     f"differs from {ORG}/.github/CODE_OF_CONDUCT.md; copy it as it is")

    def templates(self) -> None:
        config = self.read(".github/ISSUE_TEMPLATE/config.yml")
        if config is not None:
            if not re.search(r"(?m)^blank_issues_enabled:\s*false\s*$", config):
                self.add(".github/ISSUE_TEMPLATE/config.yml", 1, "templates", "sets `blank_issues_enabled: false`")
            if "SECURITY.md" not in config and "/security/" not in config:
                self.add(".github/ISSUE_TEMPLATE/config.yml", 1, "templates", "links the security policy")
        bug = self.read(".github/ISSUE_TEMPLATE/bug_report.yml")
        if bug is not None and "SECURITY.md" not in bug:
            self.add(".github/ISSUE_TEMPLATE/bug_report.yml", 1, "templates",
                     "warns not to report a vulnerability as an issue, linking SECURITY.md")

    def tags(self) -> list[str]:
        if not (self.root / ".git").exists():
            return []
        try:
            done = subprocess.run(["git", "-C", str(self.root), "tag", "--list", "v*"],
                                  capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as e:
            self.add("CHANGELOG.md", 1, "changelog", f"cannot list the tags: {e}")
            return []
        if done.returncode != 0:
            self.add("CHANGELOG.md", 1, "changelog", f"cannot list the tags: {done.stderr.strip()}")
            return []
        return [t for t in done.stdout.split() if re.fullmatch(r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?", t)]

    def changelog(self) -> None:
        text = self.read("CHANGELOG.md")
        if text is None:
            return
        rel = "CHANGELOG.md"
        first = next((line for line in text.splitlines() if line.strip()), "")
        if first != "# Changelog":
            self.add(rel, 1, "changelog", "the file starts with `# Changelog`")
        sections = headings(text, 2)
        if not sections or sections[0][1] != "Unreleased":
            self.add(rel, sections[0][0] if sections else 1, "changelog", "`## Unreleased` is the first section")
        last: tuple[int, ...] | None = None
        seen = set()
        for n, h in sections:
            if h == "Unreleased":
                continue
            m = RELEASE.match(h)
            if not m:
                self.add(rel, n, "changelog", f"`## {h}` is not `## vX.Y.Z - YYYY-MM-DD`")
                continue
            version = tuple(int(x) for x in m.group(1, 2, 3))
            seen.add(h.split(" ", 1)[0])
            if last is not None and version >= last:
                self.add(rel, n, "changelog", f"`## {h}` is out of order: the newest release comes first")
            last = version
        # The groups inside each section, in Keep a Changelog's order.
        order, section_line = -1, 0
        for n, line, code in prose_lines(text):
            if code:
                continue
            if line.startswith("## "):
                order, section_line = -1, n
            elif line.startswith("### "):
                group = line[4:].strip()
                if group not in CHANGELOG_GROUPS:
                    self.add(rel, n, "changelog", f"`### {group}` is not one of {', '.join(CHANGELOG_GROUPS)}")
                    continue
                i = CHANGELOG_GROUPS.index(group)
                if i <= order:
                    self.add(rel, n, "changelog",
                             f"`### {group}` is out of order in the section at line {section_line}")
                order = i
        for tag in self.tags():
            if tag not in seen:
                self.add(rel, 1, "changelog", f"the tag {tag} has no section")

    def writing(self) -> None:
        public = self.public_repositories() if self.runner is not None else None
        for path in walk(self.root, (".md", ".yml", ".yaml")):
            rel = path.relative_to(self.root).as_posix()
            if path.suffix != ".md" and not rel.startswith(".github/ISSUE_TEMPLATE/"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                self.add(rel, 1, "files", f"cannot be read: {e}")
                continue
            markdown = path.suffix == ".md"
            for n, line, code in prose_lines(text) if markdown else [(i, l, False) for i, l in enumerate(text.splitlines(), 1)]:
                if EM_DASH in line:
                    self.add(rel, n, "dashes", "an em dash; use a period or a comma")
                if code:
                    if BOX.search(line):
                        self.add(rel, n, "diagrams", "a box drawn in characters; draw it in mermaid")
                    continue
                prose = without_code_spans(line)
                for m in BRITISH.finditer(prose):
                    if rel == "CODE_OF_CONDUCT.md":
                        break
                    self.add(rel, n, "spelling", f"`{m.group(0)}` is British spelling")
                if markdown:
                    self.links(path, rel, n, prose, public)

    def links(self, path: Path, rel: str, n: int, prose: str, public: set[str] | None) -> None:
        targets = [m.group(2) for m in LINK.finditer(prose)]
        d = REF_DEF.match(prose)
        if d:
            targets.append(d.group(1))
        for target in targets:
            org = ORG_LINK.match(target)
            if org:
                repo, inner = org.group(1), org.group(2)
                if repo.endswith(".git"):
                    repo = repo[:-4]
                if public is not None and repo not in public:
                    self.add(rel, n, "links", f"{target} is not a public repository of {ORG}")
                if repo == self.name and inner and not (self.root / inner).exists():
                    self.add(rel, n, "links", f"{target} names {inner}, which this checkout does not have")
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            file_part, _, anchor = target.partition("#")
            dest = path if not file_part else (path.parent / file_part)
            try:
                dest = dest.resolve()
                dest.relative_to(self.root.resolve())
            except (OSError, ValueError):
                self.add(rel, n, "links", f"{target} leaves the repository")
                continue
            if not dest.exists():
                self.add(rel, n, "links", f"{target} does not exist")
                continue
            if anchor and dest.is_file() and dest.suffix == ".md":
                if anchor not in anchors(dest.read_text(encoding="utf-8")):
                    self.add(rel, n, "links", f"{target}: no heading has the anchor #{anchor}")

    # Settings, through gh.

    def api(self, path: str) -> object | None:
        assert self.runner is not None
        try:
            return json.loads(self.runner(["api", path]))
        except (RuntimeError, json.JSONDecodeError) as e:
            self.add("(github)", 0, "settings", f"cannot read {path}: {e}")
            return None

    def public_repositories(self) -> set[str] | None:
        if not hasattr(self, "_public"):
            assert self.runner is not None
            try:
                out = self.runner(["repo", "list", ORG, "--visibility", "public", "--limit", "1000",
                                   "--json", "name", "--jq", ".[].name"])
                self._public: set[str] | None = set(out.split())
            except RuntimeError as e:
                self.add("(github)", 0, "listed", f"cannot list the public repositories: {e}")
                self._public = None
        return self._public

    def settings(self) -> None:
        where = "(github)"
        repo = self.api(f"repos/{ORG}/{self.name}")
        if not isinstance(repo, dict):
            return
        if repo.get("visibility") != "public":
            self.add(where, 0, "settings", f"the repository is {repo.get('visibility')}, not public")
        desc = (repo.get("description") or "").strip()
        if not desc:
            self.add(where, 0, "settings", "no description")
        else:
            if len(desc) > 120:
                self.add(where, 0, "settings", f"the description is {len(desc)} characters, over 120")
            if not desc.endswith("."):
                self.add(where, 0, "settings", "the description is one sentence ending in a period")
            if re.search(r"[.!?]\s+[A-Z]", desc):
                self.add(where, 0, "settings", "the description is more than one sentence")
            if EM_DASH in desc:
                self.add(where, 0, "settings", "the description has an em dash")
            for m in BRITISH.finditer(desc):
                self.add(where, 0, "settings", f"the description spells `{m.group(0)}` the British way")
        topics = repo.get("topics") or []
        if not 5 <= len(topics) <= 20:
            self.add(where, 0, "settings", f"{len(topics)} topics; the standard asks for 5 to 20")
        homepage = (repo.get("homepage") or "").strip()
        if not homepage:
            self.add(where, 0, "settings", "no homepage; set the project's documentation")
        else:
            status = fetch_status(homepage)
            if status is None or status >= 400:
                self.add(where, 0, "settings", f"the homepage {homepage} answers {status or 'nothing'}")
        if not repo.get("has_issues"):
            self.add(where, 0, "settings", "issues are off")
        if repo.get("has_wiki"):
            self.add(where, 0, "settings", "the wiki is on; documentation lives in docs/")
        if repo.get("has_projects") and "projects" not in self.uses:
            self.add(where, 0, "settings", "projects are on and repositories.json names none in use")
        if repo.get("has_discussions") and "discussions" not in self.uses:
            self.add(where, 0, "settings", "discussions are on and repositories.json names them as unused")
        analysis = repo.get("security_and_analysis") or {}
        for key, what in (("secret_scanning", "secret scanning"),
                          ("secret_scanning_push_protection", "push protection")):
            if (analysis.get(key) or {}).get("status") != "enabled":
                self.add(where, 0, "settings", f"{what} is off")
        pvr = self.api(f"repos/{ORG}/{self.name}/private-vulnerability-reporting")
        if isinstance(pvr, dict) and not pvr.get("enabled"):
            self.add(where, 0, "settings", "private vulnerability reporting is off")
        seen: set[str] = set()
        for ptype in ("container", "npm", "maven", "rubygems", "nuget"):
            for p in self.org_packages(ptype):
                if (p.get("repository") or {}).get("name") == self.name:
                    seen.add(f"{ptype}/{p.get('name')}")
                    self.package_visibility(ptype, p)
        # GitHub's list of the organization's packages can leave one out, so
        # the images repositories.json names are each read on their own.
        for name in self.packages:
            if f"container/{name}" in seen:
                continue
            p = self.api(f"orgs/{ORG}/packages/container/{name}")
            if isinstance(p, dict):
                self.package_visibility("container", p)

    def org_packages(self, ptype: str) -> list[dict]:
        out: list[dict] = []
        for page in range(1, 51):
            batch = self.api(f"orgs/{ORG}/packages?package_type={ptype}&per_page=100&page={page}")
            if not isinstance(batch, list):
                break
            out += batch
            if len(batch) < 100:
                break
        return out

    def package_visibility(self, ptype: str, p: dict) -> None:
        if p.get("visibility") != "public":
            self.add("(github)", 0, "settings",
                     f"the {ptype} package {p.get('name')} is {p.get('visibility')}; "
                     f"its settings page is https://github.com/orgs/{ORG}/packages/{ptype}/"
                     f"{p.get('name')}/settings")


def fetch_status(url: str) -> int | None:
    """The status a GET of url answers, following redirects; None when nothing answers."""
    req = urllib.request.Request(url, headers={"User-Agent": "latere-standard-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except (urllib.error.URLError, OSError, ValueError):
        return None


def load_registry(path: Path = REGISTRY) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["repositories"]


def check_listed(registry: dict[str, dict], runner: Runner) -> list[Finding]:
    try:
        out = runner(["repo", "list", ORG, "--visibility", "public", "--limit", "1000",
                      "--json", "name", "--jq", ".[].name"])
    except RuntimeError as e:
        return [Finding("standard/repositories.json", 1, "listed", f"cannot list the public repositories: {e}")]
    found = []
    for name in sorted(set(out.split()) - set(registry)):
        found.append(Finding("standard/repositories.json", 1, "listed", f"{name} is public and not listed"))
    for name in sorted(set(registry) - set(out.split())):
        found.append(Finding("standard/repositories.json", 1, "listed", f"{name} is listed and not public"))
    return found


def main(argv: list[str] | None = None, runner: Runner = gh) -> int:
    ap = argparse.ArgumentParser(description="Check a checkout against the public repository standard.")
    ap.add_argument("checkout", type=Path, help="the repository's working tree")
    ap.add_argument("--name", help="the repository's name on GitHub; the checkout's directory name by default")
    ap.add_argument("--kind", choices=KINDS, help="the kind; repositories.json by default")
    ap.add_argument("--github", action="store_true", help="also read the repository's settings through gh")
    args = ap.parse_args(argv)

    root = args.checkout.resolve()
    if not root.is_dir():
        print(f"check.py: {args.checkout} is not a directory", file=sys.stderr)
        return 2
    name = args.name or root.name
    registry = load_registry()
    entry = registry.get(name, {})
    found: list[Finding] = []
    if args.github:
        found += check_listed(registry, runner)
    if "exempt" in entry and not args.kind:
        print(f"{name}: exempt: {entry['exempt']}")
        for f in found:
            print(f)
        return 1 if found else 0
    kind = args.kind or entry.get("kind")
    if kind is None:
        print(f"check.py: {name} is not in {REGISTRY.name}; add it, or pass --kind", file=sys.stderr)
        return 2
    found += Check(root, name, kind, entry.get("uses", ()), runner if args.github else None,
                   entry.get("packages", ())).run()
    for f in found:
        print(f)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
