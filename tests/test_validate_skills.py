from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_skills import validate_skill


class ValidateSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "example-skill"
        self.skill.mkdir()
        self.write_entry()

    def write_entry(self, body="", name="example-skill", description="A focused workflow."):
        (self.skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n",
            encoding="utf-8",
        )

    def test_valid_skill_with_encoded_resource_and_link_title(self):
        (self.skill / "reference notes.md").write_text("# Reference\n", encoding="utf-8")
        self.write_entry('[Notes](reference%20notes.md "Read when needed")')
        self.assertEqual(validate_skill(self.skill), [])

    def test_missing_and_invalid_frontmatter(self):
        for text in ("# No header", "---\nname: example-skill", "---\nname: [\n---\n"):
            with self.subTest(text=text):
                (self.skill / "SKILL.md").write_text(text, encoding="utf-8")
                self.assertTrue(validate_skill(self.skill))

    def test_name_must_match_directory(self):
        self.write_entry(name="different-skill")
        self.assertTrue(validate_skill(self.skill))

    def test_description_is_required(self):
        self.write_entry(description="''")
        self.assertTrue(validate_skill(self.skill))

    def test_missing_local_resource(self):
        self.write_entry("[Reference](references/missing.md)")
        self.assertTrue(validate_skill(self.skill))

    def test_resource_outside_skill_is_not_portable(self):
        (self.skill.parent / "outside.md").write_text("# Outside\n", encoding="utf-8")
        self.write_entry("[Reference](../outside.md)")
        self.assertTrue(validate_skill(self.skill))

    def test_external_urls_and_fragments_do_not_require_local_files(self):
        self.write_entry("[Docs](https://example.com/guide) [Section](#section)")
        self.assertEqual(validate_skill(self.skill), [])

    def test_reference_style_image_is_checked(self):
        self.write_entry("![Example][image]\n\n[image]: assets/missing.png")
        self.assertTrue(validate_skill(self.skill))


if __name__ == "__main__":
    unittest.main()
