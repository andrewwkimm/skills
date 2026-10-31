"""Prepares a fresh working directory and store entry for a build job."""

import contextlib
import shutil
from pathlib import Path
from typing import Protocol


class ObjectStore(Protocol):
    """The two store operations preparing a workspace needs."""

    def delete(self, key: str) -> None:
        """Removes key; raises KeyError when it does not exist."""

    def put(self, key: str, data: bytes) -> None:
        """Stores data under key."""


def prepare_workspace(job_id: str, *, root: Path, store: ObjectStore) -> Path:
    """Returns ``root / job_id`` existing and empty, with the job's store entry absent.

    A missing directory, a missing root, and a missing store entry are normal
    results. Anything the worker cannot remove, and any store failure other than
    a missing key, raises.
    """
    job_dir = root / job_id
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(job_dir)
    job_dir.mkdir(parents=True)
    with contextlib.suppress(KeyError):
        store.delete(f"jobs/{job_id}")
    return job_dir
