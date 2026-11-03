"""Check the public profile's capability links and teaser: python3 -m unittest discover -s tests."""

from pathlib import Path
import re
import struct
import unittest
import zlib


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile" / "README.md"
ASSETS = ROOT / "profile" / "assets"
TEASER = ASSETS / "teaser" / "teaser.html"
# The profile is shown outside this repository, so its images are absolute.
RAW = "https://raw.githubusercontent.com/latere-ai/.github/main/"
# The platform's capabilities as the profile lists them. Each has a section
# of its own in the console, which its name links.
CAPABILITIES = (
    "Agents", "Oversight", "Models", "Environments", "Connections",
    "Repos", "Storage", "Apps", "Parsing", "Evals",
)


def section(heading):
    """The text under a level-two heading of the profile, up to the next one."""
    return PROFILE.read_text().split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]


def left_columns(path, columns):
    """Size of an 8-bit RGBA PNG and the first `columns` pixels of each row.

    A filtered byte depends only on the bytes to its left and above it, so the
    left edge of the image is read without undoing the rest of each row.
    """
    data = path.read_bytes()
    pos, idat, width, height = 8, [], 0, 0
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if (depth, color, interlace) != (8, 6, 0):
                raise ValueError(f"{path.name}: not an 8-bit RGBA PNG")
        elif kind == b"IDAT":
            idat.append(body)
        pos += 12 + length
    raw = zlib.decompress(b"".join(idat))
    stride, n = 1 + width * 4, columns * 4
    rows, above = [], bytearray(n)
    for y in range(height):
        kind = raw[y * stride]
        line = bytearray(raw[y * stride + 1:y * stride + 1 + n])
        for i in range(n):
            left = line[i - 4] if i >= 4 else 0
            up = above[i]
            corner = above[i - 4] if i >= 4 else 0
            if kind == 1:
                line[i] = (line[i] + left) & 255
            elif kind == 2:
                line[i] = (line[i] + up) & 255
            elif kind == 3:
                line[i] = (line[i] + (left + up) // 2) & 255
            elif kind == 4:
                p = left + up - corner
                pl, pu, pc = abs(p - left), abs(p - up), abs(p - corner)
                line[i] = (line[i] + (left if pl <= pu and pl <= pc else up if pu <= pc else corner)) & 255
        rows.append(line)
        above = line
    return width, height, rows


class ProfileLinksTest(unittest.TestCase):
    def test_capabilities_link_to_console_in_descriptions(self):
        links = re.findall(r"\[([^]]+)\]\(([^)]+)\)", section("Core Platform"))
        for capability in CAPABILITIES:
            with self.subTest(capability=capability):
                self.assertEqual(
                    [url for label, url in links if label == capability],
                    [f"https://platform.latere.ai/console/{capability.lower()}"],
                )
        self.assertIn(("Identity", "https://auth.latere.ai"), links)

    def test_every_capability_but_apps_names_its_open_core(self):
        # The section says each capability except Apps is built on an open
        # source core, so each one's paragraph links that core's repository.
        paragraphs = dict(re.findall(r"^\*\*\[([^]]+)\]\([^)]+\)\*\*(.*)$", section("Core Platform"), re.M))
        self.assertEqual(set(paragraphs), {"Identity", *CAPABILITIES})
        for capability in CAPABILITIES:
            if capability == "Apps":
                continue
            with self.subTest(capability=capability):
                self.assertRegex(
                    paragraphs[capability],
                    r"Check the open source core: \[\w+\]\(https://github\.com/latere-ai/[a-z-]+\)",
                )

    def test_applications_link_their_sites(self):
        links = re.findall(r"\[([^]]+)\]\(([^)]+)\)", section("Applications"))
        self.assertIn(("Latere Chat", "https://chat.latere.ai/"), links)
        self.assertIn(("Latere Studio", "https://studio.latere.ai/"), links)


class ProfileTeaserTest(unittest.TestCase):
    def test_teaser_images_are_in_the_repository(self):
        picture = PROFILE.read_text().split("<picture>", 1)[1].split("</picture>", 1)[0]
        urls = re.findall(r'(?:src|srcset)="([^"]+)"', picture)
        self.assertEqual(len(urls), 2)
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(RAW))
                self.assertTrue((ROOT / url[len(RAW):]).is_file())

    def test_alt_text_says_what_the_teaser_shows(self):
        picture = PROFILE.read_text().split("<picture>", 1)[1].split("</picture>", 1)[0]
        alt = re.search(r'alt="([^"]+)"', picture).group(1)
        teaser = TEASER.read_text()
        headline = re.sub(r"<[^>]+>", " ", re.search(r"<h1>(.*?)</h1>", teaser).group(1))
        self.assertIn(" ".join(headline.split()), alt)
        self.assertIn(re.search(r"<p>(.*?)</p>", teaser).group(1), alt)

    def test_teaser_text_starts_on_the_image_edge(self):
        # The teaser has no frame: its mark, headline and sentences start on
        # the image's left edge, where the README's own text starts. The
        # images are twice the layout size, so 6 pixels are 3 in the layout.
        columns = 16
        for theme in ("light", "dark"):
            with self.subTest(theme=theme):
                width, height, rows = left_columns(ASSETS / f"teaser-{theme}.png", columns)
                self.assertEqual((width, height), (2400, 800))
                ink = [x for row in rows for x in range(columns) if row[x * 4 + 3] >= 128]
                self.assertTrue(ink, "no text near the left edge")
                self.assertLessEqual(min(ink), 6)
                # A frame would draw a line down the first column.
                lined = sum(1 for row in rows if row[3] >= 24)
                self.assertLess(lined, height // 4)


if __name__ == "__main__":
    unittest.main()
