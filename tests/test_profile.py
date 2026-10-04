"""Check the public profile's capability links and teaser: python3 -m unittest discover -s tests."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile" / "README.md"
TEASER = ROOT / "profile" / "assets" / "teaser" / "teaser.html"
# The profile is shown outside this repository, so its images are absolute.
RAW = "https://raw.githubusercontent.com/latere-ai/.github/main/"


class ProfileLinksTest(unittest.TestCase):
    def test_capabilities_link_to_console_in_descriptions(self):
        profile = PROFILE.read_text()
        core = profile.split("## Core Platform\n", 1)[1].split("\n## ", 1)[0]
        links = re.findall(r"\[([^]]+)\]\(([^)]+)\)", core)
        for capability in ("Agents", "Models", "Environments", "Repos", "Storage", "Apps"):
            with self.subTest(capability=capability):
                self.assertEqual(
                    [url for label, url in links if label == capability],
                    [f"https://platform.latere.ai/console/{capability.lower()}"],
                )
        self.assertIn(("Identity", "https://auth.latere.ai"), links)
        # Parsing has no console section, so it links its docs.
        self.assertIn(("Parsing", "https://platform.latere.ai/docs/parsing"), links)


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


if __name__ == "__main__":
    unittest.main()
