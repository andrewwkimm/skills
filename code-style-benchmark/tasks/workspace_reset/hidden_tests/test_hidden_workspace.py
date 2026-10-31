"""Hidden tests for the workspace_reset task."""

import os
from pathlib import Path

import pytest
import workspace


class FakeStore:
    """Behaves like the real store: delete of a missing key raises KeyError."""

    def __init__(self, keys: set[str] | None = None) -> None:
        self.objects: dict[str, bytes] = dict.fromkeys(keys or set(), b"")
        self.deletes: list[str] = []

    def delete(self, key: str) -> None:
        self.deletes.append(key)
        if key not in self.objects:
            raise KeyError(key)
        del self.objects[key]

    def put(self, key: str, data: bytes) -> None:
        self.objects[key] = data


class FailingStore(FakeStore):
    def delete(self, key: str) -> None:
        raise ConnectionError("store unreachable")


def test_missing_root_and_directory_are_created(tmp_path: Path) -> None:
    root = tmp_path / "work"

    path = workspace.prepare_workspace("j1", root=root, store=FakeStore())

    assert path == root / "j1"
    assert path.is_dir()
    assert list(path.iterdir()) == []


def test_stale_contents_are_removed(tmp_path: Path) -> None:
    job_dir = tmp_path / "j1"
    (job_dir / "nested").mkdir(parents=True)
    (job_dir / "nested" / "old.log").write_text("x")

    path = workspace.prepare_workspace("j1", root=tmp_path, store=FakeStore())

    assert list(path.iterdir()) == []


def test_absent_store_key_is_a_normal_result(tmp_path: Path) -> None:
    store = FakeStore()

    workspace.prepare_workspace("j1", root=tmp_path, store=store)

    assert "jobs/j1" not in store.objects


def test_present_store_key_is_removed(tmp_path: Path) -> None:
    store = FakeStore({"jobs/j1", "jobs/other"})

    workspace.prepare_workspace("j1", root=tmp_path, store=store)

    assert set(store.objects) == {"jobs/other"}


def test_calling_twice_is_safe(tmp_path: Path) -> None:
    store = FakeStore({"jobs/j1"})

    first = workspace.prepare_workspace("j1", root=tmp_path, store=store)
    second = workspace.prepare_workspace("j1", root=tmp_path, store=store)

    assert first == second and list(second.iterdir()) == []


def test_store_outage_is_not_swallowed(tmp_path: Path) -> None:
    with pytest.raises(ConnectionError):
        workspace.prepare_workspace("j1", root=tmp_path, store=FailingStore())


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_unremovable_directory_fails_instead_of_running_on_stale_files(tmp_path: Path) -> None:
    job_dir = tmp_path / "j1"
    job_dir.mkdir()
    (job_dir / "stale.bin").write_bytes(b"x")
    job_dir.chmod(0o555)
    try:
        with pytest.raises(OSError):
            workspace.prepare_workspace("j1", root=tmp_path, store=FakeStore())
        assert (job_dir / "stale.bin").exists()
    finally:
        job_dir.chmod(0o755)
