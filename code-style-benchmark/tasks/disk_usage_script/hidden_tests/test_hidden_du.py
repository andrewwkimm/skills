"""Hidden tests for the disk_usage_script task."""

import ast
from pathlib import Path

import du


def test_total_and_largest(tmp_path: Path) -> None:
    (tmp_path / "a").write_bytes(b"x" * 10)
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b").write_bytes(b"x" * 30)
    (tmp_path / "sub" / "c").write_bytes(b"x" * 20)

    total, largest = du.summarize(tmp_path)

    assert total == 60
    assert [(p.name, s) for p, s in largest] == [("b", 30), ("c", 20), ("a", 10)]


def test_symlinks_are_not_followed(tmp_path: Path) -> None:
    target = tmp_path / "real"
    target.mkdir()
    (target / "big").write_bytes(b"x" * 100)
    (tmp_path / "link").symlink_to(target)

    total, _ = du.summarize(tmp_path)

    assert total == 100


def test_script_stays_small_and_class_free() -> None:
    source = Path(du.__file__).read_text()
    tree = ast.parse(source)

    assert not [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)], "a 40-line script needs no classes"
    assert "pydantic" not in source
    assert len(source.splitlines()) <= 80
