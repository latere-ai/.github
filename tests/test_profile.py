"""Check public profile capability links: python3 -m unittest discover -s tests."""

from pathlib import Path
import re
import unittest


PROFILE = Path(__file__).resolve().parents[1] / "profile" / "README.md"


class ProfileLinksTest(unittest.TestCase):
    def test_capabilities_link_to_console_in_descriptions_and_footer(self):
        profile = PROFILE.read_text()
        core = profile.split("## Core Platform\n", 1)[1].split("\n## ", 1)[0]
        footer = profile.split("## Links\n", 1)[1]
        for section in (core, footer):
            links = re.findall(r"\[([^]]+)\]\(([^)]+)\)", section)
            for capability in ("Agents", "Models", "Environments", "Code", "Storage"):
                with self.subTest(section="core" if section == core else "footer", capability=capability):
                    self.assertEqual(
                        [url for label, url in links if label == capability],
                        [f"https://platform.latere.ai/console/{capability.lower()}"],
                    )
            self.assertIn(("Identity", "https://auth.latere.ai"), links)


if __name__ == "__main__":
    unittest.main()
