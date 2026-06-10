"""Tests for zenkins install-skills command."""

import argparse


def test_install_skills_copies_files(tmp_path):
    """install_skills_command copies SKILL.md to target dir."""
    from zenkins.skills import install_skills_command

    args = argparse.Namespace(skills_dir=str(tmp_path))
    install_skills_command(args)

    dest = tmp_path / "zenkins"
    assert (dest / "SKILL.md").exists()


def test_install_skills_creates_target_dir(tmp_path):
    """install_skills_command creates the target directory if it doesn't exist."""
    from zenkins.skills import install_skills_command

    target = tmp_path / "nested" / "skills"
    args = argparse.Namespace(skills_dir=str(target))
    install_skills_command(args)

    assert (target / "zenkins" / "SKILL.md").exists()


def test_install_skills_skill_md_has_name(tmp_path):
    """Installed SKILL.md contains the skill name front matter."""
    from zenkins.skills import install_skills_command

    args = argparse.Namespace(skills_dir=str(tmp_path))
    install_skills_command(args)

    content = (tmp_path / "zenkins" / "SKILL.md").read_text()
    assert "name: zenkins" in content
